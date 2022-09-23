#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import json
import win32com.client
import os
import sv_ttk
import darkdetect


with open('settings.json') as f:
    data = json.load(f)

if darkdetect.isDark():
    theme = 'dark'
else:
    theme = 'light'

class SettingsApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.iconbitmap('settings.ico')
        toplevel1.configure(height=200, width=200)
        toplevel1.resizable(False, False)
        toplevel1.title("Settings")
        frame2 = tk.Frame(toplevel1)
        frame2.configure(height=200, padx=50, pady=10, width=200)
        label1 = ttk.Label(frame2)
        label1.configure(text="Settings :")
        label1.grid(column=0, pady="0 15", row=0)
        checkbutton1 = ttk.Checkbutton(frame2)
        self.run2 = tk.IntVar()
        self.run2.set(data['run_on_start'])
        checkbutton1.configure(
            cursor="hand2",
            offvalue=0,
            onvalue=1,
            text="Run on startup",
            variable=self.run2,
        )
        checkbutton1.grid(column=0, pady="0 5", row=1)
        label2 = ttk.Label(frame2)
        label2.configure(text="Client ID :")
        label2.grid(column=0, pady="0 5", row=2)
        entry1 = ttk.Entry(frame2)
        self.ID = tk.StringVar()
        self.ID.set(data['Client_ID'])
        entry1.configure(textvariable=self.ID)
        entry1.delete("0", "end")
        entry1.insert("0", data['Client_ID'])
        entry1.grid(column=0, pady="0 5", row=3)
        label3 = ttk.Label(frame2)
        label3.configure(text="Bot Token :")
        label3.grid(column=0, pady="0 5", row=4)
        entry2 = ttk.Entry(frame2)
        self.Token = tk.StringVar()
        self.Token.set(data['Bot_Token'])
        entry2.configure(textvariable=self.Token)
        entry2.delete("0", "end")
        entry2.insert("0", data['Bot_Token'])
        entry2.grid(column=0, pady="0 5", row=5)
        label4 = ttk.Label(frame2)
        label4.configure(text="Activity Refresh Frequence (min 15 seconds):")
        label4.grid(column=0, pady="0 5", row=8)
        spinbox1 = ttk.Spinbox(frame2)
        self.refresh = tk.IntVar()
        self.refresh.set(data['refresh_time'])
        spinbox1.configure(from_=15, textvariable=self.refresh, to=100)
        spinbox1.grid(column=0, pady="0 5", row=9)
        button1 = ttk.Button(frame2)
        button1.configure(cursor="hand2", text="Ok", width=12)
        button1.grid(column=0, pady="30 0", row=10, sticky="e")
        button1.configure(command=self.on_ok)
        button2 = ttk.Button(frame2)
        button2.configure(cursor="hand2", text="Cancel", width=12)
        button2.grid(column=0, pady="30 0", row=10, sticky="w")
        button2.configure(command=self.cancel)
        separator3 = ttk.Separator(frame2)
        separator3.configure(orient="horizontal")
        separator3.grid(column=0, ipadx=120, pady="10 40", row=10)
        separator4 = ttk.Separator(frame2)
        separator4.configure(orient="horizontal")
        separator4.grid(column=0, ipadx=120, pady="0 40", row=1)
        entry3 = ttk.Entry(frame2)
        self.username = tk.StringVar()
        self.username.set(data['username'])
        entry3.configure(textvariable=self.username)
        entry3.delete("0", "end")
        entry3.insert("0", data['username'])
        entry3.grid(column=0, pady="0 5", row=7)
        label5 = ttk.Label(frame2)
        label5.configure(text="Username (with #) :")
        label5.grid(column=0, pady="0 5", row=6)
        frame2.pack(side="top")
        sv_ttk.set_theme(theme)

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()

    def on_ok(self):
        print(self.run2.get())
        print(self.ID.get())
        print(self.Token.get())
        print(self.refresh.get())
        print(self.username.get())
        run_on_start = self.run2.get()
        Client_ID = self.ID.get()
        Bot_Token = self.Token.get()
        refresh_time = self.refresh.get()
        username = self.username.get()
        settings = {
            "run_on_start": run_on_start,
            "Client_ID": Client_ID,
            "Bot_Token": Bot_Token,
            "refresh_time": refresh_time,
            "username": username
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)
        
        if run_on_start == 1:
            src = os.path.join(os.getenv("APPDATA"),"Microsoft\Windows\Start Menu\Programs\Startup")
            pthtemp = os.path.dirname(os.path.realpath(__file__))
            pth = pthtemp + "\\tray.py"
            desktop = src
            path = os.path.join(desktop, 'Activity-Condenser.lnk')
            target = pth

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WindowStyle = 7
            shortcut.save()
            print(shortcut.Targetpath, shortcut)
        else:
            if os.path.exists(os.path.join(os.getenv("APPDATA"),"Microsoft\Windows\Start Menu\Programs\Startup\Activity-Condenser.lnk")):
                os.remove(os.path.join(os.getenv("APPDATA"),"Microsoft\Windows\Start Menu\Programs\Startup\Activity-Condenser.lnk"))

        self.mainwindow.destroy()

    def cancel(self):
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = SettingsApp()
    app.run()