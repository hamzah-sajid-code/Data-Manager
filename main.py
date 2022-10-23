import json
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import shutil
import datetime
import hashlib
from cryptography.fernet import Fernet

color = "#CAF1DE"

appdatapath = os.getenv('APPDATA')
temp_folder = os.getenv("TEMP")

main_destination = f"{appdatapath}\\Data Manager DB\\"
if os.path.isdir(main_destination):
    pass
else:
    os.system(f"mkdir \"{main_destination}\"")

accounts_file = main_destination+"accounts.json"

if os.path.isfile(accounts_file):
        pass
else:
    os.system('echo {"accounts":{}} > accounts.json')
    os.system(f'copy accounts.json "{main_destination}"')
    os.remove("accounts.json")

def SHA512(data):
    sha256Form = hashlib.sha512(data.encode()).hexdigest()
    return sha256Form


def GenerateKey():
    f = Fernet.generate_key()
    return {"key_in_bytes": f, "key_in_string": str(f.decode())}


def DataManage(key, string, do="encryption"):
    if type(key) == bytes: pass
    else: key = key.encode("utf-8")
    fernetKey = Fernet(key)
    if do == "encryption":
        string = string.encode()
        encrypted = fernetKey.encrypt(string)
        return str(encrypted.decode())
    elif do == "decryption":
        if type(string) == bytes:
            pass
        else:
            string = string.encode()
        decrypted = fernetKey.decrypt(string)
        return str(decrypted.decode())


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
    return destinationPath +"\\"+ fileNameJust.replace("\\", "")

userEntryMode = "login"
userName = ""
def logout(win):
    os.remove(temp_folder+"\\temp_datamanager")
    win.destroy()
    main()
