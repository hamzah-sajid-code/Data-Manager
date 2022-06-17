import argparse
import datetime
import json
import os
import shutil
from tkinter import filedialog

import main_functions

parser = argparse.ArgumentParser()
parser.add_argument("username", help="username")
args = parser.parse_args()
username = args.username

# See if files folder exists and if not, create it
if not os.path.exists(str(os.getcwd())+"\\Data\\"+username+"\\"+"Files"):
    os.makedirs(str(os.getcwd())+"\Data\\"+username+"\\"+"Files")
else:
    pass

print("\n(1) Make Data")
print("(2) View Data")
print("(3) Delete Data")
print("(4) Export Data")
print("(5) Logout")
print("(6) Exit")


def makeData():
    print("\nPlease enter the following information:")
    try:
        fileName = filedialog.askopenfilename(title = "Select file",)
        shutil.copy(fileName, str(os.getcwd())+"\Data\\"+username+"\\"+"Files\\" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")+"_"+os.path.basename(fileName))
        print("\nFile Location: " + fileName)
    except FileNotFoundError:

        print("\nFile not found. Please try again.\n")
    handle()

def veiwData():
    if os.listdir(str(os.getcwd())+"\Data\\"+username+"\\"+"Files") != []:
        print("All files: ")
        for file in os.listdir(str(os.getcwd())+"\Data\\"+username+"\\"+"Files"):
            print(file)
        askedFilename = input("\nEnter the file name: ")
        if askedFilename in os.listdir(str(os.getcwd())+"\Data\\"+username+"\\"+"Files"):
            print("\nFile: " + askedFilename)
            fileLocation = str(os.getcwd())+"\Data\\"+username+"\\"+"Files\\"+askedFilename
            # open the file with its default application
            os.startfile(fileLocation)
            handle()
        else:
            print("\nFile not found. Please try again.\n")
            veiwData()
    else:
        print("\nNo files found.\n")
        handle()

def deleteData():
    if os.listdir(str(os.getcwd())+"\Data\\"+username+"\\"+"Files") != []:
        print("All files: ")
        for file in os.listdir(str(os.getcwd())+"\Data\\"+username+"\\"+"Files"):
            print(file)
        askedFilename = input("\nEnter the file name: ")
        if askedFilename in os.listdir(str(os.getcwd())+"\Data\\"+username+"\\"+"Files"):
            print("\nFile: " + askedFilename)
            # Ask for confirmation
            confirmation = input("\nAre you sure you want to delete this file? (y/n): ")
            if confirmation == "y":
                os.remove(str(os.getcwd())+"\Data\\"+username+"\\"+"Files\\"+askedFilename)
                print("\nFile deleted.\n")
                handle()
            else:
                print("Delete cancelled.\n")
        else:
            print("\nFile not found. Please try again.\n")
            deleteData()
    else:
        print("\nNo files found.\n")
        handle()

def exportData():
    if os.listdir(str(os.getcwd())+"\Data\\"+username+"\\"+"Files") != []:
        folder = filedialog.askdirectory(title = "Select folder")
        for file in os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\"):
            print(file)
        askedFilename = input("\nEnter the file name: ")
        if askedFilename in os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\"):
            withOutDate = askedFilename[20:]
            shutil.copy(str(os.getcwd())+"\Data\\"+username+"\\"+"Files\\"+askedFilename, folder+"\\"+withOutDate)
            print("\nFile exported.\n")
            handle()
        elif askedFilename == "All" or askedFilename == "all":
            for file in os.listdir(os.getcwd()+"\Data\\"+username+"\\"+"Files\\"):
                withOutDate = file[20:]
                if os.path.isfile(folder+"\\"+withOutDate):
                    i = 1
                    while os.path.isfile(folder+"\\"+withOutDate):
                        fileName, fileExtension = os.path.splitext(withOutDate)
                        withOutDate = fileName+" ("+str(i)+")"+fileExtension
                        i += 1
                shutil.copy(str(os.getcwd())+"\Data\\"+username+"\\"+"Files\\"+file, folder+"\\"+withOutDate)
            print("\nAll files exported.\n")
            handle()
        else:
            print("\nFile not found. Please try again.\n")
            exportData()
    else:
        print("\nNo files found.\n")
        handle()

def handle():
    with open(str(os.getcwd())+"\Data\\"+username+"\\"+"data.json") as json_file:
        dataJSON = json.load(json_file)
    command = input("Enter command: ")
    if command == "1":
        makeData()
        handle()
    elif command == "2":
        veiwData()
        handle()
    elif command == "3":
        deleteData()
        handle()
    elif command == "4":
        exportData()
        handle()
    elif command == "5":
        main_functions.logout()
    elif command == "6":
        exit()
    else:
        print("\nInvalid command. Please try again.\n")
        handle()

handle()
