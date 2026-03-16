from customtkinter import *  
from PIL import Image 
from tkinter import messagebox  
from openpyxl import *  
import os  
import sys
import subprocess  

moodnsleep = CTk()
moodnsleep.geometry("1200x800")
moodnsleep.title("D.W.T - Mood and Sleep Tracker")

screen_width = moodnsleep.winfo_screenwidth()
screen_height = moodnsleep.winfo_screenheight()

centre_x = int((screen_width - 1200) / 2)
centre_y = int((screen_height - 1000) / 2)

moodnsleep.geometry(f"+{centre_x}+{centre_y}")

header = CTkFrame(moodnsleep, fg_color=("gray90", "#212121"), height=50, corner_radius=0)
header.pack(fill="both", side="top")

header_title = CTkLabel(header, text="Digital Wellbeing Tracker", font=("Century Gothic", 22, "bold"))
header_title.pack(side="left", padx=20)

def dark_light_toggle(): 
    theme_state = get_appearance_mode()
    if theme_state == "Dark":
        set_appearance_mode("light")
        set_all_light()
    else:
        set_appearance_mode("dark")
        set_all_dark()

theme_switch = CTkSwitch(header, text="Dark / Light Mode",font=("Century Gothic", 14), command=dark_light_toggle)
theme_switch.pack(side="right", padx=20, pady=10)

contents_frame = CTkFrame(moodnsleep, fg_color=("gray95", "#212121"),height= 200, corner_radius=25)
contents_frame.pack( fill="both", expand=True, pady=(35, 20), padx=30)

def set_all_light():
    moodnsleep.configure(fg_color="gray85")
    header.configure(fg_color="gray95")
    contents_frame.configure(fg_color="gray95")

def set_all_dark():
    moodnsleep.configure(fg_color="#1A1A1A")
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

moodnsleep.mainloop()