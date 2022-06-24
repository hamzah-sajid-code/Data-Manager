from tkinter import *
import argparse
import json
import os
from tkinter import filedialog
from tkinter import messagebox

# get username argument from the command line
parser = argparse.ArgumentParser()
parser.add_argument("username", help="username")
args = parser.parse_args()
username = args.username

with open(str(os.getcwd()) + "\\Data\\" + username + "\\" + "data.json") as json_file:
    dataJSON = json.load(json_file)


def makeData(nameData, label, data):
    if nameData != "" and len(label) != 0 and len(data) != 0:
        if len(label) == len(data):
            finalData = {}
            for x in range(len(label)):
                dataDict = dict(zip(label[x], data[x]))
                finalData[nameData] = dataDict
                dataJSON["data"].update(finalData)
                with open(str(os.getcwd()) + "\\Data\\" + username + "\\" + "data.json", "w") as f:
                    json.dump(dataJSON, f)
        else:
            messagebox.showerror("Data not given properly",
                                 "Please check if the data give is respectively to the label, there are blank spaces.")
    else:
        messagebox.showerror("Data not given properly",
                             "Please check if the data name is not empty and the label and data are not empty")


class ViewData:
    def __init__(self):
        self.data = []
        for key in dataJSON["data"]:
            self.data.append(key)

    def viewData(self, dataName):
        if self.data != [] and dataName != "":
            return dataJSON["data"][dataName]
        else:
            messagebox.showerror("No data found", "There is no data name give or there is not data give to us")


class DeleteData:
    def __init__(self):
        self.data = []
        for key in dataJSON["data"]:
            self.data.append(key)

    def deleteData(self, dataName):
        if self.data != [] and dataName != "" and dataName in dataJSON["data"]:
            del dataJSON["data"][dataName]
            with open(str(os.getcwd()) + "\\Data\\" + username + "\\" + "data.json", "w") as f:
                json.dump(dataJSON, f)
            messagebox.showinfo("Delete operation successful", f"We have deleted {dataName} from our database")
        else:
            messagebox.showerror("No data found", "There is no data name give or there is not data give to us")


class ExportData:
    def __init__(self):
        self.data = []
        for key in dataJSON["data"]:
            self.data.append(key)
        if self.data:
            self.data.append("all")

    def deleteData(self, dataName):
        if self.data != [] and dataName != "" and dataName in dataJSON["data"]:
            tkinterfile = Tk()
            folder = filedialog.askdirectory(title="Select folder")
            tkinterfile.destroy()
            if dataName != "" and dataName != "all":
                if dataName in dataJSON["data"]:
                    with open(str(folder) + "\\" + dataName + ".txt", "w") as f:
                        f.write("Your data in " + dataName + ":\n")
                        for key in dataJSON["data"][dataName]:
                            f.write(key + " : " + dataJSON["data"][dataName][key] + "\n")
                        f.close()
                        messagebox.showinfo("successfully exported data",
                                            f"We have successfully exported data of {dataName}")
            elif dataName != "" and dataName == "all":
                fileName = "All Exported Data.txt"
                if os.path.isfile(folder + "\\" + fileName):
                    i = 1
                    while os.path.isfile(folder + "\\" + fileName):
                        fileName, fileExtension = os.path.splitext(fileName)
                        fileName = fileName + " (" + str(i) + ")" + fileExtension
                        i += 1
                f = open(folder + "\\" + fileName, "w")
                f.write("Your data:")
                for key in dataJSON["data"]:
                    print(key)
                    f.write("\nYour data in " + key + ":\n")
                    for key2 in dataJSON["data"][key]:
                        f.write(key2 + " : " + dataJSON["data"][key][key2] + "\n")
                f.close()
                messagebox.showinfo("successfully exported data", "We have successfully exported all the data")
        else:
            messagebox.showerror("No data found", "There is no data name give or there is not data give to us")
