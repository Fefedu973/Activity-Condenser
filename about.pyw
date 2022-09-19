#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk,Image
import requests  
import re
import subprocess
import threading


class AboutApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.iconbitmap('settings.ico')
        toplevel1.configure(height=200, width=200)
        toplevel1.resizable(False, False)
        toplevel1.title("About Activity Condenser")
        frame2 = tk.Frame(toplevel1)
        frame2.configure(height=200, padx=50, pady=10, width=200)
        label1 = tk.Label(frame2)
        label1.configure(font="{Arial} 16 {bold}", text="Activity Condenser\n")
        label1.grid(column=0, padx="60 0", pady="0 15", row=0, sticky="w")
        button1 = tk.Button(frame2)
        button1.configure(cursor="hand2", text="Ok", width=12)
        button1.grid(column=0, pady="30 0", row=4, sticky="e")
        button1.configure(command=self.on_ok)
        separator3 = ttk.Separator(frame2)
        separator3.configure(orient="horizontal")
        separator3.grid(column=0, ipadx=120, pady="10 40", row=4)
        separator4 = ttk.Separator(frame2)
        separator4.configure(orient="horizontal")
        separator4.grid(column=0, ipadx=120, pady="0 10", row=2)
        label2 = ttk.Label(frame2)
        label2.configure(
            text="Activity condenser is an application that allows you \nto condense several discord activities into a single \nanimated one\n\nCopytight © 2022 Fefe_du_973\n\nThis program is free software: you can redistribute\nit and/or modify it under the terms of the GNU\nGeneral Public License as published by the Free\n Software Foundation, either version 3 of the \nLicense, or (at your option) any later version.\n\nThis program is distributed in the hope that \nit will be useful, but WITHOUT ANY WARRANTY;\n without even the implied warranty of \nMERCHANTABILITY or FITNESS FOR A \nPARTICULAR PURPOSE. See the \nGNU General Public License for more details.\nYou should have received a copy of the GNU \nGeneral Public License along with this program."
        )
        label2.grid(column=0, row=3)
        label4 = ttk.Label(frame2)
        label4.configure(font="{Arial} 12 {}", text="Version 1.0")
        label4.grid(column=0, padx="60 0", row=0, sticky="w")
        canvas1 = tk.Canvas(frame2)
        canvas1.configure(height=50, width=50)
        canvas1.grid(column=0, pady="0 15", row=0, sticky="w")
        self.img = img = ImageTk.PhotoImage(Image.open("icon2.png"))  
        canvas1.create_image(0, 0, anchor=NW, image=img) 
        button2 = tk.Button(frame2)
        button2.configure(cursor="hand2", text="Check for updates", width=15)
        button2.grid(column=0, pady="30 0", row=4, sticky="w")
        button2.configure(command=self.update)
        self.label3 = ttk.Label(frame2)
        self.update = tk.StringVar()
        self.update.set("")
        self.label3.configure(foreground='red', textvariable=self.update)
        self.label3.grid(column=0, row=5, sticky="w")
        frame2.pack(side="top")

        # Main widget
        self.mainwindow = toplevel1


    def update(self):
        response = requests.get("https://api.github.com/repos/Fefedu973/Activity-Condenser/releases/latest")
        getver = re.sub("[^0-9,.]", "", (response.json()["name"]))
        print(getver)
        if getver == "0.0.1":
            self.label3.configure(foreground='green')
            self.update.set("You have the latest version")
            
        else:
            self.label3.configure(foreground='red')
            self.update.set("New version available Downloading... please wait") 
            t1 = threading.Thread(target=self.downloadFunc)
            t1.start()

    def downloadFunc(self):
        r = requests.get("https://github.com/Fefedu973/Activity-Condenser/releases/latest/download/package.zip")
        with open("Activity-Condenser.zip", "wb") as code:
            code.write(r.content)
        self.label3.configure(foreground='green')    
        self.update.set("Download complete ! Stop me and replace me \nwith the new version downloaded in my folder")
        #subprocess.call("Activity-Condenser.zip", shell=True)


    
            

    def run(self):
        self.mainwindow.mainloop()

    def on_ok(self):
        self.mainwindow.destroy()



if __name__ == "__main__":
    app = AboutApp()
    app.run()