from customtkinter import *  # ctk library
from PIL import Image  # pillow for image importing
from tkinter import messagebox  # messagebox funtionality for errors
from openpyxl import *  # allows interractions with excel
import os  # allows saving files to device
import sys  # allows for sys.exit() function
import subprocess  # allows opening of new python files
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    
    update_chart_theme()

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

def update_chart_theme():
    global chart_drawn
    if get_appearance_mode() == "Dark":
        fig.patch.set_facecolor("#212121")
        ax.set_facecolor("#212121")
        title_color = "white"
        text_color = "white"
    else:
        fig.patch.set_facecolor("#f2f2f2")
        ax.set_facecolor("#f2f2f2")
        title_color = "black"
        text_color = "black"

    # update title + labels if chart already exists
    if chart_drawn:
        ax.set_title("Macros (g)", color=title_color, fontfamily="Century Gothic", fontsize=14)
        for text in ax.texts:
            text.set_color(text_color)
    else:
        ax.set_title("")

    canvas.draw()

# change to dark or light mode based on current setting
if get_appearance_mode() == "Dark":
    set_all_dark()
else:
    set_all_light()

# retrieve passed email for use for database later
if len(sys.argv) >= 2:
    user_email = sys.argv[1]
else:
    user_email = ""

# top-centre title inside contents_frame
title_label = CTkLabel(contents_frame, text="Your personalised Macro Nutritional Calculator",
                       font=("Century Gothic", 30, "bold"), text_color="#4CAF50")
title_label.place(relx=0.5, y=18, anchor="n")

# buttons for entering user data on the left side of the screen
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
weight_change_entry = CTkEntry(contents_frame, placeholder_text="e.g. 0.5 or -0.5", width=300, height=36,
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
    activity_slider_bar.set(rounded_position)
    activity_value_label.configure(text=different_activitylevel_names[rounded_position])

activity_slider_bar = CTkSlider(contents_frame, from_=0, to=3, number_of_steps=3, command=activity_slider, width=300)
activity_slider_bar.set(2) 
activity_slider_bar.pack(anchor="w", padx=25, pady=(0, 5))

# pie chart container on the top right
chart_frame = CTkFrame(contents_frame, fg_color=("gray95", "#212121"), corner_radius=20, width=520, height=320)
chart_frame.place(x=480, y=95)  

# text under chart on the right
macro_text_frame = CTkFrame(contents_frame, fg_color=("gray95", "#212121"), corner_radius=20, width=520, height=220)
macro_text_frame.place(x=600, y=430)

macro_text_title = CTkLabel(macro_text_frame, text="Macro Results", font=("Century Gothic", 20, "bold"), text_color="#4CAF50")
macro_text_title.pack(pady=(15, 5))

macro_results_label = CTkLabel(
    macro_text_frame,
    text="Fill in your details and click 'Calculate your macros!'.",
    font=("Century Gothic", 16),
    justify="center")
macro_results_label.pack(padx=30, pady=(5, 10))

# create the matplotlib figure and embed it
fig = Figure(figsize=(5.2, 3.2), dpi=100)
ax = fig.add_subplot(111)

chart_drawn = False

# make matplotlib chart match dark mode

# figure background
fig.patch.set_facecolor("#212121")     
# axes background
ax.set_facecolor("#212121")            

canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)

# invisible placeholder pie chart at start
ax.clear()
ax.set_facecolor("#1F1F1F")
# hides all borders, ticks, grid, etc.
ax.axis("off")
canvas.draw()

