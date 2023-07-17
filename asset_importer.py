import os
import shutil
from tkinter import filedialog, simpledialog, messagebox
from tkinter import END
import tkinter as tk
from enum import Enum

HEIGHT_WINDOW = 400
WIDTH_WINDOW = 500

class AssetTag(str, Enum):
    NAME = "name"
    EDITOR_IMAGE = "image"
    EXT_SETTINGS = "extra-settings"

class Session():
    def __init__(self):
        pass


def find_asset(luaName, luaPath, assetTag):
    iniFilePart = luaName.split(".")[0] + ".ini"
    iniFile = os.path.join(luaPath, iniFilePart)
    
    if os.path.exists(iniFile):
        lines = open(iniFile, "r").readlines()
            
        for l in lines:
            parsed = l.split("=")
            if parsed[0].strip() == assetTag:
                return parsed[1].strip()[1:-1] # strip removes whitespace, [1:-1] removes quotation marks
        return None
    else:
        return None

def initialize_asset():
    global importButtonState
    dir = filedialog.askdirectory()
    items = os.listdir(dir)
    entries = [f for f in items if f.endswith(".lua")]

    fileList.delete(0, END)

    if len(entries) > 0:
        importButton.configure(state = tk.NORMAL)
        for e in entries:
            current_asset = find_asset(e, dir, AssetTag.NAME)

            if current_asset != None:
                fileList.insert(END, current_asset)
    else:
        # do something
        pass


def import_asset():
    file = filedialog.askopenfilename(filetypes=[("Lua files", ".lua")])
    filepath = os.path.dirname(file)
    filename = os.path.basename(file)

    new_asset = find_asset(filename, filepath, AssetTag.NAME)

    if new_asset != None:
        fileList.insert(END, new_asset)
    else:
        messagebox.showerror(title = "Invalid Asset", message = "The asset you have chosen is invalid.")



# main program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Asset Importer")
    root.resizable = False

    canvas = tk.Canvas(root, width = WIDTH_WINDOW, height = HEIGHT_WINDOW)

    importContainer = tk.LabelFrame(root, text = "Files")
    openButton = tk.Button(importContainer, text = "Open level folder", command = initialize_asset)
    importButton = tk.Button(importContainer, text = "Import new asset", command = import_asset, state = tk.DISABLED)

    importContainer.grid(row = 0, column = 0, padx = 20, pady = 20)
    openButton.grid(row = 1, column = 0, padx = 10, pady = 10)
    importButton.grid(row = 1, column = 1, padx = 10, pady = 10)

    filesContainer = tk.LabelFrame(root, text = "Custom Assets in Folder")
    filesContainer.grid(row = 2, column = 0, padx = 20, pady = 20)

    fileList = tk.Listbox(filesContainer)
    fileList.grid(row = 3, column = 0, padx = 10, pady = 10)

    root.mainloop()