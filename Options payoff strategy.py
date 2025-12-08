import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, OptionMenu, StringVar, Scale, HORIZONTAL, filedialog, messagebox
from numpy import exp, log, sqrt
from scipy.stats import norm

def calculate_and_plot(save=False):
    """
    Collect the user input, calculate the payoffs, plot the payoff diagram.
    """
    try:
        strikes_text = strike_prices_entry.get().strip()
        premiums_text = premiums_entry.get().strip()

        if not strikes_text or not premiums_text:
            raise ValueError("Provide strike prices and premiums (space-separated).")

        strike_prices = np.array(list(map(float, strikes_text.split())))
        premiums = np.array(list(map(float, premiums_text.split())))
        if len(strike_prices) != len(premiums):
            raise ValueError("Strike prices and premiums must have the same count.")

        spot_start = Spot_start_Slider.get()
        spot_end = Spot_end_slider.get()
        spot_step = spot_step_slider.get()
        if spot_start >= spot_end:
            raise ValueError("Spot start must be less than spot end.")
        spot_prices = np.arange(spot_start, spot_end + 1e-9, spot_step)

        option_type = option_type_var.get()
        plt.figure(figsize=(10, 6))
        for strike, premium in zip(strike_prices, premiums):
            payoff = option_Payoff(strike, premium, spot_prices, option_type)
            plt.plot(spot_prices, payoff, label=f'{option_type} (K={strike}, prem={premium})')
        plt.title(f'{option_type} Option Payoff Diagram')
        plt.xlabel('Spot Price')
        plt.ylabel('Payoff')
        plt.legend()
        plt.grid(True)

        if save:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
            if file_path:
                plt.savefig(file_path)
                messagebox.showinfo("Saved", f"Plot saved: {file_path}")
            plt.close()
        else:
            plt.show()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def option_Payoff(strike, premium, spot, option_type):
    """
    Calculate the payoff for various option types.
    """
    if option_type == "Call":
        return np.maximum(0, spot - strike) - premium
    elif option_type == "Put":
        return np.maximum(0, strike - spot) - premium
    elif option_type == "Short Call":
        return -np.maximum(0, spot - strike) + premium
    elif option_type == "Short Put":
        return -np.maximum(0, strike - spot) + premium
    else:
        raise ValueError(f"Unknown Option type: {option_type}")

def Black_Scholes_price(X, S, T, r, Sigma, option_type):
    """
    Calculate option price using Black Scholes formula.
    X: Strike price
    S: Spot price
    T: Time to maturity
    r: Risk-free rate
    Sigma: Volatility
    """
    if S <= 0 or X <= 0 or T <= 0 or Sigma <= 0:
        raise ValueError("S, X, T and Sigma must be positive.")
    d1 = (log(S / X) + (r + 0.5 * Sigma**2) * T) / (Sigma * sqrt(T))
    d2 = d1 - Sigma * sqrt(T)
    if option_type == "Call":
        return S * norm.cdf(d1) - X * exp(-r * T) * norm.cdf(d2)
    elif option_type == "Put":
        return X * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError(f"Unknown Option type: {option_type}")

def compute_and_show_bs_price():
    try:
        spots = spot_price_entry.get().strip()
        if not spots:
            raise ValueError("Enter spot price (single value) for Black‑Scholes.")
        S = float(spots.split()[0])

        strikes_text = strike_prices_entry.get().strip()
        if not strikes_text:
            raise ValueError("Enter at least one strike price.")
        X = float(strikes_text.split()[0])  # use first strike by default

        T = float(time_to_maturity_entry.get())
        r = float(interest_rate_entry.get()) / 100.0
        Sigma = float(volatility_entry.get()) / 100.0

        price = Black_Scholes_price(X, S, T, r, Sigma, option_type_var.get())
        messagebox.showinfo("Black-Scholes Price", f"Option Price: {price:.4f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def Option_Greeks(Delta, Gamma, Theta, Vega, Rho):
   """
   Docstring for Option_Greeks
   :param Delta: Partial derviavtive of option price with respect to underlying asset price.
   :param Gamma: Partial derivative of Delta with respect to underlying asset price.
   :param Theta: Partial derivative of option price with respect to time to expiration.
   :param Vega: Partial derivative of option price with respect to volatility.
   :param Rho: Partial derivative of option price with respect to interest rate.
   """
# Create the application window
root = Tk()
root.title("Options Dashboard")

# Row 0: Spot price for BS
Label(root, text="Spot Price (Black‑Scholes):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
spot_price_entry = Entry(root, width=20)
spot_price_entry.grid(row=0, column=1, padx=10, pady=5)

# Row 1: Strike prices
Label(root, text="Strike Prices (space-separated):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
strike_prices_entry = Entry(root, width=40)
strike_prices_entry.grid(row=1, column=1, padx=10, pady=5)

# Row 2: Premiums
Label(root, text="Premiums (space-separated):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
premiums_entry = Entry(root, width=40)
premiums_entry.grid(row=2, column=1, padx=10, pady=5)

# Row 3: Option type
Label(root, text="Option Type:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
option_type_var = StringVar(root)
option_type_var.set("Call")
OptionMenu(root, option_type_var, "Call", "Put", "Short Call", "Short Put").grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Row 3 column 1 :Option Type
Label(root, text="Option Type:").grid (row=3), column=1, sticky="w", padx=10, pady=5
option_type_var = StringVar(root)
option_type_var.set("Call")
OptionMenu(root, option_type_var, "Call", "Put", "Short Call", "Short Put").grid(row=3, column=1, sticky="w", padx=10,pady=5)
                                                                                 
# Row 4: Rate, vol, T
Label(root, text="Interest Rate (%):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
interest_rate_entry = Entry(root, width=10)
interest_rate_entry.grid(row=4, column=1, sticky="w", padx=10, pady=5)
Label(root, text="Volatility (%):").grid(row=4, column=2, sticky="w", padx=10, pady=5)
volatility_entry = Entry(root, width=10)
volatility_entry.grid(row=4, column=3, sticky="w", padx=10, pady=5)

Label(root, text="Time to Maturity (years):").grid(row=5, column=0, sticky="w", padx=10, pady=5)
time_to_maturity_entry = Entry(root, width=10)
time_to_maturity_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)

# Payoff sliders
Label(root, text="Spot Price Start:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
Spot_start_Slider = Scale(root, from_=0, to=200, orient=HORIZONTAL, length=300)
Spot_start_Slider.set(50)
Spot_start_Slider.grid(row=6, column=1, padx=10, pady=5)

Label(root, text="Spot Price End:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
Spot_end_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, length=300)
Spot_end_slider.set(150)
Spot_end_slider.grid(row=7, column=1, padx=10, pady=5)

Label(root, text="Spot Price Step:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
spot_step_slider = Scale(root, from_=1, to=50, orient=HORIZONTAL, length=300)
spot_step_slider.set(5)
spot_step_slider.grid(row=8, column=1, padx=10, pady=5)

# Buttons
Button(root, text="Plot Payoff Diagram", command=lambda: calculate_and_plot(save=False)).grid(row=9, column=0, padx=10, pady=10)
Button(root, text="Save Payoff Diagram", command=lambda: calculate_and_plot(save=True)).grid(row=9, column=1, padx=10, pady=10)
Button(root, text="Calculate Black‑Scholes Price", command=compute_and_show_bs_price).grid(row=9, column=2, padx=10, pady=10)

root.mainloop()