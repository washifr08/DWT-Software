from customtkinter import *  # ctk library
from PIL import Image  # pillow for image importing
from tkinter import messagebox  # messagebox funtionality for errors
from openpyxl import *  # allows interractions with excel
import os  # allows saving files to device
import sys  # allows for sys.exit() function
import subprocess  # allows opening of new python files

# creates box and size and title
macro_calc = CTk()
macro_calc.geometry("1200x800")
macro_calc.title("")

# finds width and height of screen
screen_width = macro_calc.winfo_screenwidth()
screen_height = macro_calc.winfo_screenheight()

# calculates x and y coordinates for the window to be centered
centre_x = int((screen_width - 1200) / 2)
centre_y = int((screen_height - 1000) / 2)

# sets the position of the window to be centered
macro_calc.geometry(f"+{centre_x}+{centre_y}")

# top bar frame for app title and dark/light toggle
header = CTkFrame(macro_calc, fg_color=("gray90", "#212121"), height=50, corner_radius=0)
header.pack(fill="both", side="top")

# app title on the left 
header_title = CTkLabel(header, text="Digital Wellbeing Tracker", font=("Century Gothic", 22, "bold"))
header_title.pack(side="left", padx=20)

def dark_light_toggle():  # dark/light mode toggle function as used in signup page
    theme_state = get_appearance_mode()
    if theme_state == "Dark":
        set_appearance_mode("light")
        set_all_light()
    else:
        set_appearance_mode("dark")
        set_all_dark()

# dark/light mode toggle on the right
theme_switch = CTkSwitch(header, text="Dark / Light Mode",font=("Century Gothic", 14), command=dark_light_toggle)
theme_switch.pack(side="right", padx=20, pady=10)

contents_frame = CTkFrame(macro_calc, fg_color=("gray95", "#212121"),height= 200, corner_radius=25)
contents_frame.pack( fill="both", expand=True, pady=(35, 20), padx=30)

# function to apply light mode colors to frames
def set_all_light():
    macro_calc.configure(fg_color="gray85")
    header.configure(fg_color="gray95")
    contents_frame.configure(fg_color="gray95")

# function to apply dark mode colors to frames
def set_all_dark():
    macro_calc.configure(fg_color="#1A1A1A")
    header.configure(fg_color="#212121")
    contents_frame.configure(fg_color="#212121")
 
if get_appearance_mode() == "Dark":
    set_all_dark()
else:
    set_all_light()


if len(sys.argv) >= 2:
    user_email = sys.argv[1]
else:
    user_email = ""

print(user_email)

macro_calc.mainloop()