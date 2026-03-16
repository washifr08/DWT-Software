from customtkinter import * #ctk library
from PIL import Image # pillow for image importing
from tkinter import messagebox # messagebox funtionality for errors
import re # allows for regex for email validity checking
from openpyxl import * # allows interractions with excel
import hashlib # allows encryption of passwords saved to excel
import os # allows saving files to device
import subprocess
import sys

# creates signup window in which everything will be placed, sets size and changes title
signup_page = CTk()
signup_page.geometry("420x480")
signup_page.title("D.W.T Welcome Page")

signup_frame = CTkFrame(signup_page) # creates signup frame
login_frame=CTkFrame(signup_page)  # creates login frame 

frame_status="signup"  # variable to track which frame is currently displayed

excel_file = "registered_users.xlsx"  # creates excel file name to store registered users
if not os.path.exists(excel_file):
    wb=Workbook() # create workbook if file doesn't exist
    ws=wb.active
    ws.append(["Name", "Email", "Password"])  # add headers if they doesn't already exist
    wb.save(excel_file) # save the new workbook

# simple regular expression to check if email is in valid format
def is_valid_email(email):
    pattern= r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern,email)

# function to cancel any scheduled updates before window closes so no errors occur
def cancel_scheduled_updates():
    global _profile_after_id, _entry_after_id
    if _profile_after_id:
        signup_page.after_cancel(_profile_after_id) # cancels scheduled profile image update
        _profile_after_id = None
    if _entry_after_id:
        signup_page.after_cancel(_entry_after_id) # cancels scheduled entry text update
        _entry_after_id = None

# function to check whether entry fields are correct in login page
def login():
    email=email_entry_login.get()
    password=password_entry_login.get()
    if not email or not password:
        # if fields are left empty or email in invalid format error box pops up
        messagebox.showwarning("Empty", "Please fill in all the fields")
        return
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address")
        return
    
    hashed_login_password = hashlib.sha256(password.encode()).hexdigest() # encrypts entered password the same way as all other passwords
    wb = load_workbook(excel_file)
    ws=wb.active
    # searches excel spreadsheet for all emails and passwords
    for row in ws.iter_rows(min_row=2,values_only=True):
        name_in_excel, email_in_excel, password_in_excel = row
        if email_in_excel == email and password_in_excel == hashed_login_password:
            messagebox.showinfo("Success", "Welcome back!")
            wb.close()
            cancel_scheduled_updates() # stops scheduled updates before closing
            signup_page.after(100, signup_page.destroy)
            subprocess.Popen([sys.executable, "homepage.py", name_in_excel, email_in_excel])  # opens homepage after login
            return
    wb.close()
    messagebox.showerror("Error", "Incorrect email or password")

# function to retrieve inputs into entry boxes and checkbox or warning message if empty, incorrect format, or used email.
def signup():
    name=name_entry.get()
    email=email_entry.get()
    password=password_entry.get()
    terms_check= terms_checkbox.get()
    if not name or not email or not password:
        messagebox.showwarning("Empty", "Please fill in all the fields")
        return
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address")
        return
    if not terms_check:
        messagebox.showwarning("Terms Not Agreed", "You must agree to the terms to sign up")
        return
    
    wb=load_workbook(excel_file) # loads the excel file
    ws=wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if email==row[1]: # checks if the email already exists in the excel file
            messagebox.showerror("Error", "Email already registered. Please use a different email.")
            return
    
    encrypted_password=hashlib.sha256(password.encode()).hexdigest() # hashes the password for security
    ws.append([name,email,encrypted_password]) # appends the user details to the excel file and the headers made earlier
    wb.save(excel_file) # saves the excel file
    wb.close()
    messagebox.showinfo("Success", "Go ahead and login now!")
    name_entry.delete(0, 'end') # clears the entry boxes and checkboxes if successful
    email_entry.delete(0, 'end')
    password_entry.delete(0, 'end')
    terms_checkbox.deselect()
    login_form()
    return 

