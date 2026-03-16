from customtkinter import *  # ctk library
from PIL import Image  # pillow for image importing
from tkinter import messagebox  # messagebox funtionality for errors
from openpyxl import *  # allows interractions with excel
import os  # allows saving files to device
import sys  # allows for sys.exit() function
import subprocess  # allows opening of new python files
import matplotlib # for plotting graphs if needed

# creates box and size and title
macro_calc = CTk()
macro_calc.geometry("1200x800")
macro_calc.title("D.W.T - Macro Nutritional Calculator")

#changes default color theme to green
set_default_color_theme("green")

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

# dark/light mode toggle function as used in signup page
def dark_light_toggle():  
    theme_state = get_appearance_mode()
    if theme_state == "Dark":
        set_appearance_mode("light")
        set_all_light()
    else:
        set_appearance_mode("dark")
        set_all_dark()

# dark/light mode toggle on the top right
theme_switch = CTkSwitch(header, text="Dark / Light Mode", font=("Century Gothic", 14), command=dark_light_toggle)
theme_switch.pack(side="right", padx=20, pady=10)

contents_frame = CTkFrame(macro_calc, fg_color=("gray95", "#212121"), height=200, corner_radius=25)
contents_frame.pack(fill="both", expand=True, pady=(25, 20), padx=30)

# function to apply light mode colors to frames and contents
def set_all_light():
    macro_calc.configure(fg_color="gray85")
    header.configure(fg_color="gray95")
    contents_frame.configure(fg_color="gray95")

# function to apply dark mode colors to frames and contents
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

# top-centre title inside contents_frame
title_label = CTkLabel(contents_frame, text="Your personalised Macro Nutritional Calculator", font=("Century Gothic", 30, "bold"), text_color="#4CAF50")
title_label.place(relx=0.5, y=18, anchor="n")

weight_entry_text = CTkLabel(contents_frame, text="Weight (kg)", font=("Century Gothic", 14))
weight_entry_text.pack(anchor="w", padx=25, pady=(70, 2))
weight_entry = CTkEntry(contents_frame, placeholder_text="e.g. 62.5", width=300, height=36,
                        corner_radius=10, font=("Century Gothic", 16))
weight_entry.pack(anchor="w", padx=25, pady=(0, 1))

height_entry_text = CTkLabel(contents_frame, text="Height (cm)", font=("Century Gothic", 14))
height_entry_text.pack(anchor="w", padx=25, pady=(16, 2))
height_entry = CTkEntry(contents_frame, placeholder_text="e.g. 175", width=300, height=36,
                        corner_radius=10, font=("Century Gothic", 16))
height_entry.pack(anchor="w", padx=25, pady=(0, 1))

age_entry_text = CTkLabel(contents_frame, text="Age", font=("Century Gothic", 14))
age_entry_text.pack(anchor="w", padx=25, pady=(16, 2))
age_entry = CTkEntry(contents_frame, placeholder_text="e.g. 25", width=300, height=36,
                        corner_radius=10, font=("Century Gothic", 16))
age_entry.pack(anchor="w", padx=25, pady=(0, 1))

# gender dropdown
sex_label = CTkLabel(contents_frame, text="Sex", font=("Century Gothic", 14))
sex_label.pack(anchor="w", padx=25, pady=(10, 2))
user_sex = StringVar(value="Male")
sex_dropdown = CTkOptionMenu(contents_frame, values=["Male", "Female"], variable=user_sex,
                             width=300, height=36, corner_radius=10, font=("Century Gothic", 16), fg_color="#469E4A",
                               button_color="#3D8B40", button_hover_color="#2F5F30", text_color="#000000")
sex_dropdown.pack(anchor="w", padx=25, pady=(0, 5))

# algorithm decision dropdown
algotihm_label = CTkLabel(contents_frame, text="Choose your algorithm", font=("Century Gothic", 14))
algotihm_label.pack(anchor="w", padx=25, pady=(10, 2))
user_algorithm = StringVar(value="Mifflin-St Jeor")
algorithm_dropdown = CTkOptionMenu(contents_frame, values=["Mifflin-St Jeor", "Katch-McArdle"], variable=user_algorithm,
                             width=300, height=36, corner_radius=10, font=("Century Gothic", 16), fg_color="#469E4A",
                               button_color="#3D8B40", button_hover_color="#2F5F30", text_color="#000000")
algorithm_dropdown.pack(anchor="w", padx=25, pady=(0, 5))

weight_change_label = CTkLabel(contents_frame, text="Choose your weight gain/loss rate PER WEEK (kg)", font=("Century Gothic", 14))
weight_change_label.pack(anchor="w", padx=25, pady=(10, 2))
weight_change_entry = CTkEntry(contents_frame, placeholder_text="e.g. 0.5", width=300, height=36,
                        corner_radius=10, font=("Century Gothic", 16))
weight_change_entry.pack(anchor="w", padx=25, pady=(0, 5))

# activity level slider
activity_label_title = CTkLabel(contents_frame, text="Activity level", font=("Century Gothic", 14))
activity_label_title.pack(anchor="w", padx=25, pady=(10, 2))
activity_value_label = CTkLabel(contents_frame, text="Moderate", font=("Century Gothic", 16, "bold"))
activity_value_label.pack(anchor="w", padx=25, pady=(0, 4))

different_activitylevel_names = ["Minimal", "Light", "Moderate", "Very Active"]

def activity_slider(number_of_steps):
    rounded_position = int(round(float(number_of_steps)))
    activity_slider.set(rounded_position)
    activity_value_label.configure(text=different_activitylevel_names[rounded_position])

activity_slider = CTkSlider(contents_frame, from_=0, to=3, number_of_steps=3, command=activity_slider, width=300)
activity_slider.set(2)  # default slider set to moderate
activity_slider.pack(anchor="w", padx=25, pady=(0, 5))

macro_calc.mainloop()
