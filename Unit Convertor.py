from tkinter import *
from tkinter import ttk

"""
> This is an unit convertor application created using the tkinter module in python 3 programming language. It is 
  programmed to convert from one unit to another of temperature, currency and distance physical quantities.
> This project was created by Anish Udupa H, Akash Harsha Hegde and Anup D Sirsikar as a first semister project at PES
  University EC Campus.
> License: GPL. This project is licensed under the GPL license, and is hence free to be used, distributed and modified.
> Version: 1.0. Released on 11th March, 2021.
"""

def enabled_mode(unit_tuple):
    input_value["state"] = "normal"
    input_unit["state"] = "readonly"
    output_value["state"] = "readonly"
    output_unit["state"] = "readonly"

    input_unit["values"] = unit_tuple
    input_unit.current(0)

    output_unit["values"] = unit_tuple
    output_unit.current(0)
    unit_callback(None)

def disabled_mode():
    clear = StringVar("")
    input_value["state"] = "disabled"
    input_value["textvariable"] = clear
    input_unit["state"] = "disabled"
    input_unit.set("")
    output_value["state"] = "disabled"
    output_value["textvariable"] = clear
    output_unit["state"] = "disabled"
    output_unit.set("")

def quantity_callback(event):
    __opt = quantity.current()
    if 1 <= __opt <= 3:
        enabled_mode(create_unit_list(__opt))
    else:
        disabled_mode()

def unit_callback(event):
    __inp_opt = input_unit.current()
    __out_opt = output_unit.current()
    __quant_opt = quantity.current()
    compute_and_display_value(__inp_opt, __out_opt, __quant_opt)

def create_unit_list(mode):
    _l = tuple()
    if mode == 1:
        # Quantity is temperature.
        _l = ("K", "°C", "°F")
    elif mode == 2:
        # Quantity is currency.
        _l = ("USD", "EUR", "GBP", "INR", "JPY")
    elif mode == 3:
        # Quantity is distance.
        _l = ("m.", "km.", "cm.", "mi.", "ft.", "in.")
    return _l

def compute_and_display_value(inp_unit, out_unit, quan_selected):
    func = None
    try:
        __inp_val = float(input_value.get())

        if quan_selected == 1:
            func = temp_convertor
        elif quan_selected == 2:
            func = currency_convertor
        elif quan_selected == 3:
            func = distance_convertor

        out_val = func(inp_unit, out_unit, __inp_val)
        if out_val is None:
            out_val = "---"
    except ValueError:
        out_val = "---"
        print("Invalid input")  # For debugging purpose

    print_value(out_val)

def temp_convertor(inp_unit, out_unit, inp_val):
    out_val = None  # Initialising the value
    if inp_unit == out_unit:
        out_val = inp_val
    elif inp_unit == 0 and out_unit == 1:
        # Kelvin to celsius
        out_val = round(inp_val - 273.15, 2)
    elif inp_unit == 0 and out_unit == 2:
        # Kelvin to Fahrenheit
        out_val = round(1.8 * (inp_val - 273.15) + 32, 2)
    elif inp_unit == 1 and out_unit == 0:
        # Celsius to kelvin
        out_val = round(inp_val + 273.15, 2)
    elif inp_unit == 1 and out_unit == 2:
        # Celsius to fahrenheit
        out_val = round(1.8 * inp_val + 32, 2)
    elif inp_unit == 2 and out_unit == 0:
        # Fahrenheit to kelvin
        out_val = round(((inp_val - 32)/1.8) + 273.15, 2)
    elif inp_unit == 2 and out_unit == 1:
        # Fahrenheit to celsius
        out_val = round((inp_val - 32)/1.8, 2)
    try:
        val = round(out_val, 2)
        return val
    except TypeError:
        return None

def distance_convertor(inp_unit, out_unit, inp_val):
    # Similar to 1 m = [1m, 0.001 cm, 1000 km, 0.00062 miles, 3.281 ft, 39.37 in]
    meter_multiplier_list = [1, 0.001, 1000, 0.00062, 3.281, 39.37]

    try:
        # Calling the values in their respective units.
        value = inp_val * meter_multiplier_list[out_unit]/meter_multiplier_list[inp_unit]
    except IndexError:
        return None
    try:
        v = round(value, 5)
        return v
    except TypeError:
        return None

def currency_convertor(inp_unit, out_unit, inp_val):
    # Similar to 1 USD = [1 USD, 0.84 EUR, 0.72 GRB, 72.64 INR, 108.52 JPY]
    usd_multiplier_list = [1, 0.84, 0.72, 72.64, 108.52]

    try:
        # Calling the values in their respective units.
        out_val = inp_val * usd_multiplier_list[out_unit]/usd_multiplier_list[inp_unit]
    except IndexError:
        return None
    try:
        val = round(out_val, 2)
        return val
    except TypeError:
        return None

def print_value(value):
    # Prints the value to output Entry widget.
    __s = StringVar()
    __s.set(str(value))
    output_value["textvariable"] = __s


# Main
window = Tk()
window.title("Unit Convertor")
window.geometry("585x200")  # Setting the geometry
window.resizable(0, 0)  # The window is non resizable

quantity = ttk.Combobox(window, width=27, state="readonly", font=("Times New Roman", 30), justify=CENTER)
quantity["values"] = ("--Select a quantity--", " Temperature", " Currency", " Distance")
quantity.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
quantity.current(0)
quantity.bind("<<ComboboxSelected>>", quantity_callback)
quantity.bind("<FocusIn>", lambda event: event.widget.master.focus_set())  # Used to lose the blue focus highlight.

input_value = Entry(window, width=10, state="disabled", font=("Times New Roman", 20), justify=CENTER)
input_value.grid(row=1, column=0, padx=10, pady=10)
input_value.bind("<Return>", unit_callback)

input_unit = ttk.Combobox(window, width=5, state="disabled", font=("Times New Roman", 20), justify=CENTER)
input_unit.grid(row=1, column=1, sticky="w", padx=5, pady=10)
input_unit.bind("<<ComboboxSelected>>", unit_callback)
input_unit.bind("<FocusIn>", lambda event: event.widget.master.focus_set())  # Used to lose the blue focus highlight.

ttk.Label(window, text="=", font=("Times New Roman", 40, "bold")).grid(row=1, column=2, padx=10, pady=10)

output_value = Entry(window, width=10, state="disabled", font=("Times New Roman", 20), justify=CENTER, relief="sunken")
output_value.grid(row=1, column=3, sticky="w", padx=5, pady=10)

output_unit = ttk.Combobox(window, width=5, state="disabled", font=("Times New Roman", 20), justify=CENTER)
output_unit.grid(row=1, column=4, sticky="w", padx=5, pady=10)
output_unit.bind("<<ComboboxSelected>>", unit_callback)
output_unit.bind("<FocusIn>", lambda event: event.widget.master.focus_set())  # Used to lose the blue focus highlight.

window.mainloop()
