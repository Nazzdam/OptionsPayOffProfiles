# This programm is used to calculate the options payoff diagram of 7 different options.
import numpy as np
import matplotlib.pyplot as plt

# these are the deatils of the options
strike_Prices=np.array([8800,9000,9200,9400,9600,9800,10000])
premiums=np.array([])
spot_Prices=np.array({8700,8800,9000,9200,9400,9600,9800,10000,101000})

#Define the options
def option_payoff(strike,premium,spot,option_type):
    if option_type=="call":
        #Call option intrinsic value
        return np.maximum(spot-strike,0)-premium
    elif option_type=="put":
        #Put intrisic value
        return np.maximum(strike-spot,0)-premium
    
#Generate a payoff diagram
   