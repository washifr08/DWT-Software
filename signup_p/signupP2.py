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

_original_profile_image = Image.open("greenprofile.png").convert("RGBA")
ctk_image_small = CTkImage(light_image=_original_profile_image, dark_image=_original_profile_image, size=(100, 100))
profile_label = CTkLabel(signup_page, text="", image=ctk_image_small)
profile_label.image = ctk_image_small
profile_label.pack(pady=(10, 15))

screen_width = signup_page.winfo_screenwidth()
screen_height = signup_page.winfo_screenheight()
centre_x = int((screen_width - 420) / 2)
centre_y = int((screen_height - 680) / 2)
signup_page.geometry(f"+{centre_x}+{centre_y}")

signup_page.mainloop()
