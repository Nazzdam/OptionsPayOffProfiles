# This programm is used to calculate the options payoff diagram of 7 different options.
import numpy as np
import matplotlib.pyplot as plt

#Get user input
def options_user_input(prompt):
   return np.array(list(map(float, input(prompt).split())))

#get user input for the details of the opton
strikePrices=options_user_input("Enter the stike prices sperated by spaces")
spotPrices=options_user_input("Enter the spot prices as a range sperated by spaces")
premiums=options_user_input("Enter the premiums seperated by spaces")

#Define the type of option and it's payyoff diagram
def option_Payoff(strike,premium,spot,option_type):
    if option_type=="Call":
        #intrinsic vlaue of a call
        np.maximum(0,spot-strike)-premium
    elif option_type=="Put":
        #instrinsic value of a put
        np.maximum(0,strike-spot)-premium
    elif option_type=="Short_Call"    :
        np.maximum(0,spot-strike)+premium
    elif option_type=="Short_Put":
        np.maximum(0,strike-spot)+premium

#Generate an options payoff diagram
def option_ploted_diagram(strike, premium, spot, option_type="Call"):
    plt.figure(figsize=(10,6))
    
    for i in range(len(strikePrices)):
        strike=strikePrices[i]
        premium=premiums[i]
        
        payoff=option_Payoff(strike,premium,spot,option_type)
        plt.plot(spotPrices, payoff,label=f'{option_type} Strike:{strike}')
        
        plt.title(f'{option_type} Option Payoff Diagram')
        plt.xlabel('Spot price')
        plt.ylabel('Payoff')
        plt.legend()
        plt.grid(True)
        plt.show
#Promt the user to enter the option type
option_type=input("Enter the option type(Call or Put or Short_Call or Short_Put):")       
#once we have user input, compute the payoff diagram
option_ploted_diagram(strikePrices,premiums,spotPrices,option_type) 