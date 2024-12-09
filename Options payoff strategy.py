import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk,Label, Entry, Button, OptionMenu, StringVar, Scale, HORIZONTAL, filedialog, messagebox

def calculate_and_plot(save=False):
    """
    Collect the user input, calculate the payoffs, plot the payoff diagram.
    """
   
    try:
        strike_prices_entry=np.array(list(map(float,strike_prices_entry.get().split())))
        premiums_Entry=np.array(list(map(float,premiums_Entry.get().split())))
        
        if len(strike_prices_entry) !=len(premiums_Entry):
            raise ValueError("Strike prices and premiums must have the saem number of entries")
        
        spot_start_slider=spot_start_slider.get()
        spot_end_slider=spot_end_slider.get()
        spot_step_slider=spot_step_slider.get()
        
        spot_prices=np.arrange(spot_start_slider,spot_end_slider,spot_step_slider)
        option_type_var=option_type_var.get()
        
        #Generate the payoff diagram
        plt.figure(figsize=(10,6))
        for strike,premium in zip(strike_prices_entry,premiums_Entry):
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
    """
    Calculate the payoff for various option types.
    """
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
    
#Create the application window
root=Tk()   
root.title("Options payoff diagram")

#Create labels and inputs
Label(root,text="Strike prices (space-seperated):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
strike_prices_entry=Entry(root,width=40)
strike_prices_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root,text="Premiums (space-seperated):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
premiums_Entry=Entry(root,width=40)
premiums_Entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Option Type (space-seperated):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
option_type_var=StringVar(root)
option_type_var.set("Call")# This is the default option type
OptionMenu(root,option_type_var, "Call", "Put", "Short_Call", "Short_Put").grid(row=2, column=0, sticky="w", padx=10, pady=5)

#The sliders for the spot price ranges
Label(root, text="Spot price start:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
Spot_start_Slider=Scale(root,from_=0, to=200, orient=HORIZONTAL, length=300)
Spot_start_Slider.set(50)
Spot_start_Slider.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Spot price End:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
Spot_end_slider=Scale(root, from_=0, to=200, orient=HORIZONTAL,length=300)
Spot_end_slider.set(150)
Spot_end_slider.grid(row=4, column=1, padx=10, pady=5)

Label(root,text="Spot price step:").grid(row=5, column=0, padx=10, pady=5)
spot_step_slider=Scale(root, from_=1, to=20, orient=HORIZONTAL, length=300)
spot_step_slider.set(5)
spot_step_slider.grid(row=5, column=1, padx=10, pady=5)

#The buttons for saving and plotting
Button(root, text="Plot Payoff diagram", command=lambda: calculate_and_plot(save=False)).grid(row=6, column=0, padx=10, pady=10)
Button(root, text="Save payoff diagram", command=lambda: calculate_and_plot(save=True)).grid(row=6, column=0, padx=10, pady=10)

#Run the application
root.mainloop()