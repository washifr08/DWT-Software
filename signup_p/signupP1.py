from customtkinter import *

signup_page = CTk()
signup_page.geometry("420x480")
signup_page.title("D.W.T Welcome Page")

screen_width = signup_page.winfo_screenwidth()
screen_height = signup_page.winfo_screenheight()
centre_x = int((screen_width - 420) / 2)
centre_y = int((screen_height - 680) / 2)
signup_page.geometry(f"+{centre_x}+{centre_y}")

signup_page.mainloop()
