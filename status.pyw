#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import darkdetect
import sv_ttk
import psutil
import os
import json
import subprocess as sp

discord = None

if ("Discord.exe" in (p.name() for p in psutil.process_iter())) == True:
    discord = "Discord is running"
    discordcolor = 'green'
else: 
    discord = "Discord is not running"
    discordcolor = 'red'

src = os.path.join(os.getenv("APPDATA"),"Activity-Condenser")
errors = os.path.join(src,"errors.json")

with open(errors) as f:
    errorfinal = json.load(f)

if errorfinal == {"Errors":""}:
    app = "Activity Condenser is running"
    appcolor = 'green'
else:
    app = errorfinal['Errors']
    appcolor = 'red'

if darkdetect.isDark():
    theme = 'dark'
    icontheme = 'health-white.ico'
else:
    theme = 'light'
    icontheme = 'health-dark.ico'

class StatusApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.iconbitmap(icontheme)
        toplevel1.configure(height=200, width=400)
        toplevel1.resizable(False, False)
        toplevel1.title("Activity Condener Status")
        frame2 = tk.Frame(toplevel1)
        frame2.configure(height=200, padx=50, pady=10, width=200)
        button1 = ttk.Button(frame2)
        button1.configure(cursor="hand2", text='Ok', width=12)
        button1.grid(column=0, pady="30 0", row=4, sticky="e")
        button1.configure(command=self.ok)
        separator3 = ttk.Separator(frame2)
        separator3.configure(orient="horizontal")
        separator3.grid(column=0, ipadx=250, pady="10 40", row=4)
        separator4 = ttk.Separator(frame2)
        separator4.configure(orient="horizontal")
        separator4.grid(column=0, ipadx=250, pady="0 10", row=2)
        label2 = ttk.Label(frame2)
        label2.configure(text='Discord status :\nApp Status :')
        label2.grid(column=0, row=3, sticky="w")
        label4 = ttk.Label(frame2)
        label4.configure(text='Activity Condenser Status')
        label4.grid(column=0, pady="0 10", row=0)
        button2 = ttk.Button(frame2)
        button2.configure(cursor="hand2", text='Reconnexion', width=15)
        button2.grid(column=0, pady="30 0", row=4, sticky="w")
        button2.configure(command=self.reconnect)
        label1 = ttk.Label(frame2)
        self.discordstatus = tk.StringVar(value=discord)
        label1.configure(text='label1', textvariable=self.discordstatus, foreground=discordcolor)
        label1.grid(column=0, row=3, sticky="ne")
        label3 = ttk.Label(frame2)
        self.appstatus = tk.StringVar(value=app)
        label3.configure(text='label3', textvariable=self.appstatus, foreground=appcolor)
        label3.grid(column=0, row=3, sticky="se")
        sv_ttk.set_theme(theme)
        frame2.pack(side="top")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def ok(self):
        self.mainwindow.destroy()

    def reconnect(self):
        pass

        #recoit les infos extProc1 et extProc2 puis kill le process puis relance le process avec sp.Popen et remet les infos dans le json puis met le texte en attente puis affiche les erreurs si il y en a sinon met Activity Condenser is running


if __name__ == "__main__":
    app = StatusApp()
    app.run()