# Importing modules
import os
import json
import time
import main_functions
from pynput import keyboard
import threading

usernameData = ""

runningFunction = "handle"

# Open the json file
with open('accounts.json') as json_file:
    accountsData = json.load(json_file)
# Important Functions
def signup():
    global runningFunction
    runningFunction = "signup"
    print("Please enter the following information:\n")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username != "" and password != "":
        if username in accountsData["accounts"]:
            print("Username already exists. Please try again.")
            signup()
        encryptedPassword = main_functions.encryptText(username, password)
        accountsData["accounts"][username] = encryptedPassword
        with open('accounts.json', 'w') as outfile:
            json.dump(accountsData, outfile)
        os.system("cls")
        print("Account created successfully.")
        os.mkdir(str(os.getcwd())+"\\Data\\"+username)
        with open(str(os.getcwd())+"\\Data\\"+username+"\\"+"data.json", "w") as f:
            f.write("{\"data\": {}}")
        print("\n")
        username = usernameData
        os.system(f'py handler.py "{usernameData}"')


def login():
    # Run the function checkIf in a new thread to prevent the program from freezing
    global runningFunction
    runningFunction = "login"
    global usernameData
    print("Please enter the following information:\n")
    username = input("Enter username: ")
    password = input("Enter password: ")
    usernameData = username
    if username in accountsData["accounts"]:
        encryptedPassword = accountsData["accounts"][username]
        decryptedPassword = main_functions.decryptData(username, encryptedPassword)
        if password == decryptedPassword:
            print("Login successful.")
            print("\n")
            os.system("cls")
            os.system(f"py handler.py \"{username}\"")
        else:
            print("Incorrect password. Please try again.")
            login()
            print("\n")
    else:
        print("Username does not exist. Please try again.")
        login()
        print("\n")
        return username

    
print("Welcome to Manager\n")

print("What do you want to do?\n")
print("(1) Create new account")
print("(2) Log in")
print("(3) Exit")
def handle():
    
    global runningFunction
    runningFunction = "handle"
    global usernameData
    command = input("Enter command: ")
    if command=="1":
        signup()
        time.sleep(5)
    elif command=="2":
        login()
        os.system(f'py handler.py "{usernameData}"')
    elif command=="3":
        print("Bye, See you next time!")
        exit()
    else:
        print("Invalid command. Please try again.")
        handle()
handle()