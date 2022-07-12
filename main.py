# Importing modules
import json
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import shutil
import datetime
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


def incrementFile(destinationPath, fileNameJust):
    if os.path.isfile(destinationPath+"\\"+fileNameJust):
        i = 1
        while os.path.isfile(destinationPath+"\\"+fileNameJust):
            fileNameJust, fileExtension = os.path.splitext(fileNameJust)
            if f"({i-1})" in fileNameJust:
                fileNameJust = fileNameJust[:-4]+" ("+str(i)+")"+fileExtension
            else:
                fileNameJust = fileNameJust+" ("+str(i)+")"+fileExtension
            i += 1
    return destinationPath + "\\"+fileNameJust

if os.path.isfile('accounts.json'):
    pass
else:
    os.system('echo {"accounts":{}} > accounts.json')

def loginAndSignUp():
    root = Tk()
    label_msg = Label(root, text="", fg="red", bg=color,
                    font=("Arial", 13, "bold"))
    userEntryMode = "login"
    button_Login = Button()

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
            decryptedPassword = main_functions.decryptData(
                username, encryptedPassword)
            if password == decryptedPassword:
                label_msg["fg"] = "lime"
                label_msg["text"] = "Logged In successfully"
                messagebox.showinfo("Login Successful",
                                    "You are now logged in")
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
                encryptedPassword = main_functions.encryptText(
                    username, password)
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

    label_Title = Label(root, text="Data Manager", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)

    label_whatToDo = Label(root, text="What You Want To Do? ", bg=color, font=(
        "@Yu Gothic UI Semibold", 20, "normal"))
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
            workWithFiles(usernameFromData)

    button_go = Button(root, text="Go!", relief="flat", bg="#70CED4", width=30, height=1,
                       font=("@Yu Gothic UI Semibold", 15, "bold"), command=changeScript)
    button_go.place(relx=0.5, rely=0.7, anchor=CENTER)

    root.mainloop()


def workWithData(usernameGave):
    root = Tk()
    root.geometry("600x400")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Work With Data", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.1, anchor=CENTER)
    label_Operations = ttk.Combobox(root, values=["Create Data", "View Data", "Delete Data", "Export Data"],
                                    state="readonly", font=("@Yu Gothic UI Semibold", 15, "normal"))
    label_Operations.place(relx=0.5, rely=0.35, anchor=CENTER)
    label_Operations.current(0)

    def back():
        root.destroy()
        handlerWhatTo(usernameGave)
    button_back = Button(root, text="Back", font=("@Yu Gothic UI Semibold", 10, "normal"),fg="white", bg="#31A3E2", command=back)
    button_back.place(relx=0.01, rely=0.03)
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
    button_Do.place(relx=0.5, rely=0.55, anchor=CENTER)
    root.mainloop()


