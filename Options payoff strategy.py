# This programm is used to calculate the options payoff diagram of 7 different options.
import numpy as np
import matplotlib.pyplot as plt

#Get user input
def options_user_input(prompt):
    return np.array(list(map(float,input(prompt).split)))

#get user input for the details of the opton
strikePrices=options_user_input("Enter the stike prices sperated by spaces")
spotPrices=options_user_input("Enter the spot prices as a range sperated by spaces")
premiums=options_user_input("Enter the premiums seperated by spaces")

#Define the type of option and it's payyoff diagram