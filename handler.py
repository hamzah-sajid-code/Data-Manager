import argparse
import os
import keyboard
import threading
import main_functions
# get username argument from the command line
parser = argparse.ArgumentParser()
parser.add_argument("username", help="username")
args = parser.parse_args()
username = args.username

# os.system("cls")

print("Welcome "+username+"\n")

print("What do you want to do?\n")
print("(1) Work with data")
print("(2) Work with files")
print("(3) Log out")
print("(4) Exit")

def workWithData():
    os.system("cls")
    print("Work with data\n")
    os.system(f'python workData.py "{username}"')

def workWithFile():
    os.system("cls")
    print("Work with data\n")
    os.system(f'python workFile.py "{username}"')

def handle():
    command = str(input("Enter Your Command: "))
    if command == "1":
        workWithData()
    elif command == "2":
        workWithFile()
    elif command == "3":
        main_functions.logout()
    elif command == "4":
        exit()                                                                            
    else:
        print("Error! Please enter an valid command")

handle()