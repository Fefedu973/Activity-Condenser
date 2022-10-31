from infi.systray import SysTrayIcon
import os
import time
import subprocess as sp
import json

def start():
    global extProc
    global extProc2
    src = os.path.join(os.getenv("APPDATA"),"Activity-Condenser")
    process = os.path.join(src,"process.json")
    extProc = sp.Popen(['python','bot.py'])
    BotProcess = {"bot":extProc.pid}
    time.sleep(10)
    extProc2 = sp.Popen(['python','app.py'])
    AppProcess = {"app":extProc2.pid}
    Processjoin = {**BotProcess, **AppProcess}
    jsonString = json.dumps(Processjoin, indent=4, default=str)
    jsonFile = open(process, "w")
    jsonFile.write(jsonString)
start()

#creer un fichier json qui contient les PIDs de extProc et de extProc2 et qui les envois à settings.pyw pour les kill quand on met à jour les paramètres

hover_text = "Activity condenser"
icon = "main.ico"
z = 0
def settings(sysTrayIcon):
    os.system("python settings.pyw")
def bye(sysTrayIcon):
    sp.Popen.terminate(extProc)
    sp.Popen.terminate(extProc2)
    #remplacer par les infos dans le json
def do_nothing(sysTrayIcon):
    pass
def about(sysTrayIcon):
    os.system("python about.pyw")
def status(sysTrayIcon):
    os.system("python status.pyw")

menu_options = (('Settings...', 'settings-dark.ico', settings),
                ('Status', 'health-dark.ico', status),
                ('About', 'about-dark.ico', about),
                ('-----', None, do_nothing),
                ('Quit', "quit.ico", SysTrayIcon.QUIT),
               )
sysTrayIcon = SysTrayIcon("main.ico", hover_text, menu_options, on_quit=bye, default_menu_index=1)
sysTrayIcon.start()
           
 
