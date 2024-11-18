import numpy as np
import matplotlib.pyplot as plt

def get_user_input(prompt):
    """
    Get user input as a list of floating-point numbers.
    """
    try:
        return np.array(list(map(float, input(prompt).split())))
    except ValueError:
        print("Invalid input. Please enter numbers separated by spaces.")
        return get_user_input(prompt)

def option_payoff(strike, premium, spot, option_type):
    """
    Calculate the payoff for various option types.
    """
    if option_type == "Call":
        return np.maximum(0, spot - strike) - premium
    elif option_type == "Put":
        return np.maximum(0, strike - spot) - premium
    elif option_type == "Short_Call":
        return -(np.maximum(0, spot - strike)) + premium
    elif option_type == "Short_Put":
        return -(np.maximum(0, strike - spot)) + premium
    else:
        raise ValueError(f"Unknown option type: {option_type}")

def plot_option_diagram(strike_prices, premiums, spot_prices, option_type):
    """
    Generate and plot the payoff diagram for options.
    """
    plt.figure(figsize=(10, 6))
    for strike, premium in zip(strike_prices, premiums):
        payoff = option_payoff(strike, premium, spot_prices, option_type)
        plt.plot(spot_prices, payoff, label=f'{option_type} (Strike: {strike})')

    plt.title(f'{option_type} Option Payoff Diagram')
    plt.xlabel('Spot Price')
    plt.ylabel('Payoff')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main Program
if __name__ == "__main__":
    print("Options Payoff Calculator")

    # Get user inputs
    strike_prices = get_user_input("Enter the strike prices separated by spaces: ")
    premiums = get_user_input("Enter the premiums separated by spaces: ")
    spot_range = get_user_input("Enter the spot price range (start, end, step): ")

    # Generate the spot prices array
    try:
        spot_prices = np.arange(*spot_range)
    except ValueError:
        print("Invalid spot price range. Please provide start, end, and step values.")
        exit()

    # Validate input lengths
    if len(strike_prices) != len(premiums):
        print("Error: Strike prices and premiums must have the same number of elements.")
        exit()

    # Get the option type
    option_type = input("Enter the option type (Call, Put, Short_Call, Short_Put): ").strip()
    if option_type not in {"Call", "Put", "Short_Call", "Short_Put"}:
        print(f"Invalid option type: {option_type}")
        exit()

    # Plot the option diagram
    plot_option_diagram(strike_prices, premiums, spot_prices, option_type)