from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    #Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SEARCH FOR PASSWORD ------------------------------- #

def search():
    website = website_entry.get().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="error", message="No Data File Found")
    else:
        if website in data:
            email_found = data[website]["email"]
            password_found = data[website]["password"]
            messagebox.showinfo(title="Password Found",
                                message=f"Email:{email_found}\n Password:{password_found}\n")
        else:
            messagebox.showinfo(title="Oops", message=f"No data for {website} exists.")

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:{
            "email":email,
            "password":password
        }
    }

    if len(website)==0 or len(password)==0:
        messagebox.showinfo(title="Oops", message="Please enter both the website name and your password.")
    else:
        # is_ok= messagebox.askokcancel(title=website,message=f"These are the details entered.\n Email:{email}\n Password:{password}\n Is it ok to save?")
        # if is_ok:
        try:
            # Reading old data
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file)
        else:
            # Updating the old data with new data
            data.update(new_data)
            # Saving updated data
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#FFFFFF")

canvas = Canvas(width=200, height=200, bg="#FFFFFF", highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", font=("Arial", 14, "normal"), bg="#FFFFFF", highlightbackground="#FFFFFF")
website_label.grid(row=1, column=0, sticky="w")

website_entry = Entry(width=22, highlightbackground="#FFFFFF")
website_entry.grid(row=1, column=1, sticky="w")
website_entry.focus()

search_button = Button(text="Search", font=("Arial", 12, "normal"), width=14, highlightthickness=0, highlightbackground="#FFFFFF", command=search)
search_button.grid(row=1, column=2, sticky="w")  # Align to the west (left)

email_label = Label(text="Email/username:", font=("Arial", 14, "normal"), bg="#FFFFFF", highlightbackground="#FFFFFF")
email_label.grid(row=2, column=0, sticky="w")

email_entry = Entry(width=36, highlightbackground="#FFFFFF")
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0,"mockemail@gmail.com")

password_label = Label(text="Password:", font=("Arial", 14, "normal"), bg="#FFFFFF", highlightbackground="#FFFFFF")
password_label.grid(row=3, column=0, sticky="w")

password_entry = Entry(width=22, highlightbackground="#FFFFFF")
password_entry.grid(row=3, column=1, sticky="w")

search_button = Button(text="Generate Password", font=("Arial", 12, "normal"), width=14, highlightthickness=0, highlightbackground="#FFFFFF", command=generate_password)
search_button.grid(row=3, column=2, sticky="w")  # Align to the west (left)

add_button = Button(text="Add", width=34, highlightthickness=0, highlightbackground="#FFFFFF", command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="w")

window.mainloop()
