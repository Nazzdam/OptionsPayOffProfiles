import numpy as np
import matplotlib.pyplot as plt
from _tkinter import Tk,Label, Entry, Button, OptionMenu, StringVar, Scale, Horizontal, Filedialog, messagebox

def calculate_and_plot(save=False):
   
    try:
        strike_prices_entry=np.array(list(map(float,strike_prices_entry.get().split())))
        premiums_entry=np.array(list(map(float,premiums_entry.get().split())))
        
        if len(strike_prices_entry) !=len(premiums_entry):
            raise ValueError("Strike prices and premiums must have the saem number of entries")
        
        spot_start_slider=spot_start_slider.get()
        spot_end_slider=spot_end_slider.get()
        spot_step_slider=spot_step_slider.get()
        
        spot_prices=np.arrange(spot_start_slider,spot_end_slider,spot_step_slider)
        option_type_var=option_type_var.get()
        
        #Generate the payoof diagram
        plt.figure(figsize=(10,6))
        for strike,premium in zip(strike_prices_entry,premiums_entry):
            payoff=option_type_var(strike,premium,spot_prices,option_type_var)
            plt.plot(spot_prices,payoff,Label=f'{option_type_var} (Strike:{strike})')
            
        plt.title(f'{option_type_var} Option payoff diagram')    
        plt.xlabel('Spot price')
        plt.ylabel('Payoff')
        plt.grid(True)
        
        if save:
            file_path=Filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG Files","*.png"), ("All Files", "*.*")], title="Save Payoff Diagram")
            if file_path:
                plt.savefig(file_path)
                messagebox.showinfo("Success", f"Plot saved as {file_path}")
            plt.close()    
        else:
            plt.show()
    except Exception as e:
        messagebox.showerror("Error",f"An error occurred:{e}")
        
def option_Payoff(strike,premium,spot,option_type):
    if option_type=="Call":
        return np.maximum(0,spot-strike )-premium
    elif option_type=="Put":
        return np.maximum(strike-spot)-premium
    elif option_type=="Short Call":
        return -(np.maximum(0,spot-strike))+premium
    elif option_type=="Short Put":
        return -(np.maximum(0,strike-spot))+premium
    else:
        raise ValueError(f"Unkown Option type:{option_type}")            