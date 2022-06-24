# Importing modules
import json
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import main_functions

color = "#CAF1DE"


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def loginAndSignUp():
    root = Tk()

    def change(username):
        root.destroy()
        handlerWhatTo(username)

    root.title("Data Manager")
    root.geometry("600x500")
    root.configure(bg="#CAF1DE")

    userEntryMode = "login"
    usernameData = ""

    label_Title = Label(root, text="Data Manager", bg=color,
                        font=("@Yu Gothic UI Semibold", 20, "normal"))
    label_Title.place(relx=0.5, rely=0.05, anchor=CENTER)

    input_Username = EntryWithPlaceholder(root, placeholder="Username")
    input_Username["width"] = 40
    input_Username["font"] = ("@Yu Gothic UI Semibold", 15, "normal")
    input_Username.place(relx=0.5, rely=0.2, anchor=CENTER)

    input_Password = EntryWithPlaceholder(root, placeholder="Password")
    input_Password["width"] = 40
    input_Password["font"] = ("@Yu Gothic UI Semibold", 15, "normal")
    input_Password.place(relx=0.5, rely=0.3, anchor=CENTER)

    button_Login = Button(root, text="Log In", relief="flat",
                          padx=70, pady=5, bg="#2C95F6", fg="white", font=("Arial", 10, "bold"))
    button_Login.place(relx=0.5, rely=0.45, anchor=CENTER)

    label_DontHaveAAccount = Label(root, text="Don't have an account? ", font=(
        "Arial", 13, "normal"), bg=color)
    label_DontHaveAAccount.place(relx=0.3, rely=0.7)

    button_DontHaveAAccount = Button(root, text="Sign Up", relief="flat", bg=color, font=("Arial", 13, "normal"),
                                     fg="#2C95F6", )

    label_msg = Label(root, text="", fg="red", bg=color, font=("Arial", 13, "bold"))
    label_msg.place(relx=0.5, rely=0.6, anchor=CENTER)

    def changeUserEntryMode():
        global userEntryMode
        global button_DontHaveAAccount
        global label_DontHaveAAccount
        global button_Login
        if userEntryMode == "login":
            userEntryMode = "signup"
            button_Login["text"] = "Sign Up"
            button_DontHaveAAccount["text"] = "Log In"
            label_DontHaveAAccount["text"] = "Have a account? "
        elif userEntryMode == "signup":
            userEntryMode = "login"
            button_Login["text"] = "Log In"
            button_DontHaveAAccount["text"] = "Sign Up"
            label_DontHaveAAccount["text"] = "Don't have an account? "

    button_DontHaveAAccount["command"] = changeUserEntryMode
    button_DontHaveAAccount.place(relx=0.59, rely=0.69, )

    def handle():
        if userEntryMode == "login":
            login()
        elif userEntryMode == "signup":
            signup()

    with open('accounts.json') as json_file:
        accountsData = json.load(json_file)

    def login():
        global usernameData
        global label_msg
        username = input_Username.get()
        password = input_Password.get()
        usernameData = username
        if username in accountsData["accounts"]:
            encryptedPassword = accountsData["accounts"][username]
            decryptedPassword = main_functions.decryptData(username, encryptedPassword)
            if password == decryptedPassword:
                label_msg["fg"] = "lime"
                label_msg["text"] = "Logged In successfully"
                messagebox.showinfo("Login Successful", "You are now logged in")
                time.sleep(5)
                change(username)
            else:
                label_msg["fg"] = "red"
                label_msg["text"] = "Username password is wrong! Please try again."
                messagebox.showerror(
                    "Wrong password", "Username password is wrong! Please try again.")
        else:
            label_msg["fg"] = "red"
            label_msg["text"] = "Username does not exists! Please try again."
            messagebox.showerror("Username not found",
                                 "Username does not exists! Please try again.")
            return username

    button_Login["command"] = handle

    def signup():
        global label_msg
        global usernameData
        username = input_Username.get()
        password = input_Password.get()
        usernameData = username
        if username != "" and password != "":
            if username in accountsData["accounts"]:
                label_msg["fg"] = "red"
                label_msg["text"] = "Username already exists. Please try again."
            else:
                encryptedPassword = main_functions.encryptText(username, password)
                accountsData["accounts"][username] = encryptedPassword
                with open('accounts.json', 'w') as outfile:
                    json.dump(accountsData, outfile)
                os.system("cls")
                os.system(f'mkdir \"{str(os.getcwd())}"\\Data\\"{username}\"')
                with open(str(os.getcwd()) + "\\Data\\" + username + "\\" + "data.json", "w") as f:
                    f.write("{\"data\": {}}")
                username = usernameData
                label_msg["fg"] = "lime"
                label_msg["text"] = "Account Successful created"
                messagebox.showinfo("Account created Successful",
                                    "Your account is successfully make now we're logging you in")
                login()

    root.mainloop()


def handlerWhatTo(usernameFromData):
    root = Tk()

    root.geometry("600x500")
    root.title("Data Manager")

    root.configure(bg=color)

    label_Title = Label(root, text="Data Manager", font=("@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)

    label_whatToDo = Label(root, text="What You Want To Do? ", bg=color, font=("@Yu Gothic UI Semibold", 20, "normal"))
    label_whatToDo.place(relx=0.1, rely=0.2)

    label_ChoiceStringVar = tk.StringVar()
    label_Choice = ttk.Combobox(values=["Work with data", "Work with files"], state="readonly",
                                textvariable=label_ChoiceStringVar, font=("@Yu Gothic UI Semibold", 20, "normal"))
    label_Choice.place(relx=0.5, rely=0.4, anchor=CENTER)
    label_Choice.current(0)

    def changeScript():
        if label_ChoiceStringVar == "Work with data":
            root.destroy()
            workWithData()
        elif label_ChoiceStringVar == "Work with files":
            root.destroy()
            workWithFiles()
        else:
            messagebox.showerror("No value error", "Please select a value than go ahead!")

    button_go = Button(root, text="Go!", relief="flat", bg="#70CED4", width=30, height=1,
                       font=("@Yu Gothic UI Semibold", 15, "bold"), command=changeScript)
    button_go.place(relx=0.5, rely=0.7, anchor=CENTER)

    root.mainloop()


def workWithData():
    pass


def workWithFiles():
    pass


handlerWhatTo("Hamzah Sajid")
