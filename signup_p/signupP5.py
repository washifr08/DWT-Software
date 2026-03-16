from customtkinter import *
from tkinter import messagebox
from PIL import Image
import re
from openpyxl import *
import hashlib
import os

# creates signup window in which everything will be placed, sets size and changes title
signup_page = CTk()
signup_page.geometry("420x480")
signup_page.title("D.W.T Welcome Page")

# creates signup and login frames
signup_frame = CTkFrame(signup_page)
login_frame = CTkFrame(signup_page)

frame_status = "signup"  # variable to track which frame is currently displayed

# creates excel file for registered users
excel_file = "registered_users.xlsx"
if not os.path.exists(excel_file):
    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Email", "Password"])
    wb.save(excel_file)

# simple regular expression to check if email is in valid format
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# signup function
def signup():
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    terms_check = terms_checkbox.get()

    if not name or not email or not password:
        messagebox.showwarning("Empty", "Please fill in all the fields")
        return
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address")
        return
    if not terms_check:
        messagebox.showwarning("Terms Not Agreed", "You must agree to the terms to sign up")
        return

    wb = load_workbook(excel_file)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if email == row[1]:
            messagebox.showerror("Error", "Email already registered. Please use a different email.")
            return

    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    ws.append([name, email, encrypted_password])
    wb.save(excel_file)
    wb.close()

    messagebox.showinfo("Success", "Go ahead and login now!")
    name_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    password_entry.delete(0, 'end')
    terms_checkbox.deselect()
    login_form()

# navigation functions
def login_form():
    global frame_status
    signup_frame.pack_forget()
    login_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    frame_status = "login"

def back_to_signup_form():
    global frame_status
    login_frame.pack_forget()
    signup_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    frame_status = "signup"

# dark/light mode toggle
def dark_light_toggle():
    theme_state = get_appearance_mode()
    if theme_state == "Dark":
        set_appearance_mode("light")
    else:
        set_appearance_mode("dark")

# dark/light mode switch
theme_switch = CTkSwitch(signup_page, text="Dark / Light Mode", command=dark_light_toggle)
theme_switch.pack(anchor="ne", padx=10, pady=10)

# image setup
_original_profile_image = Image.open("greenprofile.png").convert("RGBA")
CTK_IMG_SMALL = CTkImage(light_image=_original_profile_image, dark_image=_original_profile_image, size=(100, 100))

# signup image
profile_label = CTkLabel(signup_frame, text="", image=CTK_IMG_SMALL)
profile_label.image = CTK_IMG_SMALL
profile_label.pack(pady=(10, 15))

# login image
login_profile_label = CTkLabel(login_frame, text="", image=CTK_IMG_SMALL)
login_profile_label.image = CTK_IMG_SMALL
login_profile_label.pack(pady=(10, 15))

# signup page widgets
name_entry = CTkEntry(signup_frame, placeholder_text="Username", width=275, height=30,
                      border_width=2, corner_radius=10, font=("Lexend Deca", 16))
email_entry = CTkEntry(signup_frame, placeholder_text="Email", width=275, height=30,
                       border_width=2, corner_radius=10, font=("Lexend Deca", 16))
password_entry = CTkEntry(signup_frame, placeholder_text="Password", width=275, height=30,
                          border_width=2, corner_radius=10, font=("Lexend Deca", 16), show="*")
terms_checkbox = CTkCheckBox(signup_frame, text="I agree to give an A* to this student",
                             width=275, height=30, font=("Lexend Deca", 12))
signup_button = CTkButton(master=signup_frame, text="Start Your Wellbeing Journey!", corner_radius=20,
                           font=("Lexend Deca", 20, "bold"), fg_color="#4CAF50",
                           hover_color="#3E803F", border_color="#000000", border_width=3.5,
                           text_color="#000000", command=signup)
login_button = CTkButton(master=signup_frame, text="Already have an account? Log in here.",
                         corner_radius=10, font=("Lexend Deca", 12, "underline"),
                         fg_color="transparent", hover_color="#3c6833", border_color="#000000",
                         border_width=0, text_color="#ffffff", command=login_form)

# login page widgets
email_entry_login = CTkEntry(login_frame, placeholder_text="Email", width=275, height=30,
                             border_width=2, corner_radius=10, font=("Lexend Deca", 16))
password_entry_login = CTkEntry(login_frame, placeholder_text="Password", width=275, height=30,
                                border_width=2, corner_radius=10, font=("Lexend Deca", 16), show="*")
signup_button_login = CTkButton(master=login_frame, text="Resume Your Wellbeing Journey!",
                                corner_radius=20, font=("Lexend Deca", 20, "bold"),
                                fg_color="#4CAF50", hover_color="#3E803F", border_color="#000000",
                                border_width=3.5, text_color="#000000")
back_to_signup_button = CTkButton(master=login_frame,
                                  text="Want to go back and create a new account? \nSignup here!",
                                  corner_radius=10, font=("Lexend Deca", 12, "underline"),
                                  fg_color="transparent", hover_color="#3c6833", border_color="#000000",
                                  border_width=0, text_color="#ffffff", command=back_to_signup_form)

# signup layout
name_entry.pack(pady=(5, 0))
email_entry.pack(pady=(10, 0))
password_entry.pack(pady=(10, 0))
terms_checkbox.pack(pady=(20, 0), padx=(50, 0))
signup_button.pack(pady=(20, 0))
login_button.pack(pady=(20, 0))

# login layout
email_entry_login.pack(pady=(20, 0))
password_entry_login.pack(pady=(10, 0))
signup_button_login.pack(pady=(35, 0))
back_to_signup_button.pack(pady=(20, 0))

# show signup frame by default
signup_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

# center window
screen_width = signup_page.winfo_screenwidth()
screen_height = signup_page.winfo_screenheight()
centre_x = int((screen_width - 420) / 2)
centre_y = int((screen_height - 680) / 2)
signup_page.geometry(f"+{centre_x}+{centre_y}")

signup_page.mainloop()