# function to switch to login frame when go to login button is clicked
def login_form():
    global frame_status
    login_window_size=signup_page.state()
    signup_frame.pack_forget()  # hides the signup frame
    login_frame.pack(fill=BOTH, expand=True,padx=20,pady=10) # replaces prev frame with the login frame
    frame_status="login" # updates according to new frame being used

    # schedule the update function to set the cached image into frame
    schedule_updates()

    # logic for resizing entry boxes and buttons
    if login_window_size == "normal":
        
        new_width_txt = 275 # _txt is for entry box sizes
        new_height_txt = 30
        new_corner_radius = 10
        
        new_font_size = 16 # font size for entry boxes and login button
        
        new_button_width = 250 # for button sizes and corner smoothness
        new_button_height = 40
        new_button_corner_radius = 20

        new_login_width=50 # box and font sizes for little button to transport to different frames
        new_login_height=30
        new_login_font_size=12
        
        switch_Width=120 # Dark / Light switch sizes
        switch_Height=0
        switch_font_size=12

    elif login_window_size == "zoomed":
        
        new_width_txt = 600
        new_height_txt = 70
        new_corner_radius = 22

        new_font_size = 30

        new_button_width = 500
        new_button_height = 60
        new_button_corner_radius = 30

        new_login_width=150
        new_login_height=40
        new_login_font_size=18
        
        switch_Width=220
        switch_Height=0
        switch_font_size=20

    else:  # fallback for minimized or unknown state
        
        new_width_txt = 250
        new_height_txt = 30
        new_corner_radius = 10      

        new_font_size = 16

        new_button_width = 100
        new_button_height = 30
        new_button_corner_radius = 10


        new_login_width=200
        new_login_height=30
        new_login_font_size=12

        switch_Width=120
        switch_Height=25
        switch_font_size=12

    # updates everything with new size preferences
    theme_switch.configure(width=switch_Width, height=switch_Height, font=("Century Gothic", switch_font_size))
    email_entry_login.configure(width=new_width_txt, height=new_height_txt,corner_radius=new_corner_radius,
                                font=("Century Gothic", new_font_size))
    password_entry_login.configure(width=new_width_txt, height=new_height_txt,corner_radius=new_corner_radius,
                                    font=("Century Gothic", new_font_size))
    signup_button_login.configure(width=new_button_width, height=new_button_height,corner_radius=new_button_corner_radius,
                                    font=("Century Gothic", new_font_size, "bold"))
    back_to_signup_button.configure(font=("Century Gothic",new_login_font_size, "underline"), width=new_login_width, height=new_login_height
                                    , corner_radius=new_button_corner_radius)
            
    # places all updated objects login page based on window size
    if login_window_size=="zoomed":
        theme_switch.pack(anchor="ne", pady=(10,0))
        email_entry_login.pack(pady=(70, 0))
        password_entry_login.pack(pady=(30, 0))
        login_profile_label.pack(pady=(70, 15))
        signup_button_login.pack(pady=(85, 0))
        back_to_signup_button.pack(pady=(60, 0))
    else:
        theme_switch.pack(anchor="ne", pady=10)
        email_entry_login.pack(pady=(20, 0))
        password_entry_login.pack(pady=(10, 0))
        login_profile_label.pack(pady=(20, 10))
        signup_button_login.pack(pady=(35, 0))
        back_to_signup_button.pack(pady=(20, 0))

# function to allow smooth transition back to signup page
def back_to_signup_form():
    global frame_status
    login_frame.pack_forget()  # hides the signup frame
    signup_frame.pack(fill=BOTH, expand=True,padx=20,pady=10) # replaces prev frame with the login frame # displays the login frame
    frame_status="signup"

    # schedule the cached-image and layout updates 
    schedule_updates()

# creates the button to transport to login page
login_button = CTkButton(master=signup_frame, text="Already have an account? Log in here.", corner_radius=10,
                           font=("Century Gothic", 12, "underline"), fg_color="transparent", hover_color="#3c6833",
                             border_color="#000000", border_width=0, text_color="#ffffff", command=login_form)

#creates button to take user back to signup page
back_to_signup_button= CTkButton(master=login_frame, text="Want to go back and create a new account? \nSignup here!", corner_radius=10,
                           font=("Century Gothic", 12, "underline"), fg_color="transparent", hover_color="#3c6833",
                             border_color="#000000", border_width=0, text_color="#ffffff", command=back_to_signup_form)

# function to change the login button text color based on dark/light mode
def dark_light_text():
    global login_colour
    theme_state = get_appearance_mode()
    if theme_state=="Dark":
        login_colour="#ffffff"
        hover_colour="#3c6833"
    else:
        login_colour = "#000000"
        hover_colour="#8caf85"
        
    login_button.configure(hover_color=hover_colour,text_color=login_colour) # updates buttons with new configurations
    back_to_signup_button.configure(hover_color=hover_colour,text_color=login_colour)

