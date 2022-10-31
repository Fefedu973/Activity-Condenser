#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import darkdetect
import sv_ttk
import psutil
import os
import json
import subprocess as sp
import time
import threading
import ctypes as ct
import ctypes

myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

discord = None

if ("Discord.exe" in (p.name() for p in psutil.process_iter())) == True:
    discord = "Discord is running"
    discordcolor = 'green'
else: 
    discord = "Discord is not running"
    discordcolor = 'red'

src = os.path.join(os.getenv("APPDATA"),"Activity-Condenser")
errors = os.path.join(src,"errors.json")
process = os.path.join(src,"process.json")

with open(process) as z:
    processfinal = json.load(z)

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
        self.update = tk.StringVar()
        self.update.set('Reconnect')
        button2.configure(cursor="hand2", width=30, textvariable=self.update)
        button2.grid(column=0, pady="30 0", row=4, sticky="w")
        button2.configure(command=self.reconnect)
        self.label1 = ttk.Label(frame2)
        self.discordstatus = tk.StringVar(value=discord)
        self.label1.configure(text='label1', textvariable=self.discordstatus, foreground=discordcolor)
        self.label1.grid(column=0, row=3, sticky="ne")
        self.label3 = ttk.Label(frame2)
        self.appstatus = tk.StringVar(value=app)
        self.label3.configure(text='label3', textvariable=self.appstatus, foreground=appcolor)
        self.label3.grid(column=0, row=3, sticky="se")
        sv_ttk.set_theme(theme)
        frame2.pack(side="top")

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

    def ok(self):
        self.mainwindow.destroy()

    def reconnect(self):
        try :
            noerror = {"Errors":""}
            jsonString = json.dumps(noerror, indent=4, default=str)
            jsonFile = open(errors, "w")
            jsonFile.write(jsonString)
            jsonFile.close()
        except:
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
        self.discordstatus.set("Loading...")
        self.label1.configure(foreground='white')
        self.appstatus.set("Loading...")
        self.label3.configure(foreground='white')
        t1 = threading.Thread(target=self.restart)
        t1.start()
    
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
        time.sleep(5)
        with open(errors) as f:
            errorfinal = json.load(f)
        #change here to change wits self.configure and not variables + add something for the connect button
        if ("Discord.exe" in (p.name() for p in psutil.process_iter())) == True:
            self.discordstatus.set("Discord is running")
            self.label1.configure(foreground='green')
            buttondiscord = 'Done'
        else: 
            self.discordstatus.set("Discord is not running")
            self.label1.configure(foreground='red')
            buttondiscord = 'Failed'

        if errorfinal == {"Errors":""}:
            self.appstatus.set("Activity Condenser is running")
            self.label3.configure(foreground='green')
            button = "Done"
        else:
            self.appstatus.set(errorfinal['Errors'])
            self.label3.configure(foreground='red')
            button = 'Failed'
        
        if button == buttondiscord:
            if button == 'Failed':
                buttonfinal = 'Failed'
            else:
                buttonfinal = 'Done'
        else:
            buttonfinal = 'Failed'
        
        self.update.set(buttonfinal)
        time.sleep(5)
        self.update.set('Reconnect')
        print('done')

        #recoit les infos extProc1 et extProc2 puis kill le process puis relance le process avec sp.Popen et remet les infos dans le json puis met le texte en attente puis affiche les erreurs si il y en a sinon met Activity Condenser is running


if __name__ == "__main__":
    app = StatusApp()
    app.run()