def calculate_macros():
    try:
        # basic input validation
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        age = float(age_entry.get())
        weight_change = float(weight_change_entry.get())
    except:
        # error message if inputs are invalid
        messagebox.showerror("Input Error", "Please make sure all inputs are filled in correctly.")
        return

    # Mifflin-St Jeor calculations
    if user_algorithm.get() == "Mifflin-St Jeor":
        if user_sex.get() == "Male":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            if activity_value_label.cget("text") == "Minimal":
                tdee = bmr * 1.2
            elif activity_value_label.cget("text") == "Light":
                tdee = bmr * 1.375
            elif activity_value_label.cget("text") == "Moderate":
                tdee = bmr * 1.55
            else:
                tdee = bmr * 1.725
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
            if activity_value_label.cget("text") == "Minimal":
                tdee = bmr * 1.2
            elif activity_value_label.cget("text") == "Light":
                tdee = bmr * 1.375
            elif activity_value_label.cget("text") == "Moderate":
                tdee = bmr * 1.55
            else:
                tdee = bmr * 1.725

    # Katch-McArdle calculations
    else:  
        if user_sex.get() == "Male":
            lbm = (0.407 * weight) + (0.267 * height) - 19.2
            bmr = 370 + (21.6 * lbm)
            if activity_value_label.cget("text") == "Minimal":
                tdee = bmr * 1.2
            elif activity_value_label.cget("text") == "Light":
                tdee = bmr * 1.375
            elif activity_value_label.cget("text") == "Moderate":
                tdee = bmr * 1.55
            else:
                tdee = bmr * 1.725
        else:
            lbm = (0.252 * weight) + (0.473 * height) - 48.3
            bmr = 370 + (21.6 * lbm)
            if activity_value_label.cget("text") == "Minimal":
                tdee = bmr * 1.2
            elif activity_value_label.cget("text") == "Light":
                tdee = bmr * 1.375
            elif activity_value_label.cget("text") == "Moderate":
                tdee = bmr * 1.55
            else:
                tdee = bmr * 1.725

    # calculate daily caloric needs including weight change
    # 7700 calories per kg of fat
    surplus_deficit = (weight_change * 7700) / 7  
    daily_caloric_needs = tdee + surplus_deficit

    # 2 grams of protein per kg of body weight
    protein_intake = weight * 2  
    # 28% of calories from fat, 9 calories per gram
    fat_intake = (0.28 * daily_caloric_needs) / 9  
    carb_intake = daily_caloric_needs - ((protein_intake * 4) + (fat_intake * 9))
    # 4 calories per gram of carbohydrate
    carb_intake = carb_intake / 4  

    # update the text under the pie chart 
    macro_results_label.configure(text=
        f"Daily calories: {int(daily_caloric_needs)} kcal\n\n"
        f"Protein: {int(protein_intake)} g\n"
        f"Fats: {int(fat_intake)} g\n"
        f"Carbohydrates: {int(carb_intake)} g")

    # update the pie chart with new values
    values = [protein_intake, fat_intake, carb_intake]
    labels = ["Protein", "Fats", "Carbs"]

    # safety avoid errors if something weird happens
    values = [max(0, float(v)) for v in values]
    if sum(values) == 0:
        ax.clear()
        ax.set_title("Macros (grams)")
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center")
        canvas.draw()
        return

    ax.clear()
    #keep background dark after clear
    ax.set_facecolor("#212121")  

    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90,
        textprops={"color": "white", "fontfamily": "Century Gothic", "fontsize": 14})  # make labels white and sets century gothic font

    ax.set_title("Macros (g)", color="white", fontfamily="Century Gothic", fontsize=14)  # title white and century gothic
    ax.axis("equal")
    canvas.draw()

    global chart_drawn
    chart_drawn = True

    update_chart_theme()

# function to handle calculate button presses
btn_pressed = False
def calculate_button_pressed():
    global btn_pressed 
    btn_pressed = True
    calculate_macros()
    if btn_pressed==True:
        view_progress_btn.pack(anchor="w", padx=65, pady=(30, 6))
    else:
        pass

calculate_btn = CTkButton(contents_frame, text="Calculate your macros!",
                        corner_radius=25, font=("Century Gothic", 16),
                        fg_color="#4CAF50", hover_color="#3E803F",
                        border_color="#000000", border_width=2,
                        text_color="#000000", command=calculate_button_pressed)
calculate_btn.pack(anchor="w", padx=65, pady=(20, 6))

view_progress_btn = CTkButton(macro_text_frame, text="View Past Progress",
                        corner_radius=25, font=("Century Gothic", 16),
                        fg_color="#4CAF50", hover_color="#3E803F",
                        border_color="#000000", border_width=2,
                        text_color="#000000")

macro_calc.mainloop()