# function to toggle between dark and light mode
def dark_light_toggle():
    theme_state= get_appearance_mode()
    if theme_state=="Dark":
        set_appearance_mode("light")
    else:
        set_appearance_mode("dark")

    # updates the text color of the login button every time dark_light mode is toggled
    dark_light_text() 
    # schedule an update after theme change so no lag as we are not ahead of theme engine
    schedule_updates()

# creates the dark/light mode switch button and places is it top right, activates the toggle function when clicked
theme_switch = CTkSwitch(signup_page, text="Dark / Light Mode", command=dark_light_toggle, progress_color="#4CAF50")
theme_switch.pack(anchor="ne", padx=10, pady=10)

# IMAGE LOADING + CACHING
# loads the original image (converted to RGBA to be safe with transparency)
_original_profile_image = Image.open("greenprofile.png").convert("RGBA")

# define the sizes app actually uses (small for normal, large for zoomed), made constants as sizes wont be reconfigured ever
_SMALL_SIZE = (100, 100)
_LARGE_SIZE = (300, 300)

# create cached resized images, heavy image loading work finished here and saved to be reused 
_pil_small = _original_profile_image.copy().resize(_SMALL_SIZE, Image.LANCZOS)
_pil_large = _original_profile_image.copy().resize(_LARGE_SIZE, Image.LANCZOS)

# create cached CTkImage objects from those resized images
CTK_IMG_SMALL = CTkImage(light_image=_pil_small, dark_image=_pil_small, size=_SMALL_SIZE)
CTK_IMG_LARGE = CTkImage(light_image=_pil_large, dark_image=_pil_large, size=_LARGE_SIZE)

# sses the small image as initial image 
normal_profile_image_displayed = CTK_IMG_SMALL

# creates and displays label with image in signup frame
profile_label = CTkLabel(signup_frame, text="", image=normal_profile_image_displayed)
profile_label.image = normal_profile_image_displayed
profile_label.pack(pady=(10, 15))

# creates and displays label with image in login frame
login_profile_label = CTkLabel(login_frame, text="", image=normal_profile_image_displayed)
login_profile_label.image = normal_profile_image_displayed
login_profile_label.pack(pady=(10, 15))

# creates entry boxes for name, email, password, checkbox for terms and signup button for signup page
name_entry = CTkEntry(signup_frame, placeholder_text="Username", width=275, height=30
                      , border_width=2, corner_radius=10, font=("Century Gothic", 16))
email_entry = CTkEntry(signup_frame, placeholder_text="Email", width=275, height=30
                         , border_width=2, corner_radius=10, font=("Century Gothic", 16))
password_entry = CTkEntry(signup_frame, placeholder_text="Password", width=275, height=30
                         , border_width=2, corner_radius=10, font=("Century Gothic", 16), show="*")
terms_checkbox = CTkCheckBox(signup_frame, text="I agree to give an A* to this student",width=275,
                             height=30, font=("Century Gothic", 12))
signup_button = CTkButton(master=signup_frame, text="Start Your Wellbeing Journey!", corner_radius=20,
                           font=("Century Gothic", 20, "bold"), fg_color="#4CAF50", hover_color="#3E803F",
                             border_color="#000000", border_width=3.5, text_color="#000000", command=signup)

# creates email and password entry fields for login page
email_entry_login = CTkEntry(login_frame, placeholder_text="Email", width=275, height=30
                         , border_width=2, corner_radius=10, font=("Century Gothic", 16))
password_entry_login = CTkEntry(login_frame, placeholder_text="Password", width=275, height=30
                         , border_width=2, corner_radius=10, font=("Century Gothic", 16), show="*")
signup_button_login = CTkButton(master=login_frame, text="Resume Your Wellbeing Journey!", corner_radius=20,
                           font=("Century Gothic", 20, "bold"), fg_color="#4CAF50", hover_color="#3E803F",
                             border_color="#000000", border_width=3.5, text_color="#000000", command=login)

# TRACKERS + SCHEDULER 
# trackers for last-known states which are going to be used for functionality of functions later
window_size_for_img = signup_page.state()
last_frame_img = frame_status

window_size_for_entrytxt = signup_page.state()
last_frame_txt = frame_status

# after ids so we can cancel previously-scheduled updates 
_profile_after_id = None
_entry_after_id = None

