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

root = Tk()
label_msg = Label(root, text="", fg="red", bg=color, font=("Arial", 13, "bold"))
userEntryMode = "login"
button_Login = Button()
def loginAndSignUp():
    global  button_Login
    global userEntryMode
    global label_msg
    def change(username):
        root.destroy()
        handlerWhatTo(username)

    root.title("Data Manager")
    root.geometry("600x500")
    root.configure(bg="#CAF1DE")

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

    label_Choice = ttk.Combobox(values=["Work with data", "Work with files"], state="readonly",
                                font=("@Yu Gothic UI Semibold", 20, "normal"))
    label_Choice.place(relx=0.5, rely=0.4, anchor=CENTER)
    label_Choice.current(0)

    def changeScript():
        if label_Choice.get() == "Work with data":
            root.destroy()
            workWithData(usernameFromData)
        elif label_Choice.get() == "Work with files":
            root.destroy()
            workWithFiles()

    button_go = Button(root, text="Go!", relief="flat", bg="#70CED4", width=30, height=1,
                       font=("@Yu Gothic UI Semibold", 15, "bold"), command=changeScript)
    button_go.place(relx=0.5, rely=0.7, anchor=CENTER)

    root.mainloop()


def workWithData(usernameGave):
    root = Tk()
    root.geometry("600x400")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Work With Data", font=("@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    label_Operations = ttk.Combobox(root, values=["Create Data", "View Data", "Delete Data", "Export Data"],
                                    state="readonly", font=("@Yu Gothic UI Semibold", 15, "normal"))
    label_Operations.place(relx=0.5, rely=0.25, anchor=CENTER)
    label_Operations.current(0)

    def changeScreen():
        if label_Operations.get() == "Create Data":
            makeData(usernameGave)
        elif label_Operations.get() == "View Data":
            viewData(usernameGave)
        elif label_Operations.get() == "Delete Data":
            deleteData(usernameGave)
        elif label_Operations.get() == "Export Data":
            exportData(usernameGave)

    button_Do = Button(root, text="Continue", font=("@Yu Gothic UI Semibold", 13, "normal"), command=changeScreen,
                       relief="flat", bg="#70CED4", fg="white")
    button_Do.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()


def makeData(usernameDataGave):
    root = Tk()
    root.geometry("600x500")
    root.title("Data Manager")
    root.configure(bg=color)
    label_Title = Label(root, text="Create Data", font=("@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    label_insrtuction = Label(root, text="Please put the labels and data \" | \" seprated", bg=color,
                              font=("@Yu Gothic UI Semibold", 15, "normal"))
    label_insrtuction.place(relx=0.2, rely=0.2)
    input_DataName = EntryWithPlaceholder(root, placeholder="Data Name")
    input_Labels = EntryWithPlaceholder(root, placeholder="Data Labels")
    input_data = EntryWithPlaceholder(root, placeholder="Data")
    input_DataName["width"] = 40
    input_Labels["width"] = 40
    input_data["width"] = 40
    input_DataName["font"] = ("@Yu Gothic UI Semibold", 15, "normal")
    input_Labels["font"] = ("@Yu Gothic UI Semibold", 15, "normal")
    input_data["font"] = ("@Yu Gothic UI Semibold", 15, "normal")
    input_DataName.place(relx=0.5, rely=0.3, anchor=CENTER)
    input_Labels.place(relx=0.5, rely=0.4, anchor=CENTER)
    input_data.place(relx=0.5, rely=0.5, anchor=CENTER)

    def back():
        workWithData(usernameDataGave)

    with open(str(os.getcwd()) + "\\Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)

    def makeDataNew():
        nameDataIn = input_DataName.get()
        labelIn = input_Labels.get().split(" | ")
        dataIn = input_data.get().split(" | ")
        if nameDataIn != "" and len(labelIn) != 0 and len(dataIn) != 0:
            if len(labelIn) == len(labelIn):
                finalData = {}
                dataDict = dict(zip(labelIn, dataIn))
                finalData[nameDataIn] = dataDict
                dataJSON["data"].update(finalData)
                with open(str(os.getcwd()) + "\\Data\\" + usernameDataGave + "\\" + "data.json", "w") as f:
                    json.dump(dataJSON, f)
            else:
                messagebox.showerror("Data not given properly",
                                     "Please check if the data give is respectively to the label, there are blank spaces.")
        else:
            messagebox.showerror("Data not given properly",
                                 "Please check if the data name is not empty and the label and data are not empty")

    button_createData = Button(root, text="Create Data", font=("@Yu Gothic UI Semibold", 15, "normal"), relief=FLAT,
                               bg="#70CED4", fg="white", command=makeDataNew)
    button_createData.place(relx=0.5, rely=0.7)
    root.mainloop()


def viewData(usernameDataGave):
    root = Tk()
    root.geometry("600x500")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="View Data", font=("@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    data = []
    with open(str(os.getcwd()) + "\\Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)
    for key in dataJSON["data"]:
        data.append(key)
    comboxbox_options = ttk.Combobox(root, values=data, font=("@Yu Gothic UI Semibold", 20, "bold"), state="readonly")
    comboxbox_options.place(relx=0.5, rely=0.2, anchor=CENTER)
    try:
        comboxbox_options.current(0)
    except:
        pass
    dataName = comboxbox_options.get()
    textbox = Text(root,font=("calbri",10,"normal"),width=75)
    textbox.place(relx=0.5, rely=0.5, anchor=CENTER, height=200)
    def viewDataShow():
        dataShowText = ""
        dataShowText = dataShowText +f"Data in {dataName}\n"
        for key in dataJSON["data"][dataName]:
            dataShowText = dataShowText + f"\t{key} : {dataJSON['data'][dataName][key]}\n"
        textbox.delete(1.0, END)
        textbox.insert(END, dataShowText)
    button_proccessData = Button(root, text="Show data",relief=FLAT ,font=("@Yu Gothic UI Semibold", 20, "normal"), width=20,command=viewDataShow)
    button_proccessData.place(relx=0.5, rely=0.9, anchor=CENTER)

    root.mainloop()

def deleteData(usernameDataGave):
    pass


def exportData(usernameDataGave):
    pass


def workWithFiles():
    pass

loginAndSignUp()
handlerWhatTo("Hamzah Sajid")