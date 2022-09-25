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
import json

with open('settings.json') as f:
    data = json.load(f)

if darkdetect.isDark():
    theme = 'dark'
else:
    theme = 'light'
response = requests.get("https://api.github.com/repos/Fefedu973/Activity-Condenser/releases/latest")
getchangelog = (response.json()["body"])
getver = re.sub("[^0-9,.]", "", (response.json()["name"]))
print(getver)

if data['checkonstart'] == 1:
    if getver == "0.0.3":
        sp.Popen(['python','tray.py'])
        sys.exit()

    else:
        pass
else :
    sp.Popen(['python','tray.py'])
    sys.exit()

class UpdateApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.iconbitmap('about.ico')
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
        checkbutton1 = ttk.Checkbutton(frame2)
        self.check2 = tk.IntVar()
        self.check2.set(data['checkonstart'])
        checkbutton1.configure(command=self.check, variable=self.check2, text="Check updates on start")
        checkbutton1.grid(column=0, pady="10 0", row=5, sticky="e")
        frame2.pack(side="top")
        sv_ttk.set_theme(theme)

        # Main widget
        self.mainwindow = toplevel1

    def check(self):
        data['checkonstart'] = self.check2.get()
        with open('settings.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(data)

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
        with open("Activity-Condenser.exe", "wb") as code:
            code.write(r.content)
        self.label3.configure(foreground='green')    
        self.update.set("Download complete ! Please wait for the installer to start")
        subprocess.call("Activity-Condenser.exe", shell=True)

    def cancel(self):
        sp.Popen(['python','tray.py'])
        self.mainwindow.destroy()
        sys.exit()


if __name__ == "__main__":
    app = UpdateApp()
    app.run()