def schedule_updates():
    global _profile_after_id, _entry_after_id
    
    # cancel pending scheduled calls if they exist
    try:
        if _profile_after_id is not None:
            signup_page.after_cancel(_profile_after_id)
    except Exception:
        pass
    try:
        if _entry_after_id is not None:
            signup_page.after_cancel(_entry_after_id)
    except Exception:
        pass

    # schedule updates after a short 40 ms delay (coalescing rapid events)
    _profile_after_id = signup_page.after(40, update_profile_image)
    _entry_after_id = signup_page.after(40, update_entry_text)

# fucntion to resize the profile image based on window size 
def update_profile_image():
    global window_size_for_img, last_frame_img

    state = signup_page.state() # grabs the current window size

    # only do work if window state or visible frame changed
    if state != window_size_for_img or frame_status != last_frame_img:
        # pick cached CTkImage depending on window state
        if state == "zoomed":
            current_ctk_image = CTK_IMG_LARGE # resizes image to constant of 300px set earlier based on window size
        else:
            current_ctk_image = CTK_IMG_SMALL # similarly resizes to 100px

        # set the image for the currently visible label
        if frame_status == "signup":
            target_label = profile_label
        else:
            target_label = login_profile_label

        # assign only if different
        if getattr(target_label, "image", None) is not current_ctk_image:
            target_label.configure(image=current_ctk_image)
            target_label.image = current_ctk_image
            
        window_size_for_img = state # reupdates the window state variable for image
        last_frame_img = frame_status # reupdates the current frame variable for image

