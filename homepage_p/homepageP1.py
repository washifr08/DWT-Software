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
    user_email = "test"

# creates box and size and title
homepage = CTk()
homepage.geometry("1000x600")
homepage.title("D.W.T Homepage")

# set base background (subtle contrast between modes)
set_default_color_theme("green")
homepage.configure(fg_color=("gray85", "#101010"))  # light bg | dark bg

# finds width and height of screen
screen_width = homepage.winfo_screenwidth()
screen_height = homepage.winfo_screenheight()

# calculates x and y coordinates for the window to be centered
centre_x = int((screen_width - 1000) / 2)
centre_y = int((screen_height - 800) / 2)

# sets the position of the window to be centered
homepage.geometry(f"+{centre_x}+{centre_y}")

# top header bar with app title and dark/light toggle
header_bar = CTkFrame(homepage, fg_color=("gray70", "#1c1c1c"), height=50, corner_radius=0)
header_bar.pack(fill="x", side="top")

header_title = CTkLabel(header_bar, text="Digital Wellbeing Tracker",
                        font=("Century Gothic", 22, "bold"))
header_title.pack(side="left", padx=20)


def dark_light_toggle():  # dark/light mode toggle function as used in signup page
    theme_state = get_appearance_mode()

    if theme_state == "Dark":
        # Switch to improved light mode
        set_appearance_mode("light")

        homepage.configure(fg_color="gray85")          
        header_bar.configure(fg_color="gray70")      
        mainpage_frame.configure(fg_color="white")     
        footer.configure(text_color="#505050")         

    else:
        # Switch to restored original dark mode
        set_appearance_mode("dark")

        homepage.configure(fg_color="#101010")         
        header_bar.configure(fg_color="#1c1c1c")       
        mainpage_frame.configure(fg_color="#1c1c1c")   
        footer.configure(text_color="#A0A0A0")         


theme_switch = CTkSwitch(header_bar, text="Dark / Light Mode", command=dark_light_toggle)
theme_switch.pack(side="right", padx=20, pady=10)

# main frame for the homepage
mainpage_frame = CTkFrame(homepage, fg_color=("white", "#1c1c1c"), corner_radius=25)
mainpage_frame.pack(pady=(30, 20), padx=30, fill=BOTH, expand=True)

# welcome text
my_text = CTkLabel(mainpage_frame,
                   text=f"Welcome to the\nDigital Wellbeing Tracker\n{user_name}!",
                   font=("Century Gothic", 48, "bold"),
                   text_color="#4CAF50")
my_text.pack(anchor="n", pady=(40, 5))

# subtitle line under welcome text
subtitle = CTkLabel(mainpage_frame,
                    text="Track your nutrition, mood and sleep all in one place.",
                    font=("Century Gothic", 18),
                    text_color=("#404040", "#A0A0A0"))
subtitle.pack(anchor="n", pady=(0, 30))

# frame to hold both buttons evenly spaced
button_frame = CTkFrame(mainpage_frame, fg_color="transparent")
button_frame.pack(expand=True)

# optional icons beside buttons (replace with your own image paths if desired)
try:
    macro_icon = CTkImage(light_image=Image.open("apple.png"), dark_image=Image.open("apple.png"), size=(40, 40))
    mood_icon = CTkImage(light_image=Image.open("moon.png"), dark_image=Image.open("moon.png"), size=(40, 40))
except:
    macro_icon = None
    mood_icon = None

# button to macro nutritional tracker
macro_nutritional = CTkButton(master=button_frame,
                              text=" Macro\nNutritional\nTracker",
                              image=macro_icon,
                              compound="left",
                              font=("Century Gothic", 30, "bold"),
                              text_color="#000000",
                              fg_color="#4CAF50",
                              hover_color="#3E803F",
                              border_color="#000000",
                              border_width=3.5,
                              corner_radius=30,
                              width=350,
                              height=150)

# button to mood and sleep tracker
mood_sleep = CTkButton(master=button_frame,
                       text=" Mood\nand\nSleep Tracker",
                       image=mood_icon,
                       compound="left",
                       font=("Century Gothic", 30, "bold"),
                       text_color="#000000",
                       fg_color="#4CAF50",
                       hover_color="#3E803F",
                       border_color="#000000",
                       border_width=3.5,
                       corner_radius=30,
                       width=350,
                       height=150)

# place buttons side by side
macro_nutritional.pack(side="left", padx=60, pady=20)
mood_sleep.pack(side="left", padx=60, pady=20)

# footer placed neatly BELOW the main frame (outside it but with spacing)
footer = CTkLabel(homepage,
                  text="© 2025 Digital Wellbeing Tracker | All Rights Reserved",
                  font=("Century Gothic", 11),
                  text_color=("#505050", "#A0A0A0"))
footer.pack(side="bottom", pady=(0, 10))

homepage.mainloop()
