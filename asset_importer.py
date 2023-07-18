import os
import shutil
from tkinter import filedialog, simpledialog, messagebox
from tkinter import END
import tkinter as tk
from enum import Enum

HEIGHT_WINDOW = 600
WIDTH_WINDOW = 800

# classes

class AssetTag(str, Enum):
    NAME = "name"
    EDITOR_IMAGE = "image"
    EXT_SETTINGS = "extra-settings"
    ICON = "icon"

class AssetType(str, Enum):
    BLOCK = "block"
    NPC = "npc"

class Extension(str, Enum):
    INI = "ini"
    IMAGE = "png"
    LUA = "lua"
    JSON = "json"


class Session():
    def __init__(self):
        self.assetsNPC = []
        self.assetsBlock = []
        self.directory = ""
        self.currentAssetButton = AssetType.NPC
        self.assets = {
            AssetType.NPC: self.assetsNPC,
            AssetType.BLOCK: self.assetsBlock,
        }

    def setup_listbox(self, list):
        fileList.delete(0, END)

        for item in list:
            fileList.insert(END, item)

    def add_item_listbox(self, item):
        fileList.insert(END, item)

    def show_NPC(self):
        self.currentAssetButton = AssetType.NPC
        fileList.delete(0, END)

        for item in self.assetsNPC:
            currentAsset = self.find_asset_info(item, self.directory, AssetTag.NAME)

            fileList.insert(END, currentAsset[1])

    def show_blocks(self):
        self.currentAssetButton = AssetType.BLOCK
        fileList.delete(0, END)

        for item in self.assetsBlock:
            currentAsset = self.find_asset_info(item, self.directory, AssetTag.NAME)

            fileList.insert(END, currentAsset[1])

    def find_asset_info(self, luaName, luaPath, assetTag):
        filename = luaName.split(".")[0]
        iniFilePart = filename + ".ini"
        iniFile = os.path.join(luaPath, iniFilePart)
        
        if os.path.exists(iniFile):
            lines = open(iniFile, "r").readlines()
                
            for l in lines:
                parsed = l.split("=")
                if parsed[0].strip() == assetTag:
                    return (filename, parsed[1].strip()[1:-1]) # strip removes whitespace, [1:-1] removes quotation marks
            return None
        else:
            return None

    def initialize_asset(self):
        dir = filedialog.askdirectory()

        if dir == '':
            return

        items = os.listdir(dir)
        entries = [f for f in items if f.endswith(".lua")]

        fileList.delete(0, END)

        if len(entries) > 0:
            importButton.configure(state = tk.NORMAL)
            NPCButton.configure(state = tk.NORMAL)
            blocksButton.configure(state = tk.NORMAL)
            copyButton.configure(state = tk.NORMAL)

            for e in entries:
                currentAsset = self.find_asset_info(e, dir, AssetTag.NAME)

                if currentAsset != None:
                    assetType = currentAsset[0].split("-")[0]                        

                    if assetType == AssetType.NPC:
                        self.assetsNPC.append(currentAsset[0])

                        if self.currentAssetButton == AssetType.NPC:
                            fileList.insert(END, currentAsset[1])
                    elif assetType == AssetType.BLOCK:
                        self.assetsBlock.append(currentAsset[0])

                        if self.currentAssetButton == AssetType.BLOCK:
                            fileList.insert(END, currentAsset[1])
                    

        folderName.configure(text = dir, foreground = "black")
        self.directory = dir
        #fileList.config(yscrollcommand = fileScroll.set)
        #fileScroll.config(command = fileList.yview)

    def find_lowest_available_id(self, assetType):
        minID = 751

        if assetType == AssetType.NPC:
            asset = "npc"
        elif assetType == AssetType.BLOCK:
            asset = "block"
        
        while minID < 1000:
            if f'{asset}-{minID}' not in self.assets[assetType]:
                return minID
            minID += 1
        
        return -1

    def copy_assets(self, srcID, srcLua, dstPath, assetType):
        availableID = self.find_lowest_available_id(assetType)
        srcPath = os.path.dirname(srcLua)

        # copy lua
        dstLua = os.path.join(dstPath, f'{assetType}-{availableID}.lua')
        shutil.copy(srcLua, dstLua)

        # copy image
        srcPng = os.path.join(srcPath, f'{assetType}-{srcID}.png')
        dstPng = os.path.join(dstPath, f'{assetType}-{availableID}.png')
        shutil.copy(srcPng, dstPng)

        # copy ini
        srcIni = os.path.join(srcPath, f'{assetType}-{srcID}.ini')
        dstIni = os.path.join(dstPath, f'{assetType}-{availableID}.ini')

        # edit ini
        lines = open(srcIni, "r").readlines()
        i = -1
            
        for l in range(len(lines)):
            parsed = lines[l].split("=")
            if parsed[0].strip() == AssetTag.EDITOR_IMAGE:
                i = l

        lines[i] = f'image = "{assetType}-{availableID}.png"\n'
        out = open(dstIni, "w", newline='\r\n')
        out.writelines(lines)
        out.close()

    def import_asset(self):
        file = filedialog.askopenfilename(filetypes=[("Lua files", ".lua")])
        filepath = os.path.dirname(file)
        filename = os.path.basename(file)

        newAsset = self.find_asset_info(filename, filepath, AssetTag.NAME)

        if newAsset != None:
            assetType = newAsset[0].split("-")[0]

            if assetType == AssetType.NPC:
                self.assetsNPC.append(newAsset[0])

                if self.currentAssetButton == AssetType.NPC:
                    fileList.insert(END, newAsset[1])
            elif assetType == AssetType.BLOCK:
                self.assetsBlock.append(newAsset[0])

                if self.currentAssetButton == AssetType.BLOCK:
                    fileList.insert(END, newAsset[1])

            # copying
            #print(newAsset[0], assetType)
            self.copy_assets(newAsset[0].split("-")[1], file, self.directory, assetType)
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
    importContainer.grid(row = 0, column = 0, padx = 20, pady = 20)

    openButton = tk.Button(importContainer, text = "Open level folder", command = session.initialize_asset)
    openButton.grid(row = 1, column = 0, padx = 10, pady = 10)

    importButton = tk.Button(importContainer, text = "Import new asset", command = session.import_asset, state = tk.DISABLED)
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
    fileList.grid(row = 5, column = 0, padx = 10, pady = 10)

    imageContainer = tk.LabelFrame(filesContainer, text = "Preview Image")
    imageContainer.grid(row = 3, column = 1, padx = 10, pady = 10)

    imagePrev = tk.Label(folderContainer, text = "Image")#, image = imageContent)
    imagePrev.grid(row = 5, column = 1, padx = 10, pady = 10)

    buttonContainer = tk.LabelFrame(folderContainer, text = "")
    buttonContainer.grid(row = 4, column = 0, padx = 10, pady = 10)

    NPCButton = tk.Button(buttonContainer, text = "NPCs", command = session.show_NPC, state = tk.DISABLED)
    NPCButton.grid(row = 4, column = 0, padx = 10, pady = 10)

    blocksButton = tk.Button(buttonContainer, text = "Blocks", command = session.show_blocks, state = tk.DISABLED)
    blocksButton.grid(row = 4, column = 1, padx = 10, pady = 10)

    copyButton = tk.Button(buttonContainer, text = "Copy", command = lambda: session.import_asset(), state = tk.DISABLED)
    copyButton.grid(row = 4, column = 2, padx = 10, pady = 10)

    root.mainloop()