def loginAndSignUp():
    global userName
    root = Tk()
    root.title("Data Manager")
    root.geometry("600x500")
    root.configure(bg="#CAF1DE")
    label_msg = Label(root, text="", fg="red", bg=color,
                      font=("Arial", 13, "bold"))
    button_Login = Button()
    def change(username):
        root.destroy()
        handlerWhatTo(username)

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

    with open(main_destination+'accounts.json') as json_file:
        accountsData = json.load(json_file)
    def handle():
        global userName
        if userEntryMode == "login":
            login()
        elif userEntryMode == "signup":
            signup()


    def login():
        global userName
        username = input_Username.get()
        password = input_Password.get()
        if username in accountsData["accounts"]:
            encryptedPassword = accountsData["accounts"][username][0]
            if encryptedPassword == SHA512(password):
                d = f"{username} | {password}"
                with open(f"{temp_folder}/temp_datamanager", "w+") as f:
                    f.write(d)
                label_msg["fg"] = "lime"
                label_msg["text"] = "Logged In successfully"
                messagebox.showinfo("Login Successful","You are now logged in",parent=root)
                userName = username
                change(username)
            else:
                label_msg["fg"] = "red"
                label_msg["text"] = "Username password is wrong! Please try again."
                messagebox.showerror("Wrong password", "Username password is wrong! Please try again.",parent=root)
                
        else:
            label_msg["fg"] = "red"
            label_msg["text"] = "Username does not exists! Please try again."
            messagebox.showerror(
                "Username not found", "Username does not exists! Please try again.", parent=root)
            
            return username
    button_Login["command"] = handle

    def signup():
        username = input_Username.get()
        password = input_Password.get()
        usernameData = username
        if username != "" and password != "":
            if username in accountsData["accounts"]:
                label_msg["fg"] = "red"
                label_msg["text"] = "Username already exists. Please try again."
            else:
                encryptedPassword = SHA512(password)
                key = GenerateKey()
                accountsData["accounts"][username] = encryptedPassword, key["key_in_string"]
                with open(main_destination+'accounts.json', 'w') as outfile:
                    json.dump(accountsData, outfile)
                os.system("cls")
                os.system(f'mkdir \"{main_destination}Data\\{username}\"')
                with open(main_destination + "Data\\" + username + "\\" + "data.json", "w") as f:
                    f.write("{\"data\": {}}")
                username = usernameData
                label_msg["fg"] = "lime"
                label_msg["text"] = "Account Successful created"
                messagebox.showinfo("Account created Successful","Your account is successfully make now we're logging you in",parent=root)
                
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
    button_logout = Button(root, text="Log Out", font=("@Yu Gothic UI Semibold", 12, "bold"), relief="flat", bg="white", command=lambda: logout(root))
    button_logout.place(relx=0.01, rely=0.01)
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
    button_back = Button(root, text="Back", font=(
        "@Yu Gothic UI Semibold", 10, "normal"), fg="white", bg="#31A3E2", command=back)
    button_back.place(relx=0.01, rely=0.03)
    button_logout = Button(root, text="Log Out", font=(
        "@Yu Gothic UI Semibold", 12, "bold"), relief="flat", bg="white", command=lambda: logout(root))
    button_logout.place(relx=0.87, rely=0.01)
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

    with open(main_destination+"Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)
    with open(main_destination + "accounts.json") as json_file:
        accountsJSON = json.load(json_file)
    key = accountsJSON["accounts"][usernameDataGave][1]
    def makeDataNew():
        nameDataIn = input_DataName.get()
        nameDataIn = DataManage(key, nameDataIn, do="encryption")
        labelIn = input_Labels.get().split(" | ")
        labelIn = [(DataManage(key,x,do="encryption")) for x in labelIn]
        dataIn = input_data.get().split(" | ")
        dataIn = [(DataManage(key, y, do="encryption")) for y in dataIn]
        if nameDataIn != "" and len(labelIn) != 0 and len(dataIn) != 0:
            if len(labelIn) == len(labelIn):
                finalData = {}
                dataDict = dict(zip(labelIn, dataIn))
                finalData[nameDataIn] = dataDict
                dataJSON["data"].update(finalData)
                with open(main_destination+ "Data\\" + usernameDataGave + "\\" + "data.json", "w") as f:
                    json.dump(dataJSON, f)
                
                messagebox.showinfo("Data Successfully stored", "We have successfully saved your data!", parent=root)

            else:
                
                messagebox.showerror(
                    "Data not given properly", "Please check if the data give is respectively to the label, there are blank spaces.", parent=root)
        else:
            
            messagebox.showerror("Data not given properly",
                                 "Please check if the data name is not empty and the label and data are not empty", parent=root)
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
    with open(main_destination+ "Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)
    with open(main_destination+ "accounts.json") as json_file:
        accountsJSON = json.load(json_file)
    key = accountsJSON["accounts"][usernameDataGave][1]
    # Decryption Data
    mainData = {"data":{}}
    for keyData in dataJSON["data"]:
        dataNameKey = []
        dataNameData = []
        realkeyData = DataManage(key, keyData, do="decryption")
        for dataGotKey in dataJSON["data"][keyData]:

            dataNameKey.append(DataManage(key, dataGotKey, do="decryption"))
            dataNameData.append(DataManage(key, dataJSON["data"][keyData][dataGotKey], do="decryption"))
        mainData["data"][realkeyData] = dict(zip(dataNameKey, dataNameData))
    
    data = []
    for key in mainData["data"]:
        data.append(key)
    if len(data) > 1:
        data.append("All")
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
            for keyInDataDict in mainData["data"][dataName]:
                dataShowText = dataShowText + \
                    f"\t{keyInDataDict} : {mainData['data'][dataName][keyInDataDict]}\n"
                textbox.delete(1.0, END)
                textbox.insert(END, dataShowText)
        elif dataName != "" and dataName == "All":
            dataShowText = "Data:"
            for key in mainData["data"]:
                dataShowText = dataShowText + "\nData in " + key + ":\n"
                for key2 in mainData["data"][key]:
                    dataShowText = dataShowText + "\t"+key2 + \
                        " : " + mainData["data"][key][key2] + "\n"
            textbox.delete(1.0, END)
            textbox.insert(END, dataShowText)
    viewDataShow()
    def callData(event):
        viewDataShow()
    comboxbox_options.bind("<<ComboboxSelected>>", callData)
    root.mainloop()


def deleteData(usernameDataGave):
    root = Tk()
    root.geometry("600x500")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Delete Data", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    with open(main_destination+ "Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)
    with open(main_destination+ "accounts.json") as json_file:
        accountsJSON = json.load(json_file)
    
    keyEncryptor = accountsJSON["accounts"][usernameDataGave][1]
    # Decryption Data
    mainData = {"data": {}}
    for keyData in dataJSON["data"]:
        dataNameKey = []
        dataNameData = []
        realkeyData = DataManage(keyEncryptor, keyData, do="decryption")
        for dataGotKey in dataJSON["data"][keyData]:

            dataNameKey.append(DataManage(keyEncryptor, dataGotKey, do="decryption"))
            dataNameData.append(DataManage(
                keyEncryptor, dataJSON["data"][keyData][dataGotKey], do="decryption"))
        mainData["data"][realkeyData] = dict(zip(dataNameKey, dataNameData))

    data = []
    for key in mainData["data"]:
        data.append(key)
    if len(data) > 1:
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
            for key in mainData["data"][dataName]:
                dataShowText = dataShowText + \
                    f"\t{key} : {mainData['data'][dataName][key]}\n"
                textbox.delete(1.0, END)
                textbox.insert(END, dataShowText)
        elif dataName != "" and dataName == "All":
            dataShowText = "Data:"
            for key in mainData["data"]:
                dataShowText = dataShowText + "\nData in " + key + ":\n"
                for key2 in mainData["data"][key]:
                    dataShowText = dataShowText + "\t"+key2 + \
                        " : " + mainData["data"][key][key2] + "\n"
            textbox.delete(1.0, END)
            textbox.insert(END, dataShowText)
    if len(data) != 0:
        viewDataDel()

    def callData(event):
        viewDataDel()
    comboxbox_options.bind("<<ComboboxSelected>>", callData)

    def deleteDataShow():
        dataName = comboxbox_options.get()
        
        deletedataPrompt = messagebox.askyesno(
            "Delete Data", "Are you sure that you want to delete "+dataName+" ?", parent=root)
        if deletedataPrompt:
            if dataName != "All":
                indexOfKey = list(mainData["data"]).index(dataName)
                dictDataKey = list(mainData["data"])[indexOfKey]
                dataJSON = {"data":{}}
                del mainData["data"][dictDataKey]

                # Encryption Data
                for keyDataE in mainData["data"]:
                    dataNameKey = []
                    dataNameData = []
                    realkeyData = DataManage(keyEncryptor, keyDataE, do="encryption")
                    for dataGotKey in mainData["data"][keyDataE]:

                        dataNameKey.append(DataManage(keyEncryptor, dataGotKey, do="encryption"))
                        dataNameData.append(DataManage(keyEncryptor, mainData["data"][keyDataE][dataGotKey], do="encryption"))
                    dataJSON["data"][realkeyData] = dict(zip(dataNameKey, dataNameData))

                with open(main_destination+ "Data\\" + usernameDataGave + "\\" + "data.json", "w") as f:
                    json.dump(dataJSON, f)
                root.destroy()
                deleteData(usernameDataGave)
            else:
                dataJSON = {"data": {}}
                with open(main_destination+ "Data\\" + usernameDataGave + "\\" + "data.json", "w") as f:
                    json.dump(dataJSON, f)
                messagebox.showinfo("Successfully Deleted",
                                    "We have successfully deleted all the data.", parent=root)
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
    # root.eval('tk::PlaceWindow . center')

    label_Title = Label(root, text="Export Data", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    data = []
    with open(main_destination+ "Data\\" + usernameDataGave + "\\" + "data.json") as json_file:
        dataJSON = json.load(json_file)
    with open(main_destination+ "accounts.json") as json_file:
        accountsJSON = json.load(json_file)
    keyEncryptor = accountsJSON["accounts"][usernameDataGave][1]
    # Decryption Data
    mainData = {"data": {}}
    for keyData in dataJSON["data"]:
        dataNameKey = []
        dataNameData = []
        realkeyData = DataManage(keyEncryptor, keyData, do="decryption")
        for dataGotKey in dataJSON["data"][keyData]:

            dataNameKey.append(DataManage(
                keyEncryptor, dataGotKey, do="decryption"))
            dataNameData.append(DataManage(
                keyEncryptor, dataJSON["data"][keyData][dataGotKey], do="decryption"))
        mainData["data"][realkeyData] = dict(zip(dataNameKey, dataNameData))
    for key in mainData["data"]:
        data.append(key)
    if len(data) > 1:
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

    def exportDataWork():
        
        folder = filedialog.askdirectory(title="Select folder", parent=root)
        dataName = comboxbox_options.get()
        if dataName != "" and dataName != "All":
            if dataName in mainData["data"]:
                dataName2 = dataName + ".txt"
                endDestination = incrementFile(str(folder), dataName2)
                with open(endDestination, "w") as f:
                    f.write("Your data in " + dataName + ":\n")
                    for key in mainData["data"][dataName]:
                        f.write("\t"+key + " : " +
                                mainData["data"][dataName][key] + "\n")
                    f.close()
                    
                    messagebox.showinfo(
                        "successfully exported data", f"We have successfully exported data of {dataName}", parent=root)

            else:
                
                messagebox.showerror(
                    "Something went wrong please contact our engineers!", parent=root)
        elif dataName != "" and dataName == "All":
            fileName = "All Exported Data.txt"
            finalDest = incrementFile(folder, fileName)
            f = open(finalDest, "w")
            f.write("Your data:")
            for key in mainData["data"]:
                f.write("\nData in " + key + ":\n")
                for key2 in mainData["data"][key]:
                    f.write("\t"+key2 + " : " +
                            mainData["data"][key][key2] + "\n")
            f.close()
            
            messagebox.showinfo("successfully exported data",
                                "We have successfully exported all the data", parent=root)

    button_proccessData = Button(root, text="Export data", relief=FLAT, font=("@Yu Gothic UI Semibold", 20, "normal"),
                                 width=20, command=exportDataWork)
    button_proccessData.place(relx=0.5, rely=0.9, anchor=CENTER)

    def viewDataExport():
        dataName = comboxbox_options.get()
        if dataName != "All" and dataName != "":
            dataShowText = ""
            dataShowText = dataShowText + f"Data in {dataName}\n"
            for key in mainData["data"][dataName]:
                dataShowText = dataShowText + \
                    f"\t{key} : {mainData['data'][dataName][key]}\n"
                textbox.delete(1.0, END)
                textbox.insert(END, dataShowText)
        elif dataName == "All" and dataName != "":
            dataShowText = ""
            dataShowText = dataShowText + "Your data:"
            for key in mainData["data"]:
                dataShowText = dataShowText + "\nData in " + key + ":\n"
                for key2 in mainData["data"][key]:
                    dataShowText = dataShowText + "\t"+key2 + \
                        " : " + mainData["data"][key][key2] + "\n"
            textbox.delete(1.0, END)
            textbox.insert(END, dataShowText)
    if len(data) != 0:
        viewDataExport()

    def callData(event):
        viewDataExport()
    comboxbox_options.bind("<<ComboboxSelected>>", callData)
    root.mainloop()

# Work with file


def FileManage(keyUse, file_loc, action="encryption", change_name="no"):
    if action == "encryption":
        keyFernet = Fernet(keyUse)
        with open(file_loc, "rb") as file:
            data = file.read()
        encrypted_data = keyFernet.encrypt(data)

        with open(file_loc, "wb") as file:
            file.write(encrypted_data)
        if change_name != "no":
            encrypted_name = DataManage(keyUse, str(os.path.basename(file_loc)))
            os.rename(file_loc, os.path.dirname(os.path.realpath(file_loc))+ "\\"+encrypted_name)

    elif action == "decryption":
        keyFernet = Fernet(keyUse)
        with open(file_loc, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = keyFernet.decrypt(encrypted_data)

        with open(file_loc, "wb") as file:
            file.write(decrypted_data)
        if change_name != "no":
            decrypted_name = DataManage(keyUse, str(os.path.basename(file_loc)), do="decryption")
            os.rename(file_loc, os.path.dirname(os.path.realpath(file_loc))
                      + "\\"+decrypted_name)
    elif action == "showrealname":
        keyFernet = Fernet(keyUse)
        decrypted_name = DataManage(keyUse, str(os.path.basename(file_loc)), do="decryption")
        return decrypted_name


def workWithFiles(usernameGave):
    if not os.path.exists(main_destination+"Data\\"+usernameGave+"\\"+"Files"):
        os.makedirs(main_destination+"Data\\"+usernameGave+"\\"+"Files")
    else:
        pass

    root = Tk()
    root.geometry("600x400")
    root.title("Data Manager")
    root.configure(bg=color)

    with open(accounts_file) as json_file:
            accountsJSON = json.load(json_file)

    label_Title = Label(root, text="Work With File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.1, anchor=CENTER)
    label_Operations = ttk.Combobox(root, values=["Upload File", "View File", "Delete File", "Export File"],
                                    state="readonly", font=("@Yu Gothic UI Semibold", 15, "normal"))
    label_Operations.place(relx=0.5, rely=0.35, anchor=CENTER)
    label_Operations.current(0)
    button_logout = Button(root, text="Log Out", font=(
        "@Yu Gothic UI Semibold", 12, "bold"), relief="flat", bg="white", command=lambda: logout(root))
    button_logout.place(relx=0.87, rely=0.01)
    def back():
        root.destroy()
        handlerWhatTo(usernameGave)
    button_back = Button(root, text="Back", font=(
        "@Yu Gothic UI Semibold", 10, "normal"), fg="white", bg="#31A3E2", command=back)
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
        with open(main_destination+ "accounts.json") as json_file:
            accountsJSON = json.load(json_file)
        keyEncryptor = accountsJSON["accounts"][usernameDataGave][1]
        try:
            
            fileNames = filedialog.askopenfilenames(parent=root, title="Select file")
            fileNames = list(fileNames)
            if fileNames != []:
                for file in fileNames:
                    orignal = file
                    target = incrementFile(main_destination+"Data\\"+usernameDataGave+"\\" + "Files\\",os.path.basename(file))
                    shutil.copy(orignal, target)
                    FileManage(keyEncryptor, target)
                
                messagebox.showinfo(
                    "File saved", "We have successfully saved you file/files!", parent=root)
            else:
                
                messagebox.showerror(
                    "File not gave", "You have not provided us with the file.", parent=root)
        except FileNotFoundError:
            
            messagebox.showerror(
                "File not found", "We didn't found the expected file gave by you!", parent=root)

    button_uploadFile = Button(root, text="Upload File", relief="flat", font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=saveFile)
    button_uploadFile.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()


def viewFile(usernameDataGave):
    with open(main_destination+ "accounts.json") as json_file:
        accountsJSON = json.load(json_file)

    keyEncryptor = accountsJSON["accounts"][usernameDataGave][1]

    root = Tk()
    root.geometry("600x300")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="View File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    fileData = []
    for file in os.listdir(main_destination+"Data\\"+usernameDataGave+"\\"+"Files"):
        fileData.append(file)
        FileManage(keyEncryptor, main_destination+"Data\\"+usernameDataGave+"\\"+"Files\\"+file, action="decryption")
    if len(fileData) > 1:
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
            os.startfile(main_destination+"\Data\\" +
                         usernameDataGave+"\\"+"Files\\" + fileNameGot)
        elif fileNameGot != "" and fileNameGot == "All":
            for x in fileData:
                if x != "All":
                    os.startfile(main_destination+"Data\\" +
                                 usernameDataGave+"\\"+"Files\\" + x)
    button_uploadFile = Button(root, text="View File", relief="flat", font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=viewFileWork)
    button_uploadFile.place(relx=0.5, rely=0.6, anchor=CENTER)
    def on_closing():
        for file in os.listdir(main_destination+"Data\\"+usernameDataGave+"\\"+"Files"):
            FileManage(keyEncryptor, main_destination+"Data\\" +usernameDataGave+"\\"+"Files\\"+file)
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def deleteFile(usernameDataGave):
    with open(main_destination+ "accounts.json") as json_file:
        accountsJSON = json.load(json_file)

    keyEncryptor = accountsJSON["accounts"][usernameDataGave][1]

    root = Tk()
    root.geometry("600x300")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Delete File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    fileData = []
    for file in os.listdir(main_destination+"\Data\\"+usernameDataGave+"\\"+"Files"):
        fileData.append(file)
        FileManage(keyEncryptor, main_destination+"Data\\"+usernameDataGave+"\\"+"Files\\"+file, action="decryption")
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
        
        deletedataPrompt = messagebox.askyesno(
            "Delete Data", "Are you sure that you want to delete "+dataName+" ?", parent=root)
        try:
            if dataName != "" and dataName != "All":
                if deletedataPrompt:
                    os.remove(main_destination+"\Data\\" +
                              usernameDataGave+"\\"+"Files\\" + dataName)
                    messagebox.showinfo(
                        "Successfully Delete", "We have successfully deleted the file", parent=root)
                    on_closing()
                    deleteFile(usernameDataGave)
                else:
                    pass
            elif dataName != "" and dataName == "All" and deletedataPrompt:
                for x in os.listdir(main_destination+"\Data\\" + usernameDataGave+"\\"+"Files\\"):
                    os.remove(main_destination+"\Data\\" +
                              usernameDataGave+"\\"+"Files\\" + x)
                messagebox.showinfo("Successfully Delete",
                                    "We have successfully deleted the file", parent=root)
                on_closing()
                deleteFile(usernameDataGave)

        except:
            pass

    def viewdeleteFileWork():
        fileNameGot = comboxbox_options.get()
        if fileNameGot != "" and fileNameGot != "All":
            os.startfile(main_destination+"\Data\\" +usernameDataGave+"\\"+"Files\\" + fileNameGot)
        elif fileNameGot != "" and fileNameGot == "All":
            for x in fileData:
                os.startfile(main_destination+"\Data\\" +usernameDataGave+"\\"+"Files\\" + x)
    button_uploadFile = Button(root, text="Delete File", relief="flat", font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=deleteFileWork)
    button_uploadFile.place(relx=0.2, rely=0.6)
    button_showGoingToDeleteFile = Button(root, text="Show File", relief=FLAT, font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=viewdeleteFileWork)
    button_showGoingToDeleteFile.place(relx=0.6, rely=0.6)

    def on_closing():
        for file in os.listdir(main_destination+"Data\\"+usernameDataGave+"\\"+"Files"):
            FileManage(keyEncryptor, main_destination+"Data\\" +
                       usernameDataGave+"\\"+"Files\\"+file)
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def exportFile(usernameDataGave):
    with open(main_destination+ "accounts.json") as json_file:
        accountsJSON = json.load(json_file)

    keyEncryptor = accountsJSON["accounts"][usernameDataGave][1]
    root = Tk()
    root.geometry("600x300")
    root.title("Data Manager")
    root.configure(bg=color)

    label_Title = Label(root, text="Export File", font=(
        "@Yu Gothic UI Semibold", 30, "bold"), bg=color)
    label_Title.place(relx=0.5, rely=0.07, anchor=CENTER)
    fileData = []
    for file in os.listdir(main_destination+"\Data\\"+usernameDataGave+"\\"+"Files"):
        fileData.append(file)
        FileManage(keyEncryptor, main_destination+"Data\\"+usernameDataGave+"\\"+"Files\\"+file, action="decryption")
    if len(fileData) > 1:
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
        
        folder = filedialog.askdirectory(title="Select folder", parent=root)
        if askedFilename in os.listdir(main_destination+"\\Data\\"+username+"\\"+"Files\\"):
            target = incrementFile(folder, askedFilename)
            shutil.copy(main_destination+"\Data\\"+username+"\\" +"Files\\"+askedFilename, target)
            
            messagebox.showinfo("Successfully exported file",
                                "We have successfully exported "+askedFilename+" file.",parent=root)
        elif askedFilename == "All":
            if len(os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\")) != 1:
                datetimeGen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                exportFolder = folder+"\\" + datetimeGen+" Exported Files"
                os.mkdir(exportFolder)
                for file in os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\"):
                    shutil.copy(main_destination+"\Data\\"+username +
                                "\\"+"Files\\"+file, exportFolder+"\\"+file)
                
                messagebox.showinfo(
                    "Successfully exported files", "We have successfully exported all files.", parent=root)

            else:
                for file in os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\"):
                    shutil.copy(main_destination+"\Data\\"+username +
                                "\\"+"Files\\"+file, folder+"\\"+file)
                messagebox.showinfo(
                    "Successfully exported files", "We have successfully exported all file.", parent=root)


    def viewdeleteFileWork():
        fileNameGot = comboxbox_options.get()
        if fileNameGot != "" and fileNameGot != "All":
            os.startfile(main_destination+"\Data\\" +
                         usernameDataGave+"\\"+"Files\\" + fileNameGot)
        elif fileNameGot == "" and fileNameGot == "All":
            for x in fileData:
                os.startfile(main_destination+"\Data\\" +
                             usernameDataGave+"\\"+"Files\\" + x)
    button_uploadFile = Button(root, text="Export File", relief="flat", font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=exportFileWork)
    button_uploadFile.place(relx=0.2, rely=0.6)
    button_showGoingToDeleteFile = Button(root, text="Show File", relief=FLAT, font=(
        "@Yu Gothic UI Semibold", 16, "normal"), command=viewdeleteFileWork)
    button_showGoingToDeleteFile.place(relx=0.6, rely=0.6)

    def on_closing():
        for file in os.listdir(main_destination+"Data\\"+usernameDataGave+"\\"+"Files"):
            FileManage(keyEncryptor, main_destination+"Data\\" +
                       usernameDataGave+"\\"+"Files\\"+file)
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def main():
    try:
        with open(main_destination+'accounts.json') as json_file:
            accountsData = json.load(json_file)
        if os.path.isfile(f"{temp_folder}/temp_datamanager"):
            with open(f"{temp_folder}/temp_datamanager", "r+") as f:
                data = (f.read()).split(" | ")
            if data[0] in accountsData["accounts"]:
                encryptedPassword = accountsData["accounts"][data[0]][0]
                if encryptedPassword == SHA512(data[1]):
                    userName = data[0]
                    try:
                        handlerWhatTo(data[0])
                    except:
                        pass
        else:
            loginAndSignUp()
    finally:
        with open(accounts_file) as json_file:
            accountsJSON = json.load(json_file)

        keyEncryptor = accountsJSON["accounts"][userName][1]
        for file in os.listdir(main_destination+"Data\\"+userName+"\\"+"Files"):
            FileManage(keyEncryptor, main_destination+"Data\\" + userName+"\\"+"Files\\"+file)
    except:
        pass

if __name__ == '__main__':
    main()

