#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk,Image
import requests  
import re
import subprocess
import threading
import sv_ttk
import darkdetect
from tkinter import scrolledtext
import subprocess as sp
import sys
import os

src = os.path.join(os.getenv("APPDATA"),"Activity-Condenser")
downloadsrc = os.path.join(src,"Activity-Condenser.exe")

if darkdetect.isDark():
    theme = 'dark'
    icontheme = 'about-white.ico'
else:
    theme = 'light'
    icontheme = 'about-dark.ico'
response = requests.get("https://api.github.com/repos/Fefedu973/Activity-Condenser/releases/latest")
getchangelog = (response.json()["body"])


class UpdateApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.iconbitmap(icontheme)
        toplevel1.configure(height=200, width=200)
        toplevel1.resizable(False, False)
        toplevel1.title("update")
        frame2 = tk.Frame(toplevel1)
        frame2.configure(height=200, padx=50, pady=10, width=200)
        label1 = ttk.Label(frame2)
        label1.configure(text="New update avalaible !")
        label1.grid(column=0, pady="0 15", row=0)
        button1 = ttk.Button(frame2)
        button1.configure(cursor="hand2", text="Install", width=12)
        button1.grid(column=0, pady="30 0", row=8, sticky="e")
        button1.configure(command=self.install)
        button2 = ttk.Button(frame2)
        button2.configure(cursor="hand2", text="Ignore", width=12)
        button2.grid(column=0, pady="30 0", row=8, sticky="w")
        button2.configure(command=self.cancel)
        separator3 = ttk.Separator(frame2)
        separator3.configure(orient="horizontal")
        separator3.grid(column=0, ipadx=120, pady="10 40", row=8)
        separator4 = ttk.Separator(frame2)
        separator4.configure(orient="horizontal")
        separator4.grid(column=0, ipadx=120, pady="0 10", row=1)
        ScrolledText = scrolledtext.ScrolledText(frame2)
        ScrolledText.configure(height=10, width=50)
        ScrolledText.grid(column=0, pady="0 0", row=2)
        ScrolledText.insert(tk.INSERT, getchangelog)
        ScrolledText.configure(state="disabled")
        self.label3 = ttk.Label(frame2)
        self.update = tk.StringVar()
        self.update.set("")
        self.label3.configure(foreground='red', textvariable=self.update)
        self.label3.grid(column=0, row=5, sticky="w")
        frame2.pack(side="top")
        sv_ttk.set_theme(theme)

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def install(self):
        self.label3.configure(foreground='red')
        self.update.set("Downloading... please wait") 
        t1 = threading.Thread(target=self.downloadFunc)
        t1.start()

    def downloadFunc(self):
        response = requests.get("https://api.github.com/repos/Fefedu973/Activity-Condenser/releases/latest")
        getver = re.sub("[^0-9,.]", "", (response.json()["name"]))
        r = requests.get(f'https://github.com/Fefedu973/Activity-Condenser/releases/download/{getver}/Activity-Condenser.exe')
        print(r)
        with open(downloadsrc, "wb") as code:
            code.write(r.content)
        self.label3.configure(foreground='green')    
        self.update.set("Download complete ! Please wait for the installer to start")
        subprocess.call(downloadsrc, shell=True)

    def cancel(self):
        self.mainwindow.destroy()
        sys.exit()


if __name__ == "__main__":
    app = UpdateApp()
    app.run()
