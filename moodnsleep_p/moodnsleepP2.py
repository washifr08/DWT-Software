from customtkinter import *
from tkinter import messagebox
from datetime import datetime
import sys
import subprocess

moodnsleep = CTk()
moodnsleep.geometry("1200x800")
moodnsleep.title("D.W.T - Mood and Sleep Tracker")

set_default_color_theme("green")

screen_width = moodnsleep.winfo_screenwidth()
screen_height = moodnsleep.winfo_screenheight()

centre_x = int((screen_width - 1200) / 2)
centre_y = int((screen_height - 1000) / 2)

moodnsleep.geometry(f"+{centre_x}+{centre_y}")

if len(sys.argv) >= 2:
    user_email = sys.argv[1]
else:
    user_email = "test"

header = CTkFrame(moodnsleep, fg_color=("gray90", "#212121"), height=50, corner_radius=0)
header.pack(fill="both", side="top")

header_title = CTkLabel(header, text="Digital Wellbeing Tracker", font=("Century Gothic", 22, "bold"))
header_title.pack(side="left", padx=20)

contents_frame = CTkFrame(moodnsleep, fg_color=("gray95", "#212121"), height=200, corner_radius=25)
contents_frame.pack(fill="both", expand=True, pady=(25, 20), padx=30)

def set_all_light():
    moodnsleep.configure(fg_color="gray85")
    header.configure(fg_color="gray95")
    contents_frame.configure(fg_color="gray95")

def set_all_dark():
    moodnsleep.configure(fg_color="#1A1A1A")
    header.configure(fg_color="#212121")
    contents_frame.configure(fg_color="#212121")

def dark_light_toggle():
    theme_state = get_appearance_mode()
    if theme_state == "Dark":
        set_appearance_mode("light")
        set_all_light()
    else:
        set_appearance_mode("dark")
        set_all_dark()

theme_switch = CTkSwitch(header, text="Dark / Light Mode", font=("Century Gothic", 14), command=dark_light_toggle)
theme_switch.pack(side="right", padx=20, pady=10)

if get_appearance_mode() == "Dark":
    set_all_dark()
else:
    set_all_light()

date_today = datetime.now().strftime("%Y-%m-%d")

title_label = CTkLabel(contents_frame, text="Mood & Sleep Tracker",
                       font=("Century Gothic", 30, "bold"), text_color="#4CAF50")
title_label.place(relx=0.5, y=18, anchor="n")

date_label = CTkLabel(contents_frame, text=f"Entry Date: {date_today}",
                      font=("Century Gothic", 16))
date_label.pack(anchor="w", padx=25, pady=(70, 4))

mood_entry_text = CTkLabel(contents_frame, text="Mood (1–10)", font=("Century Gothic", 14))
mood_entry_text.pack(anchor="w", padx=25, pady=(16, 2))

mood_value_label = CTkLabel(contents_frame, text="5", font=("Century Gothic", 16, "bold"))
mood_value_label.pack(anchor="w", padx=25, pady=(0, 4))

def mood_slider_changed(v):
    mood_value_label.configure(text=str(int(v)))

mood_slider = CTkSlider(contents_frame, from_=1, to=10, number_of_steps=9, command=mood_slider_changed, width=300)
mood_slider.set(5)
mood_slider.pack(anchor="w", padx=25, pady=(0, 5))

sleep_time_title = CTkLabel(contents_frame, text="Sleep time", font=("Century Gothic", 14))
sleep_time_title.pack(anchor="w", padx=25, pady=(14, 2))

times_h = [f"{i:02d}" for i in range(24)]
times_m = [f"{i:02d}" for i in range(0, 60, 5)]

bed_label = CTkLabel(contents_frame, text="Bed time", font=("Century Gothic", 14))
bed_label.pack(anchor="w", padx=25, pady=(6, 2))

bed_row = CTkFrame(contents_frame, fg_color="transparent")
bed_row.pack(anchor="w", padx=25, pady=(0, 6))

bed_hour_var = StringVar(value="23")
bed_minute_var = StringVar(value="00")

bed_hour_menu = CTkOptionMenu(bed_row, values=times_h, variable=bed_hour_var,
                           width=140, height=36, corner_radius=10,
                           font=("Century Gothic", 16), fg_color="#469E4A",
                           button_color="#3D8B40", button_hover_color="#2F5F30",
                           text_color="#000000")
bed_hour_menu.pack(side="left", padx=(0, 10))

bed_minute_menu = CTkOptionMenu(bed_row, values=times_m, variable=bed_minute_var,
                           width=140, height=36, corner_radius=10,
                           font=("Century Gothic", 16), fg_color="#469E4A",
                           button_color="#3D8B40", button_hover_color="#2F5F30",
                           text_color="#000000")
