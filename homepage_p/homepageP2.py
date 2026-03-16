from customtkinter import *  # ctk library
from PIL import Image  # pillow for image importing
from tkinter import messagebox  # messagebox funtionality for errors
from openpyxl import *  # allows interractions with excel
import os  # allows saving files to device
import sys  # allows for sys.exit() function

# get the passed arguments from signup page
if len(sys.argv) >= 3:
    user_name = sys.argv[1]
    user_email = sys.argv[2]
else:
    user_name = "User"
    user_email = ""

# creates box and size and title
homepage = CTk()
homepage.geometry("1000x600")
homepage.title("")

# set base background for contrast
set_default_color_theme("green")
homepage.configure(fg_color=("gray75", "#1A1A1A"))  # light bg and dark bg

# finds width and height of screen
screen_width = homepage.winfo_screenwidth()
screen_height = homepage.winfo_screenheight()

# calculates x and y coordinates for the window to be centered
centre_x = int((screen_width - 1000) / 2)
centre_y = int((screen_height - 800) / 2)

# sets the position of the window to be centered
homepage.geometry(f"+{centre_x}+{centre_y}")

# top bar frame for app title and dark/light toggle
header_bar = CTkFrame(homepage, fg_color=("gray90", "#212121"), height=50, corner_radius=0)
header_bar.pack(fill="both", side="top")

# app title on the left 
header_title = CTkLabel(header_bar, text="Digital Wellbeing Tracker", font=("Century Gothic", 22, "bold"))
header_title.pack(side="left", padx=20)

def dark_light_toggle():  # dark/light mode toggle function as used in signup page
    theme_state = get_appearance_mode()
    if theme_state == "Dark":
        set_appearance_mode("light")
        apply_light_mode()
    else:
        set_appearance_mode("dark")
        apply_dark_mode()

# dark/light mode toggle on the right
theme_switch = CTkSwitch(header_bar, text="Dark / Light Mode", command=dark_light_toggle)
theme_switch.pack(side="right", padx=20, pady=10)

# main frame for the homepage content
mainpage_frame = CTkFrame(homepage, fg_color=("gray90", "#212121"), bg_color=("gray75", "#1A1A1A"),height= 100, corner_radius=25)
mainpage_frame.pack( fill="both", expand=True, pady=(35, 20), padx=30)

# welcome text uncluding user's name
my_text = CTkLabel(mainpage_frame, text=f"Welcome to the\nDigital Wellbeing Tracker\n{user_name}!",
                   font=("Century Gothic", 48, "bold"), text_color="#4CAF50")
my_text.pack(anchor="n", pady=(40, 5))

# subtitle line under welcome text
subtitle = CTkLabel(mainpage_frame,
                    text="Track your nutrition, mood and sleep all in one place.",
                    font=("Century Gothic", 18),
                    text_color=("#404040", "#A0A0A0"))
subtitle.pack(anchor="n", pady=(0, 30))

# button to macro nutritional tracker
macro_nutritional = CTkButton(master=mainpage_frame, text=" Macro\nNutritional\nTracker", compound="left", 
                              font=("Century Gothic", 30, "bold"), text_color="#000000",
                              fg_color="#4CAF50", hover_color="#3E803F", border_color="#000000",
                              border_width=3.5, corner_radius=30, width=350, height=150)

# button to mood and sleep tracker
mood_sleep = CTkButton(master=mainpage_frame, text=" Mood\nand\nSleep Tracker", compound="left", 
                       font=("Century Gothic", 30, "bold"), text_color="#000000",
                       fg_color="#4CAF50", hover_color="#3E803F", border_color="#000000", 
                       border_width=3.5, corner_radius=30, width=350, height=150)

# place buttons side by side
macro_nutritional.pack(side="left", padx=60, pady=20)
mood_sleep.pack(side="left", padx=60, pady=20)

# frame placed below the main frame 
footer = CTkLabel(homepage, text="© 2025 Digital Wellbeing Tracker | All Rights Reserved",
                  font=("Century Gothic", 11), text_color=("#505050", "#A0A0A0"))
footer.pack(side="bottom", pady=(0, 20))

# function to apply light mode colors to frames
def apply_light_mode():
    homepage.configure(fg_color="gray75")
    header_bar.configure(fg_color="gray90")
    mainpage_frame.configure(fg_color="gray90", bg_color="gray75")
    footer.configure(text_color="#505050")

# function to apply dark mode colors to frames
def apply_dark_mode():
    homepage.configure(fg_color="#1A1A1A")
    header_bar.configure(fg_color="#212121")
    mainpage_frame.configure(fg_color="#212121", bg_color="#1A1A1A")
    footer.configure(text_color="#A0A0A0")
 
if get_appearance_mode() == "Dark":
    apply_dark_mode()
else:
    apply_light_mode()

homepage.mainloop()
