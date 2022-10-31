#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import json
import win32com.client
import os
import sv_ttk
import darkdetect
import psutil
import ctypes
import time
import subprocess as sp
import threading
import discord
import asyncio
import ctypes as ct

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

src = os.path.join(os.getenv("APPDATA"),"Activity-Condenser")
settingssrc = os.path.join(src,"settings.json")
process = os.path.join(src,"process.json")
errors = os.path.join(src,"errors.json")

with open(settingssrc) as debug:
    startdebug = json.load(debug)


async def get_application_id():
  global tokenerror
  global IDvalue
  token = startdebug['Bot_Token']
  async with discord.Client(intents=discord.Intents.default()) as client:
    try:
      await client.login(token)
      IDvalue = client.application_id
      tokenerror = ''
      print('Token is valid')
    except:
      tokenerror = 'Error'
      IDvalue = '0'
      print('Token is invalid')

asyncio.run(get_application_id())

with open(process) as z:
    processfinal = json.load(z)

with open(settingssrc) as f:
    data = json.load(f)

if darkdetect.isDark():
    theme = 'dark'
    icontheme = 'settings-white.ico'
else:
    theme = 'light'
    icontheme = 'settings-dark.ico'

class SettingsApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.iconbitmap(icontheme)
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
        checkbutton1.configure(cursor="hand2",offvalue=0,onvalue=1,text="Run on startup",variable=self.run2,)
        checkbutton1.grid(column=0, pady="0 5", row=1)
        label3 = ttk.Label(frame2)
        label3.configure(text="Bot Token :")
        label3.grid(column=0, pady="0 5", row=6)
        entry2 = ttk.Entry(frame2)
        self.Token = tk.StringVar()
        self.Token.set(data['Bot_Token'])
        entry2.configure(textvariable=self.Token)
        entry2.delete("0", "end")
        entry2.insert("0", data['Bot_Token'])
        entry2.grid(column=0, pady="0 10", row=7)
        label4 = ttk.Label(frame2)
        label4.configure(text="Activity Refresh Frequence (min 15 seconds):")
        label4.grid(column=0, pady="0 5", row=11)
        spinbox1 = ttk.Spinbox(frame2)
        self.refresh = tk.IntVar()
        self.refresh.set(data['refresh_time'])
        spinbox1.configure(from_=15, textvariable=self.refresh, to=100)
        spinbox1.grid(column=0, pady="0 5", row=12)
        button1 = ttk.Button(frame2)
        button1.configure(cursor="hand2",text="Ok", width=12)
        button1.grid(column=0, pady="30 0", row=13, sticky="e")
        button1.configure(command=self.on_ok)
        self.button2 = ttk.Button(frame2)
        self.button2.configure(cursor="hand2", text="Cancel", width=12, state="normal")
        self.button2.grid(column=0, pady="30 0", row=13, sticky="w")
        self.button2.configure(command=self.cancel)
        separator3 = ttk.Separator(frame2)
        separator3.configure(orient="horizontal")
        separator3.grid(column=0, ipadx=100, pady="10 40", row=13)
        separator4 = ttk.Separator(frame2)
        separator4.configure(orient="horizontal")
        separator4.grid(column=0, ipadx=100, pady="0 40", row=1)
        entry3 = ttk.Entry(frame2)
        self.username = tk.StringVar()
        self.username.set(data['username'])
        entry3.configure(textvariable=self.username)
        entry3.delete("0", "end")
        entry3.insert("0", data['username'])
        entry3.grid(column=0, pady="0 10", row=10)
        label5 = ttk.Label(frame2)
        label5.configure(text="Username (with #) :")
        label5.grid(column=0, pady="0 5", row=9)
        checkbutton2 = ttk.Checkbutton(frame2)
        self.check2 = tk.IntVar()
        self.check2.set(data['checkonstart'])
        checkbutton2.configure(variable=self.check2, text="Check for updates on start")
        checkbutton2.grid(column=0, pady="0 5", row=2)
        frame2.pack(side="top")
        self.label10 = ttk.Label(frame2)
        self.appstatus = tk.StringVar(value='Invalid Token')
        self.label10.configure(text='label3', textvariable=self.appstatus, foreground='red')
        self.label10.grid(column=0, row=8,pady="0 10")
        if tokenerror == '':
            self.label10.grid_forget()
        else:
            pass
        sv_ttk.set_theme(theme)

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        if darkdetect.isDark():
            self.mainwindow.update()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ct.windll.user32.GetParent
            hwnd = get_parent(self.mainwindow.winfo_id())
            rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
            value = 2
            value = ct.c_int(value)
            set_window_attribute(hwnd, rendering_policy, ct.byref(value),ct.sizeof(value))
        else:
            pass
        self.mainwindow.mainloop()
        
    def on_ok(self):
        async def checktoken():
            global oktoclose
            global IDvalue
            token = self.Token.get()
            async with discord.Client(intents=discord.Intents.default()) as client:
                try:
                    await client.login(token)
                    print('Token is valid')
                    oktoclose = True
                    IDvalue = client.application_id
                    try:
                        self.label10.grid_forget()
                    except:
                        pass
                except:
                    print('Invalid Token')
                    oktoclose = False
                    IDvalue = 0
                    try:
                        self.label10.grid(column=0, row=8,pady="0 10")
                    except:
                        pass

        asyncio.run(checktoken())
        if oktoclose == True:
            run_on_start = self.run2.get()
            Client_ID = IDvalue
            Bot_Token = self.Token.get()
            refresh_time = self.refresh.get()
            username = self.username.get()
            checkonstart = self.check2.get()
            settings = {
                "run_on_start": run_on_start,
                "Client_ID": Client_ID,
                "Bot_Token": Bot_Token,
                "refresh_time": refresh_time,
                "username": username,
                "checkonstart": checkonstart
            }
            with open(settingssrc, 'w') as f:
                json.dump(settings, f, indent=4)
            
            if run_on_start == 1:
                src = os.path.join(os.getenv("APPDATA"),"Microsoft\Windows\Start Menu\Programs\Startup")
                pthtemp = os.path.dirname(os.path.realpath(__file__))
                pth = pthtemp + "\\start.vbs"
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
                else:
                    pass
            try:
                botprocess = processfinal['bot']
                appprocess = processfinal['app']
                botterminate = psutil.Process(botprocess)
                appterminate = psutil.Process(appprocess)
                appterminate.terminate()
                botterminate.terminate()
            except:
                pass
            t4 = threading.Thread(target=self.restart)
            t4.start()
            self.mainwindow.destroy()
        else:
            pass

    def restart(self):
        extProc = sp.Popen(['python','bot.py'])
        BotProcess = {"bot":extProc.pid}
        time.sleep(10)
        extProc2 = sp.Popen(['python','app.py'])
        AppProcess = {"app":extProc2.pid}
        Processjoin = {**BotProcess, **AppProcess}
        jsonString = json.dumps(Processjoin, indent=4, default=str)
        jsonFile = open(process, "w")
        jsonFile.write(jsonString)

    def cancel(self):
        self.mainwindow.destroy()

if __name__ == "__main__":
    app = SettingsApp()
    app.run()