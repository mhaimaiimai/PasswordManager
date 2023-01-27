from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    
    password_input.delete(0, END)
    password_input.insert(0, password)
    
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {website: {"email" : email,
                          "password" : password} }
    
    if len(website) >0 and len(email) >0 and len(password) >0:
        is_save_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                            f"\nPassword: {password} \nIs it ok to save?")
        if is_save_ok:
            try:
                with open("data.json", mode="r") as datafile:
                    data = json.load(datafile)        
                                    
            except FileNotFoundError:
                datafile = open("data.json", mode="w")
                json.dump(new_data, datafile, indent=4)
                datafile.close()
                
            else:
                data.update(new_data)
                with open("data.json", mode="w") as datafile:
                    json.dump(data, datafile, indent=4)
                    
            finally:
                website_input.delete(0,END)
                email_input.delete(0,END)
                password_input.delete(0,END)
    else:
        messagebox.showerror(title="Error", message="Please fill out all fields before save.")

# ---------------------------- SEARCH ------------------------------- #
def search():
    try:
        with open("data.json", mode="r") as datafile:
            data = json.load(datafile)        
                            
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="There is no password data being saved yet.")
    
    website = website_input.get()
    
    try:
        website_data = data[website]
    except KeyError:
        messagebox.showerror(title="Error", message="There is no password data for this website.")
    else:
        email_input.delete(0, END)
        email_input.insert(0, website_data["email"])
        password_input.delete(0, END)
        password_input.insert(0, website_data["password"])
        

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("My Password Manager")
window.configure(padx=40, pady=40, bg="white")

logo_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
canvas.create_image(130,100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", fg="black", bg="white")
website_label.grid(row=1, column=0)
website_input = Entry(width=21, fg="black", bg="white", highlightthickness=0)
website_input.focus()
website_input.grid(row=1, column=1)

search_button = Button(text="Search", width=13, fg="black", bg="white", highlightthickness=0, highlightbackground="white", command=search)
search_button.grid(row=1, column=2)

email_label = Label(text="Email/Username:", fg="black", bg="white")
email_label.grid(row=2, column=0)
email_input = Entry(width=38, fg="black", bg="white", highlightthickness=0)
email_input.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:", fg="black", bg="white")
password_label.grid(row=3, column=0)
password_input = Entry(width=21, fg="black", bg="white", highlightthickness=0)
password_input.grid(row=3, column=1)

password_gen_button = Button(text="Generate Password", width=13, fg="black", bg="white", highlightthickness=0, highlightbackground="white", command=password_gen)
password_gen_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, fg="black", bg="white", highlightthickness=0, highlightbackground="white", command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()