def makeData(usernameDataGave):
    root = Tk()
    root.geometry("600x500")
    root.title("Data Manager")
    root.configure(bg=color)
    label_Title = Label(root, text="Create Data", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
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
                messagebox.showinfo("Data Successfully stored",
                                    "We have successfully saved your data!")
            else:
                messagebox.showerror("Data not given properly",
                                     "Please check if the data give is respectively to the label, there are blank spaces.")
        else:
            messagebox.showerror("Data not given properly",
                                 "Please check if the data name is not empty and the label and data are not empty")

    button_createData = Button(root, text="Create Data", font=("@Yu Gothic UI Semibold", 15, "normal"), relief=FLAT,
                               bg="#70CED4", fg="white", command=makeDataNew)
    button_createData.place(relx=0.5, rely=0.7, anchor=CENTER)
    root.mainloop()


def viewData(usernameDataGave):
    root = Tk()
    root.geometry("600x500")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="View Data", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    data = []
    with open(str(os.getcwd()) + "\\Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)
    for key in dataJSON["data"]:
        data.append(key)
    comboxbox_options = ttk.Combobox(root, values=data, font=(
        "@Yu Gothic UI Semibold", 20, "bold"), state="readonly")
    comboxbox_options.place(relx=0.5, rely=0.2, anchor=CENTER)
    try:
        comboxbox_options.current(0)
    except:
        pass
    textbox = Text(root, font=("calbri", 10, "normal"), width=75)
    textbox.place(relx=0.5, rely=0.5, anchor=CENTER, height=200)

    def viewDataShow():
        dataName = comboxbox_options.get()
        if dataName != "All":
            dataShowText = ""
            dataShowText = dataShowText + f"Data in {dataName}\n"
            for key in dataJSON["data"][dataName]:
                dataShowText = dataShowText + \
                    f"\t{key} : {dataJSON['data'][dataName][key]}\n"
                textbox.delete(1.0, END)
                textbox.insert(END, dataShowText)
    button_proccessData = Button(root, text="Show data", relief=FLAT, font=(
        "@Yu Gothic UI Semibold", 20, "normal"), width=20, command=viewDataShow)
    button_proccessData.place(relx=0.5, rely=0.9, anchor=CENTER)

    root.mainloop()


def deleteData(usernameDataGave):
    root = Tk()
    root.geometry("600x500")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Delete Data", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    data = []
    with open(str(os.getcwd()) + "\\Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)
    for key in dataJSON["data"]:
        data.append(key)
    if len(data) != 0:
        data.append("All")

    comboxbox_options = ttk.Combobox(root, values=data, font=(
        "@Yu Gothic UI Semibold", 20, "bold"), state="readonly")
    comboxbox_options.place(relx=0.5, rely=0.2, anchor=CENTER)
    try:
        comboxbox_options.current(0)
    except:
        pass
    textbox = Text(root, font=("calbri", 10, "normal"), width=75,)
    textbox.place(relx=0.5, rely=0.5, anchor=CENTER, height=200)
    def viewDataDel():
        dataName = comboxbox_options.get()
        if dataName != "All" and dataName != "":
            dataShowText = ""
            dataShowText = dataShowText + f"Data in {dataName}\n"
            for key in dataJSON["data"][dataName]:
                dataShowText = dataShowText + \
                    f"\t{key} : {dataJSON['data'][dataName][key]}\n"
                textbox.delete(1.0, END)
                textbox.insert(END, dataShowText)
        elif dataName != "" and dataName == "All":
            dataShowText = "Data:"
            for key in dataJSON["data"]:
                dataShowText = dataShowText + "\nData in " + key + ":\n"
                for key2 in dataJSON["data"][key]:
                    dataShowText = dataShowText + "\t"+key2 + " : " +dataJSON["data"][key][key2] + "\n"
            textbox.delete(1.0, END)
            textbox.insert(END, dataShowText)
    if len(data) != 0:
        viewDataDel()
    def callData(event):
        viewDataDel()
    comboxbox_options.bind("<<ComboboxSelected>>", callData)

    def deleteDataShow():
        dataName = comboxbox_options.get()
        deletedataPrompt = messagebox.showwarning(
            "Delete Data", "Are you sure that you want to delete "+dataName+" ?")
        print(deletedataPrompt)
        if deletedataPrompt:
            if dataName != "All":
                del dataJSON["data"][dataName]
                with open(str(os.getcwd()) + "\\Data\\" + usernameDataGave + "\\" + "data.json", "w") as f:
                    json.dump(dataJSON, f)
                root.destroy()
                deleteData(usernameDataGave)
            elif dataName == "All":
                dataJSON = {"data":{}}
                with open(str(os.getcwd()) + "\\Data\\" + usernameDataGave + "\\" + "data.json", "w") as f:
                    json.dump(dataJSON, f)
                messagebox.showinfo("Successfully Deleted", "We have successfully deleted all the data.")
                root.destroy()
                deleteData(usernameDataGave)
        else:
            pass

    button_proccessData = Button(root, text="Delete data", relief=FLAT, font=("@Yu Gothic UI Semibold", 20, "normal"),
                                 width=20, command=deleteDataShow)
    button_proccessData.place(relx=0.5, rely=0.9, anchor=CENTER)

    root.mainloop()


def exportData(usernameDataGave):
    root = Tk()
    root.geometry("600x500")
    root.title("Data Manager")
    root.configure(bg=color)
    root.eval('tk::PlaceWindow . center')

    label_Title = Label(root, text="Export Data", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    data = []
    with open(str(os.getcwd()) + "\\Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)
    for key in dataJSON["data"]:
        data.append(key)
    if len(data) != 0:
        data.append("All")
    comboxbox_options = ttk.Combobox(root, values=data, font=(
        "@Yu Gothic UI Semibold", 20, "bold"), state="readonly")
    comboxbox_options.place(relx=0.5, rely=0.2, anchor=CENTER)
    try:
        comboxbox_options.current(0)
    except:
        print("error")
    textbox = Text(root, font=("calbri", 10, "normal"), width=75,)
    textbox.place(relx=0.5, rely=0.5, anchor=CENTER, height=200)

    def exportDataWork():
        folder = filedialog.askdirectory(title="Select folder")
        dataName = comboxbox_options.get()
        if dataName != "" and dataName != "All":
            if dataName in dataJSON["data"]:
                dataName2 = dataName + ".txt"
                endDestination = incrementFile(str(folder), dataName2)
                print(endDestination)
                with open(endDestination, "w") as f:
                    f.write("Your data in " + dataName + ":\n")
                    for key in dataJSON["data"][dataName]:
                        f.write(key + " : " +
                                dataJSON["data"][dataName][key] + "\n")
                    f.close()
                    messagebox.showinfo(
                        "successfully exported data", f"We have successfully exported data of {dataName}")
            else:
                messagebox.showerror(
                    "Something went wrong please contact our engineers!")
        elif dataName != "" and dataName == "All":
            fileName = "All Exported Data.txt"
            finalDest = incrementFile(folder, fileName)
            f = open(finalDest, "w")
            f.write("Your data:")
            for key in dataJSON["data"]:
                print(key)
                f.write("\nData in " + key + ":\n")
                for key2 in dataJSON["data"][key]:
                    f.write("\t"+key2 + " : " +
                            dataJSON["data"][key][key2] + "\n")
            f.close()
            messagebox.showinfo("successfully exported data",
                                "We have successfully exported all the data")
    button_proccessData = Button(root, text="Export data", relief=FLAT, font=("@Yu Gothic UI Semibold", 20, "normal"),
                                 width=20, command=exportDataWork)
    button_proccessData.place(relx=0.5, rely=0.9, anchor=CENTER)

    def viewDataExport():
        dataName = comboxbox_options.get()
        if dataName != "All" and dataName != "":
            dataShowText = ""
            dataShowText = dataShowText + f"Data in {dataName}\n"
            for key in dataJSON["data"][dataName]:
                dataShowText = dataShowText + \
                    f"\t{key} : {dataJSON['data'][dataName][key]}\n"
                textbox.delete(1.0, END)
                textbox.insert(END, dataShowText)
        elif dataName == "All" and dataName != "":
            dataShowText = ""
            dataShowText = dataShowText + "Your data:"
            for key in dataJSON["data"]:
                dataShowText = dataShowText + "\nData in " + key + ":\n"
                for key2 in dataJSON["data"][key]:
                    dataShowText = dataShowText + "\t"+key2 + \
                        " : " + dataJSON["data"][key][key2] + "\n"
            textbox.delete(1.0, END)
            textbox.insert(END, dataShowText)
    if len(data) != 0:
        viewDataExport()
    def callData(event):
        viewDataExport()
    comboxbox_options.bind("<<ComboboxSelected>>", callData)



def workWithFiles(usernameGave):
    if not os.path.exists(str(os.getcwd())+"\\Data\\"+usernameGave+"\\"+"Files"):
        os.makedirs(str(os.getcwd())+"\Data\\"+usernameGave+"\\"+"Files")
    else:
        pass

    root = Tk()
    root.geometry("600x400")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Work With File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.1, anchor=CENTER)
    label_Operations = ttk.Combobox(root, values=["Upload File", "View File", "Delete File", "Export File"],
                                    state="readonly", font=("@Yu Gothic UI Semibold", 15, "normal"))
    label_Operations.place(relx=0.5, rely=0.35, anchor=CENTER)
    label_Operations.current(0)
    def back():
        root.destroy()
        handlerWhatTo(usernameGave)
    button_back = Button(root, text="Back", font=(
        "@Yu Gothic UI Semibold", 10, "normal"), fg="white", bg="#31A3E2",command=back)
    button_back.place(relx=0.01, rely=0.03)
    def changeScreen():
        if label_Operations.get() == "Upload File":
            uploadFile(usernameGave)
        elif label_Operations.get() == "View File":
            viewFile(usernameGave)
        elif label_Operations.get() == "Delete File":
            deleteFile(usernameGave)
        elif label_Operations.get() == "Export File":
            exportFile(usernameGave)

    button_Do = Button(root, text="Continue", font=("@Yu Gothic UI Semibold", 13, "normal"), command=changeScreen,
                       relief="flat", bg="#70CED4", fg="white")
    button_Do.place(relx=0.5, rely=0.55, anchor=CENTER)
    root.mainloop()

def uploadFile(usernameDataGave):
    root = Tk()
    root.geometry("600x300")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Upload File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)

    def saveFile():
        try:
            fileNames = filedialog.askopenfilenames(parent=root, title="Select file",)
            fileNames = list(fileNames)
            if fileNames != []:
                for file in fileNames:
                    orignal = file
                    target = incrementFile(str(os.getcwd())+"\\Data\\"+usernameDataGave+"\\" + "Files\\", os.path.basename(file))
                    shutil.copyfile(orignal,target)
                messagebox.showinfo("File saved", "We have successfully saved you file/files!")
            else:
                messagebox.showerror("File not gave", "You have not provided us with the file.")
        except FileNotFoundError:
            messagebox.showerror("File not found", "We didn't found the expected file gave by you!")
    button_uploadFile = Button(root, text="Upload File", relief="flat", font=(
        "@Yu Gothic UI Semibold", 16, "normal"),command=saveFile)
    button_uploadFile.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()


def viewFile(usernameDataGave):
    root = Tk()
    root.geometry("600x300")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="View File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    fileData = []
    for file in os.listdir(str(os.getcwd())+"\Data\\"+usernameDataGave+"\\"+"Files"):
        fileData.append(file)
    if len(fileData) != 0:
        fileData.append("All")
    comboxbox_options = ttk.Combobox(root, values=fileData, font=(
        "@Yu Gothic UI Semibold", 20, "bold"), state="readonly")
    comboxbox_options.place(relx=0.5, rely=0.35, anchor=CENTER)
    try:
        comboxbox_options.current(0)
    except:
        pass
    def viewFileWork():
        fileNameGot = comboxbox_options.get()
        if fileNameGot != "" and fileNameGot != "All":
            os.startfile(str(os.getcwd())+"\Data\\"+usernameDataGave+"\\"+"Files\\" +fileNameGot)
        elif fileNameGot == "" and fileNameGot == "All":
            for x in fileData:
                os.startfile(str(os.getcwd())+"\Data\\" + usernameDataGave+"\\"+"Files\\" + x)
    button_uploadFile = Button(root, text="View File", relief="flat", font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=viewFileWork)
    button_uploadFile.place(relx=0.5, rely=0.6, anchor=CENTER)
    root.mainloop()


def deleteFile(usernameDataGave):
    root = Tk()
    root.geometry("600x300")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Delete File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    fileData = []
    for file in os.listdir(str(os.getcwd())+"\Data\\"+usernameDataGave+"\\"+"Files"):
        fileData.append(file)
    if len(fileData) != 0:
        fileData.append("All")
    comboxbox_options = ttk.Combobox(root, values=fileData, font=(
        "@Yu Gothic UI Semibold", 20, "bold"), state="readonly")
    comboxbox_options.place(relx=0.5, rely=0.35, anchor=CENTER)
    try:
        comboxbox_options.current(0)
    except:
        pass

    def deleteFileWork():
        dataName = comboxbox_options.get()
        deletedataPrompt = messagebox.showwarning("Delete Data", "Are you sure that you want to delete "+dataName+" ?")
        try:
            if dataName != "" and dataName != "All":
                if deletedataPrompt:
                    os.remove(str(os.getcwd())+"\Data\\" +
                            usernameDataGave+"\\"+"Files\\" + dataName)
                    messagebox.showinfo("Successfully Delete", "We have successfully deleted the file")
                    root.destroy()
                    deleteFile(usernameDataGave)
                else:
                    pass
            elif dataName != "" and dataName == "All":
                for x in os.listdir(str(os.getcwd())+"\Data\\" + usernameDataGave+"\\"+"Files\\"):
                    os.remove(str(os.getcwd())+"\Data\\" +usernameDataGave+"\\"+"Files\\" + x)
                messagebox.showinfo("Successfully Delete","We have successfully deleted the file")
                root.destroy()
                deleteFile(usernameDataGave)

        except:
            pass

    def viewdeleteFileWork():
        fileNameGot = comboxbox_options.get()
        if fileNameGot != "" and fileNameGot != "All":
            os.startfile(str(os.getcwd())+"\Data\\" +
                         usernameDataGave+"\\"+"Files\\" + fileNameGot)
        elif fileNameGot == "" and fileNameGot == "All":
            for x in fileData:
                os.startfile(str(os.getcwd())+"\Data\\" +
                             usernameDataGave+"\\"+"Files\\" + x)
    button_uploadFile = Button(root, text="Delete File", relief="flat", font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=deleteFileWork)
    button_uploadFile.place(relx=0.2, rely=0.6)
    button_showGoingToDeleteFile = Button(root, text="Show File", relief=FLAT,font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=viewdeleteFileWork)
    button_showGoingToDeleteFile.place(relx=0.6, rely=0.6)
    root.mainloop()


def exportFile(usernameDataGave):
    root = Tk()
    root.geometry("600x300")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Export File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    fileData = []
    for file in os.listdir(str(os.getcwd())+"\Data\\"+usernameDataGave+"\\"+"Files"):
        fileData.append(file)
    if len(fileData) != 0:
        fileData.append("All")
    comboxbox_options = ttk.Combobox(root, values=fileData, font=(
        "@Yu Gothic UI Semibold", 20, "bold"), state="readonly")
    comboxbox_options.place(relx=0.5, rely=0.35, anchor=CENTER)
    try:
        comboxbox_options.current(0)
    except:
        pass

    def exportFileWork():
        username = usernameDataGave
        askedFilename = comboxbox_options.get()
        folder = filedialog.askdirectory(title="Select folder")
        if askedFilename in os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\"):
            shutil.copy(str(os.getcwd())+"\Data\\"+username+"\\" +"Files\\"+askedFilename, folder+"\\"+askedFilename)
            messagebox.showinfo("Successfully exported file", "We have successfully exported "+askedFilename+" file.")
        elif askedFilename == "All":
            if len(os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\")) != 1:
                datetimeGen = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                exportFolder = folder+"\\" + datetimeGen+" Exported Files"
                os.mkdir(exportFolder)
                for file in os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\"):
                    shutil.copy(str(os.getcwd())+"\Data\\"+username +"\\"+"Files\\"+file, exportFolder+"\\"+file)
                messagebox.showinfo("Successfully exported files", "We have successfully exported all files.")
            else:
                for file in os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\"):
                    shutil.copy(str(os.getcwd())+"\Data\\"+username + "\\"+"Files\\"+file, folder+"\\"+file)
                messagebox.showinfo("Successfully exported files", "We have successfully exported all file.")


    def viewdeleteFileWork():
        fileNameGot = comboxbox_options.get()
        if fileNameGot != "" and fileNameGot != "All":
            os.startfile(str(os.getcwd())+"\Data\\" +
                         usernameDataGave+"\\"+"Files\\" + fileNameGot)
        elif fileNameGot == "" and fileNameGot == "All":
            for x in fileData:
                os.startfile(str(os.getcwd())+"\Data\\" +
                             usernameDataGave+"\\"+"Files\\" + x)
    button_uploadFile = Button(root, text="Export File", relief="flat", font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=exportFileWork)
    button_uploadFile.place(relx=0.2, rely=0.6)
    button_showGoingToDeleteFile = Button(root, text="Show File", relief=FLAT, font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=viewdeleteFileWork)
    button_showGoingToDeleteFile.place(relx=0.6, rely=0.6)
    root.mainloop()


loginAndSignUp()