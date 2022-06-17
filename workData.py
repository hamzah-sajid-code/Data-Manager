from tkinter import *
import argparse
import json
import os
from tkinter import filedialog
import threading
import main_functions

# get username argument from the command line
parser = argparse.ArgumentParser()
parser.add_argument("username", help="username")
args = parser.parse_args()
username = args.username

print("\n(1) Make Data")
print("(2) View Data")
print("(3) Delete Data")
print("(4) Export Data")
print("(5) Back")
print("(6) Log out")
print("(7) Exit")

with open(str(os.getcwd())+"\\Data\\"+username+"\\"+"data.json") as json_file:
    dataJSON = json.load(json_file)

def makeData():
    print("\nPlease enter the following information:")
    print("For adding more data respectively to their labels, please add parallel line between them.\n")
    nameData = input("Enter a name for the data: ")
    label = input("Enter labels: ")
    data = input("Enter data: ")
    if label != "" and data != "":
        if len(label.split(" | ")) == len(data.split(" | ")):
            finalData = {}
            label = label.split(" | ")
            data = data.split(" | ")
            dataDict = dict(zip(label, data))
            finalData[nameData] = dataDict
            dataJSON["data"].update(finalData)
            with open(str(os.getcwd())+"\Data\\"+username+"\\"+"data.json", "w") as f:
                json.dump(dataJSON, f)
            print("\n")
            print("Data added successfully.")
            handle()
        else:
            print("\nInvalid data. Please try again.\n")
            makeData()
    else:
        print("\nPlease enter the data.")
        makeData()

def viewData():
    print("List of all data by key name\n")
    if dataJSON["data"] != {}:
        for key in dataJSON["data"]:
            print(key)
        print("\n")

        nameData = input("Select a data to view: ")
        if nameData != "":
            if nameData in dataJSON["data"]:
                print(f"\nData in {nameData}")
                for key in dataJSON["data"][nameData]:
                    print(key, ":", dataJSON["data"][nameData][key])
                handle()
            else:
                print("\nInvalid data. Please try again.\n")
                viewData()
        else:
            print("\nInvalid data. Please try again.\n")
            viewData()
    else:
        print("No data found.\n")
        handle()
        # When CTRL+B is pressed, the program will call the handler function

def deleteData():
    if dataJSON["data"] != {}:
        print("List of all data by key name\n")
        for key in dataJSON["data"]:
            print(key)
        print("\n")
        nameData = input("Enter a data to delete: ")
        if nameData != "":
            if nameData in dataJSON["data"]:
                del dataJSON["data"][nameData]
                with open(str(os.getcwd())+"\Data\\"+username+"\\"+"data.json", "w") as f:
                    json.dump(dataJSON, f)
                print("\n")
                print("Data deleted successfully.")
                handle()
            else:
                print("\nInvalid data. Please try again.\n")
                deleteData()
        else:
            print("\nInvalid data. Please try again.\n")
            deleteData()
    else:
        print("No data found.\n")
        handle()
def exportData():
    if dataJSON["data"] != {}:
        root = Tk()
        folder = filedialog.askdirectory(title="Select folder")
        root.destroy()
        print("List of all data by key name\n")
        for key in dataJSON["data"]:
            print(key)
        print("\n")
        nameData = input("Enter a data to export: ")
        if nameData != "" and nameData != "all":
            if nameData in dataJSON["data"]:
                with open(str(folder)+"\\"+nameData+".txt", "w") as f:
                    f.write("Your data in " + nameData + ":\n")
                    for key in dataJSON["data"][nameData]:
                        f.write(key+" : "+dataJSON["data"][nameData][key]+"\n")
                    f.close()
                print("\n")
                print("Data exported successfully.")
                handle()
            else:
                print("\nInvalid data. Please try again.\n")
                exportData()
        elif nameData != "" and nameData == "all" or nameData == "All":
            fileName = "All Exported Data.txt"
            if os.path.isfile(folder+"\\"+fileName):
                i = 1
                while os.path.isfile(folder+"\\"+fileName):
                    fileName, fileExtension = os.path.splitext(fileName)
                    fileName = fileName+" ("+str(i)+")"+fileExtension
                    i += 1
            f = open(folder+"\\"+fileName, "w")
            f.write("Your data:")
            for key in dataJSON["data"]:
                print(key)
                f.write("\nYour data in " + key + ":\n")
                for key2 in dataJSON["data"][key]:
                    f.write(key2+" : "+dataJSON["data"][key][key2]+"\n")
            f.close()
            print("\n")
            print("Data exported successfully.")
            handle()
        else:
            print("\nInvalid data. Please try again.\n")
            exportData()
    else:
        print("No data found.\n")
        handle()

def handle():
    command = input("Enter command: ")
    if command == "1":
        makeData()
    elif command == "2":
        viewData()
    elif command == "3":
        deleteData()
    elif command == "4":
        exportData()
    elif command == "5":
        os.system("py handler.py \""+username+"\"")
    elif command == "6":
        main_functions.logout()
    elif command == "7":
        exit()
    else:
        print("\nInvalid command. Please try again.\n")
        handle()

handle()