bed_minute_menu.pack(side="left")

wake_label = CTkLabel(contents_frame, text="Wake time", font=("Century Gothic", 14))
wake_label.pack(anchor="w", padx=25, pady=(10, 2))

wake_row = CTkFrame(contents_frame, fg_color="transparent")
wake_row.pack(anchor="w", padx=25, pady=(0, 10))

wake_hour_var = StringVar(value="07")
wake_minute_var = StringVar(value="00")

wake_hour_menu = CTkOptionMenu(wake_row, values=times_h, variable=wake_hour_var,
                            width=140, height=36, corner_radius=10,
                            font=("Century Gothic", 16), fg_color="#469E4A",
                            button_color="#3D8B40", button_hover_color="#2F5F30",
                            text_color="#000000")
wake_hour_menu.pack(side="left", padx=(0, 10))

wake_minute_menu = CTkOptionMenu(wake_row, values=times_m, variable=wake_minute_var,
                            width=140, height=36, corner_radius=10,
                            font=("Century Gothic", 16), fg_color="#469E4A",
                            button_color="#3D8B40", button_hover_color="#2F5F30",
                            text_color="#000000")
wake_minute_menu.pack(side="left")

sleep_quality_label = CTkLabel(contents_frame, text="Sleep quality (1–5)", font=("Century Gothic", 14))
sleep_quality_label.pack(anchor="w", padx=25, pady=(6, 2))

sleep_quality_var = StringVar(value="3")
sleep_quality_menu = CTkOptionMenu(contents_frame, values=["1", "2", "3", "4", "5"], variable=sleep_quality_var,
                                   width=300, height=36, corner_radius=10,
                                   font=("Century Gothic", 16), fg_color="#469E4A",
                                   button_color="#3D8B40", button_hover_color="#2F5F30",
                                   text_color="#000000")
sleep_quality_menu.pack(anchor="w", padx=25, pady=(0, 5))

notes_label = CTkLabel(contents_frame, text="Notes (optional)", font=("Century Gothic", 14))
notes_label.pack(anchor="w", padx=25, pady=(12, 2))

notes_box = CTkTextbox(contents_frame, height=95, width=300)
notes_box.pack(anchor="w", padx=25, pady=(0, 10))

def save_ui():
    messagebox.showinfo("UI Only", "This screen is UI-only right now. Saving will be added next.")

def view_ui():
    messagebox.showinfo("UI Only", "Weekly insights + graphs will be added next.")

save_btn = CTkButton(contents_frame, text="Save Today's Entry",
                     corner_radius=25, font=("Century Gothic", 16),
                     fg_color="#4CAF50", hover_color="#3E803F",
                     border_color="#000000", border_width=2,
                     text_color="#000000", command=save_ui, width=300, height=44)
save_btn.pack(anchor="w", padx=25, pady=(12, 10))

view_btn = CTkButton(contents_frame, text="View Weekly Insights",
                     corner_radius=25, font=("Century Gothic", 16),
                     fg_color="#4CAF50", hover_color="#3E803F",
                     border_color="#000000", border_width=2,
                     text_color="#000000", command=view_ui, width=260, height=44)
view_btn.place(relx=0.7, rely=0.87, anchor="center")

right_top_frame = CTkFrame(contents_frame, fg_color=("gray95", "#212121"), corner_radius=20, width=520, height=320)
right_top_frame.place(relx=0.7, y=120, anchor="n")

right_top_title = CTkLabel(right_top_frame, text="Today’s Overview",
                           font=("Century Gothic", 20, "bold"), text_color="#4CAF50")
right_top_title.pack(pady=(15, 8))

overview_text = CTkLabel(right_top_frame,
                         text="Sleep hours and trends will appear here.\n\n"
                              "Later, this section can show:\n"
                              "• Sleep duration\n"
                              "• Sleep quality\n"
                              "• Mood score",
                         font=("Century Gothic", 16), justify="center")
overview_text.pack(padx=30, pady=(5, 10))

right_bottom_frame = CTkFrame(contents_frame, fg_color=("gray95", "#212121"), corner_radius=20, width=520, height=220)
right_bottom_frame.place(relx=0.7, y=375, anchor="n")

right_bottom_title = CTkLabel(right_bottom_frame, text="Patterns & Insights",
                              font=("Century Gothic", 20, "bold"), text_color="#4CAF50")
right_bottom_title.pack(pady=(0, 8))

insight_text = CTkLabel(right_bottom_frame,
                        text="This area will compare wellbeing with progress.\n\n"
                             "Examples for your NEA:\n"
                             "• Mood vs sleep quality\n"
                             "• Sleep vs weekly weight trend",
                        font=("Century Gothic", 16), justify="center")
insight_text.pack(padx=30, pady=(5, 10))

moodnsleep.mainloop()
