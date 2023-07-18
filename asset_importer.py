import os
import shutil
from tkinter import filedialog, simpledialog, messagebox
from tkinter import END
import tkinter as tk
from enum import Enum
from PIL import ImageTk, Image

HEIGHT_WINDOW = 600
WIDTH_WINDOW = 800

class AssetTag(str, Enum):
    NAME = "name"
    EDITOR_IMAGE = "image"
    EXT_SETTINGS = "extra-settings"
    ICON = "icon"

class Extension(str, Enum):
    INI = "ini"
    IMAGE = "png"
    LUA = "lua"
    JSON = "json"

class Session():
    def __init__(self):
        self.assets = []


    def find_asset_info(self, luaName, luaPath, assetTag):
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

    def filter_asset(self):
        pass

    def initialize_asset(self):
        dir = filedialog.askdirectory()
        items = os.listdir(dir)
        entries = [f for f in items if f.endswith(".lua")]

        fileList.delete(0, END)

        if len(entries) > 0:
            importButton.configure(state = tk.NORMAL)
            for e in entries:
                current_asset = self.find_asset_info(e, dir, AssetTag.NAME)

                if current_asset != None:
                    fileList.insert(END, current_asset)

        folderName.configure(text = dir, foreground = "black")
        #fileList.config(yscrollcommand = fileScroll.set)
        #fileScroll.config(command = fileList.yview)


    def copy_asset(self, srcPath, dstPath, fileExt):
        shutil.copyfile(srcPath, dstPath)

    def import_asset(self):
        file = filedialog.askopenfilename(filetypes=[("Lua files", ".lua")])
        filepath = os.path.dirname(file)
        filename = os.path.basename(file)

        new_asset = self.find_asset_info(filename, filepath, AssetTag.NAME)

        if new_asset != None:
            fileList.insert(END, new_asset)

            # copying
            # copy_assets(file, folderName["text"])]
        else:
            messagebox.showerror(title = "Invalid Asset", message = "The asset you have chosen is invalid.")


# main program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Asset Importer")
    root.resizable = False

    #root.geometry(f"{WIDTH_WINDOW}x{HEIGHT_WINDOW}")

    session = Session()

    importContainer = tk.LabelFrame(root, text = "Files")
    openButton = tk.Button(importContainer, text = "Open level folder", command = session.initialize_asset)
    importButton = tk.Button(importContainer, text = "Import new asset", command = session.import_asset, state = tk.DISABLED)

    importContainer.grid(row = 0, column = 0, padx = 20, pady = 20)
    openButton.grid(row = 1, column = 0, padx = 10, pady = 10)
    importButton.grid(row = 1, column = 1, padx = 10, pady = 10)

    filesContainer = tk.LabelFrame(root, text = "Custom Assets in Folder")
    filesContainer.grid(row = 2, column = 0, padx = 20, pady = 20, )

    folderContainer = tk.LabelFrame(filesContainer, text = "Current Assets")
    folderContainer.grid(row = 3, column = 0, padx = 10, pady = 10)

    #folderScroll = tk.Scrollbar(folderContainer, orient = "horizontal")
    #folderScroll.grid(row = 3, column = 0, padx = 10, pady = 10)

    folderName = tk.Label(filesContainer, text = "Pick a directory first", foreground = "gray")
    folderName.grid(row = 2, column = 0, padx = 10, pady = 10)

    #fileScroll = tk.Scrollbar(folderContainer, orient = tk.VERTICAL, )
    #fileScroll.grid(row = 4, column = 1)

    fileList = tk.Listbox(folderContainer)
    fileList.grid(row = 4, column = 0, padx = 10, pady = 10)

    imageContainer = tk.LabelFrame(filesContainer, text = "Preview Image")
    imageContainer.grid(row = 3, column = 1, padx = 10, pady = 10)

    #imageDummy = Image.open("empty.png")
    #imageContent = ImageTk.PhotoImage(imageDummy)

    imagePrev = tk.Label(imageContainer, text = "Image")#, image = imageContent)
    imagePrev.grid(row = 4, column = 1, padx = 10, pady = 10)

    root.mainloop()