# function to resize the entry boxes, checkbox and signup button based on window size (one-shot)
def update_entry_text():
    global window_size_for_entrytxt, last_frame_txt
    
    state = signup_page.state()

    # only update if something changed
    if state != window_size_for_entrytxt or frame_status != last_frame_txt:
        if frame_status=="signup":  # only resize entry boxes etc if signup frame is displayed
            # pick new size depending on window state
            if state == "normal":
                new_width_txt = 275 # _txt is for entry boxes
                new_height_txt = 30
                new_corner_radius = 10

                new_font_size = 16 # font size for entry boxes and checkbox
                
                new_font_size_checkbox = 14

                new_button_width = 250
                new_button_height = 40
                new_button_corner_radius = 20

                new_login_width=50 # box and font sizes for login button
                new_login_height=30
                new_login_font_size=14

                switch_Width=120 #font and size for dark / light switch
                switch_Height=0
                switch_font_size=12

            elif state == "zoomed":
                new_width_txt = 600
                new_height_txt = 70
                new_corner_radius = 22

                new_font_size = 30

                new_font_size_checkbox = 24

                new_button_width = 500
                new_button_height = 60
                new_button_corner_radius = 30

                new_login_width=150
                new_login_height=40
                new_login_font_size=24

                switch_Width=220
                switch_Height=0
                switch_font_size=20

            else:  # fallback for minimized or unknown state (use ints)
                # same as normal mode
                new_width_txt = 275 
                new_height_txt = 30
                new_corner_radius = 10

                new_font_size = 16
                
                new_font_size_checkbox = 22

                new_button_width = 250
                new_button_height = 40
                new_button_corner_radius = 20

                new_login_width=50
                new_login_height=30
                new_login_font_size=12

                switch_Width=120 
                switch_Height=0
                switch_font_size=12

            # applies all the updates based on the window sizes
            name_entry.configure(width=new_width_txt, height=new_height_txt,corner_radius=new_corner_radius,
                                font=("Century Gothic", new_font_size))
            email_entry.configure(width=new_width_txt, height=new_height_txt,corner_radius=new_corner_radius,
                                font=("Century Gothic", new_font_size))
            password_entry.configure(width=new_width_txt, height=new_height_txt,corner_radius=new_corner_radius,
                                    font=("Century Gothic", new_font_size))
            terms_checkbox.configure(width=new_width_txt, height=new_height_txt,
                                    font=("Century Gothic", new_font_size_checkbox))
            signup_button.configure(width=new_button_width, height=new_button_height,corner_radius=new_button_corner_radius,
                                    font=("Century Gothic", new_font_size, "bold"))
            login_button.configure(font=("Century Gothic",new_login_font_size, "underline"), width=new_login_width, height=new_login_height
                                   , corner_radius=new_button_corner_radius)
            theme_switch.configure(width=switch_Width, height=switch_Height, font=("Century Gothic", switch_font_size))
            
            # places all the updates objects in distances from eachother based on window size
            if state=="zoomed":
                name_entry.pack(pady=(40, 0))
                email_entry.pack(pady=(30, 0))
                password_entry.pack(pady=(30, 0))
                terms_checkbox.pack(pady=(45, 0), padx=(145, 0))
                signup_button.pack(pady=(50, 0))
                login_button.pack(pady=(40, 0))
                signup_frame.pack(pady=10, padx=20, fill="both", expand=True)
                profile_label.pack(pady=(60, 25))
                theme_switch.pack(anchor="ne", pady=(10,0))
            else:
                name_entry.pack(pady=(5, 0))
                email_entry.pack(pady=(10, 0))
                password_entry.pack(pady=(10, 0))
                terms_checkbox.pack(pady=(20, 0))
                signup_button.pack(pady=(20, 0))
                login_button.pack(pady=(20, 0))
                signup_frame.pack(pady=(10, ), padx=20, fill="both", expand=True)
                profile_label.pack(pady=(10, 15))
                theme_switch.pack(anchor="ne", pady=(10))
        else:
            # login frame objects sizing, same pattern
            if state == "normal":
                new_width_txt = 275
                new_height_txt = 30
                new_corner_radius = 10

                new_font_size = 16

                new_button_width = 250
                new_button_height = 40
                new_button_corner_radius = 20

                new_login_width=50
                new_login_height=30
                new_login_font_size=14

                switch_Width=120
                switch_Height=0
                switch_font_size=12

            elif state == "zoomed":
                new_width_txt = 600
                new_height_txt = 70
                new_corner_radius = 22

                new_font_size = 30

                new_button_width = 500
                new_button_height = 60
                new_button_corner_radius = 30

                new_login_width=150
                new_login_height=40
                new_login_font_size=24

                switch_Width=220
                switch_Height=0
                switch_font_size=20

            else:  # fallback
                new_width_txt = 275
                new_height_txt = 30
                new_corner_radius = 10

                new_font_size = 16

                new_button_width = 250
                new_button_height = 40
                new_button_corner_radius = 20

                new_login_width=50
                new_login_height=30
                new_login_font_size=12

                switch_Width=120
                switch_Height=0
                switch_font_size=12
                
            # applies all the updates based on the window sizes
            theme_switch.configure(width=switch_Width, height=switch_Height, font=("Century Gothic", switch_font_size))
            email_entry_login.configure(width=new_width_txt, height=new_height_txt,corner_radius=new_corner_radius,
                                font=("Century Gothic", new_font_size))
            password_entry_login.configure(width=new_width_txt, height=new_height_txt,corner_radius=new_corner_radius,
                                    font=("Century Gothic", new_font_size))
            signup_button_login.configure(width=new_button_width, height=new_button_height,corner_radius=new_button_corner_radius,
                                    font=("Century Gothic", new_font_size, "bold"))
            back_to_signup_button.configure(font=("Century Gothic",new_login_font_size, "underline"), width=new_login_width, height=new_login_height, corner_radius=new_button_corner_radius)
            
            # places all the updates objects in distances from eachother based on window size
            if state=="zoomed":
                theme_switch.pack(anchor="ne", pady=(10,0))
                email_entry_login.pack(pady=(70, 0))
                password_entry_login.pack(pady=(30, 0))
                login_profile_label.pack(pady=(60,25))
                signup_button_login.pack(pady=(85, 0))
                back_to_signup_button.pack(pady=(60, 0))
                login_frame.pack(pady=10, padx=20)
            else:
                theme_switch.pack(anchor="ne", pady=10)
                email_entry_login.pack(pady=(20, 0))
                password_entry_login.pack(pady=(10, 0))
                login_profile_label.pack(pady=(10, 15))
                signup_button_login.pack(pady=(35, 0))
                back_to_signup_button.pack(pady=(20, 0))
                login_frame.pack(pady=(10, ))
                
        window_size_for_entrytxt = state
        last_frame_txt = frame_status

def on_configure(event=None):
    # schedule debounced updates coalesces rapid resize/theme events
    schedule_updates()

# binds configure to schedule updates functoin
signup_page.bind("<Configure>", on_configure)

# initial schedule to ensure correct initial sizing/images
schedule_updates()

# finds width and height of screen
screen_width = signup_page.winfo_screenwidth()
screen_height = signup_page.winfo_screenheight()

# calculates x and y coordinates for the window to be centered
centre_x = int((screen_width - 420) / 2)
centre_y = int((screen_height - 680) / 2)

# sets the position of the window to be centered
signup_page.geometry(f"+{centre_x}+{centre_y}")

signup_page.mainloop()