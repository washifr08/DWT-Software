from customtkinter import * 
import sys 
import subprocess  

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
homepage.title("D.W.T - Home Page")

# set background for contrast
set_default_color_theme("green")
homepage.configure(fg_color=("gray85", "#1A1A1A"))  # light and dark colours

# finds width and height of screen
screen_width = homepage.winfo_screenwidth()
screen_height = homepage.winfo_screenheight()

# calculates x and y coordinates for the window to be centered
centreofx = int((screen_width - 1000) / 2)
centreofy = int((screen_height - 800) / 2)

# sets the position of the window to be centered
homepage.geometry(f"+{centreofx}+{centreofy}")

# top bar fram for app title and dark/light toggle
header_frame = CTkFrame(homepage, fg_color=("gray95", "#212121"), height=50, corner_radius=0)
header_frame.pack(fill="both", side="top")

# app title on the left 
app_title = CTkLabel(header_frame, text="Digital Wellbeing Tracker", font=("Century Gothic", 22, "bold"))
app_title.pack(side="left", padx=20)

def dark_light_toggle():  # dark/light mode toggle function as used in signup page
    theme_state = get_appearance_mode()
    if theme_state == "Dark":
        set_appearance_mode("light")
        set_all_light()
    else:
        set_appearance_mode("dark")
        set_all_dark()

# dark/light mode toggle on the right
theme_switch = CTkSwitch(header_frame, text="Dark / Light Mode", font=("Century Gothic", 14), command=dark_light_toggle)
theme_switch.pack(side="right", padx=20, pady=10)

# main frame for the homepage content
contents_frame = CTkFrame(homepage, fg_color=("gray95", "#212121"),height= 200, corner_radius=25)
contents_frame.pack( fill="both", expand=True, pady=(35, 20), padx=30)

# welcome text uncluding user's name
welcome_text = CTkLabel(contents_frame, text=f"Welcome to the\nDigital Wellbeing Tracker\n{user_name}!",
                   font=("Century Gothic", 48, "bold"), text_color="#4CAF50")
welcome_text.pack(anchor="n", pady=(40, 5))

# mini info line under welcome text
mini_info = CTkLabel(contents_frame,
                    text="Track your nutrition, mood and sleep all in one place.",
                    font=("Century Gothic", 18),
                    text_color=("#404040", "#A0A0A0"))
mini_info.pack(anchor="n", pady=(0, 30))

def macro_nutrition_page():
    homepage.after(100, homepage.destroy)
    subprocess.Popen([sys.executable, "macro_calc.py", user_name,user_email])  # opens macro nutrition page

# button to macro nutritional tracker
macro_nutritional = CTkButton(master=contents_frame, text=" Macro\nNutritional\nTracker", 
                              font=("Century Gothic", 30, "bold"), text_color="#000000",
                              fg_color="#4CAF50", hover_color="#3E803F", border_color="#000000",
                              border_width=3.5, corner_radius=30, width=350, height=150, command=macro_nutrition_page)

def mood_sleep_page():
    homepage.after(100, homepage.destroy)
    subprocess.Popen([sys.executable, "moodnsleep.py", user_name, user_email])  # opens mood and sleep tracker page

# button to mood and sleep tracker
mood_sleep = CTkButton(master=contents_frame, text=" Mood\nand\nSleep Tracker", 
                       font=("Century Gothic", 30, "bold"), text_color="#000000",
                       fg_color="#4CAF50", hover_color="#3E803F", border_color="#000000", 
                       border_width=3.5, corner_radius=30, width=350, height=150, command=mood_sleep_page)

# place buttons side by side
macro_nutritional.pack(side="left", padx=60, pady=20)
mood_sleep.pack(side="left", padx=60, pady=20)

# copyright text at the bottom
copyright = CTkLabel(homepage, text="© 2025 Digital Wellbeing Tracker | All Rights Reserved",
                  font=("Century Gothic", 11), text_color=("#505050", "#A0A0A0"))
copyright.pack(side="bottom", pady=(0, 20))

# function to apply light mode colors to frames
def set_all_light():
    homepage.configure(fg_color="gray85")
    header_frame.configure(fg_color="gray95")
    contents_frame.configure(fg_color="gray95")
    copyright.configure(text_color="#505050")

# function to apply dark mode colors to frames
def set_all_dark():
    homepage.configure(fg_color="#1A1A1A")
    header_frame.configure(fg_color="#212121")
    contents_frame.configure(fg_color="#212121")
    copyright.configure(text_color="#A0A0A0")
 
if get_appearance_mode() == "Dark":
    set_all_dark()
else:
    set_all_light()

homepage.mainloop()
