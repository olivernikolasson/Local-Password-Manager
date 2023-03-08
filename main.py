import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(numbers) for _ in range(nr_numbers)]
    password_numbers = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password_load = "".join(password_list)

    password_entry.insert(index=0, string=password_load)
    pyperclip.copy(password_load)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_credentials():
    new_data = {
        web_get.get(): {
            "email": user_get.get(),
            "password": pass_get.get(),
        }

    }

    if len(web_get.get()) == 0 or len(pass_get.get()) == 0:
        messagebox.showinfo(title="Fields are empty", message="please dont leave any fields empty")
    else:
        try:
            with open("creds.json", "r") as data_file:
                creds = json.load(data_file)
        except FileNotFoundError:
            with open("creds.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            messagebox.showinfo(title="Error", message="If you see this error something went wrong with the\n"
                                                       ".json file.\nPlease backup all information found in it\n"
                                                       "then delete it. Then restart the program and add a new\n"
                                                       "website, this will create a new .json file.\n\n"
                                                       "then add your backedup information")
        else:
            creds.update(new_data)

            with open("creds.json", "w") as data_file:
                json.dump(creds, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    try:
        with open("creds.json", "r") as data_read:
            data_load = json.load(data_read)
        info = web_get.get()
        search_item = [(data_load[info]) for website in data_load if website == info]
        email = search_item[0]["email"]
        pword = search_item[0]["password"]
        messagebox.showinfo(title=info, message=f"username: {email}\npassword: {pword}\n\nYour password is copied"
                                                f" to the clipboard!")
        pyperclip.copy(pword)
    except IndexError:
        messagebox.showinfo(title="Not found", message="Not found.\nNot added or a spelling error")


# ---------------------------- HELP INFO ------------------------------- #
def help_info():
    messagebox.showinfo(title="Information", message="Version 1\n\nCase Sensetive so please add\nwebsites using only"
                                                     " lowercase\n\n //Oliver")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()

window.title("Py-Password-Safe")
window.config(padx=100, pady=50, )
canvas = Canvas(width=300, height=300, highlightthickness=0)
bg = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=bg)
canvas.grid(column=2, row=0)

# Website Text and Entry Section
website_text = Label(text="Website")
website_text.grid(column=1, row=1)
web_get = website_entry = Entry(width=35)
website_entry.grid(column=2, row=1, columnspan=2)

# Email/Username Entry Section

user_text = Label(text="Email/Username")
user_text.grid(column=1, row=2)
user_get = user_entry = Entry(width=35)
user_entry.insert(index=0, string="")
user_entry.grid(column=2, row=2, columnspan=2)

# Password Section

password_text = Label(text="Password")
password_text.grid(column=1, row=3)
pass_get = password_entry = Entry(width=35)
password_entry.grid(column=2, row=3, columnspan=2)
password_entry.insert(index=0, string="")
password_button = Button(text="Generate Password", command=password, width=13)
password_button.grid(column=3, row=3)

# Search Section

search_button = Button(text="Search", command=find_password, width=13)
search_button.grid(column=3, row=1)

# Add to database Section
add_button = Button(text="Add", width=36, command=save_credentials)
add_button.grid(column=2, row=4, columnspan=2)

# Add Help button
add_button = Button(text="Help", width=5, command=help_info)
add_button.grid(column=4, row=5)

window.mainloop()
