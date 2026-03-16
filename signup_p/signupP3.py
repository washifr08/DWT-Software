from customtkinter import *
from PIL import Image

signup_page = CTk()
signup_page.geometry("420x480")
signup_page.title("D.W.T Welcome Page")

def dark_light_toggle():
    theme_state = get_appearance_mode()
    if theme_state == "Dark":
        set_appearance_mode("light")
    else:
        set_appearance_mode("dark")

theme_switch = CTkSwitch(signup_page, text="Dark / Light Mode", command=dark_light_toggle)
theme_switch.pack(anchor="ne", padx=10, pady=10)

signup_frame = CTkFrame(signup_page)
signup_frame.pack(fill="both", expand=True, padx=20, pady=10)

_original_profile_image = Image.open("greenprofile.png").convert("RGBA")
CTK_IMG_SMALL = CTkImage(light_image=_original_profile_image, dark_image=_original_profile_image, size=(100, 100))
profile_label = CTkLabel(signup_frame, text="", image=CTK_IMG_SMALL)
profile_label.image = CTK_IMG_SMALL
profile_label.pack(pady=(10, 15))

name_entry = CTkEntry(signup_frame, placeholder_text="Username", width=275, height=30, border_width=2, corner_radius=10, font=("Lexend Deca", 16))
email_entry = CTkEntry(signup_frame, placeholder_text="Email", width=275, height=30, border_width=2, corner_radius=10, font=("Lexend Deca", 16))
password_entry = CTkEntry(signup_frame, placeholder_text="Password", width=275, height=30, border_width=2, corner_radius=10, font=("Lexend Deca", 16), show="*")
terms_checkbox = CTkCheckBox(signup_frame, text="I agree to give an A* to this student", width=275, height=30, font=("Lexend Deca", 12))
signup_button = CTkButton(signup_frame, text="Start Your Wellbeing Journey!", corner_radius=20, font=("Lexend Deca", 20, "bold"), fg_color="#4CAF50", hover_color="#3E803F", border_color="#000000", border_width=3.5, text_color="#000000")
login_button = CTkButton(signup_frame, text="Already have an account? Log in here.", corner_radius=10, font=("Lexend Deca", 12, "underline"), fg_color="transparent", hover_color="#3c6833", border_color="#000000", border_width=0, text_color="#ffffff")

name_entry.pack(pady=(5, 0))
email_entry.pack(pady=(10, 0))
password_entry.pack(pady=(10, 0))
terms_checkbox.pack(pady=(20, 0), padx=(50, 0))
signup_button.pack(pady=(20, 0))
login_button.pack(pady=(20, 0))

screen_width = signup_page.winfo_screenwidth()
screen_height = signup_page.winfo_screenheight()
centre_x = int((screen_width - 420) / 2)
centre_y = int((screen_height - 680) / 2)
signup_page.geometry(f"+{centre_x}+{centre_y}")

signup_page.mainloop()
