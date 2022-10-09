from infi.systray import SysTrayIcon
import os
import time
import subprocess as sp

extProc = sp.Popen(['python','bot.py'])
print(extProc)
time.sleep(10)
extProc2 = sp.Popen(['python','app.py'])

#creer un fichier json qui contient extProc et extProc2 et qui les envois à settings.pyw pour les kill quand on met à jour les paramètres

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

menu_options = (('Settings...', 'settings.ico', settings),
                ('Status', 'health.ico', status),
                ('About', 'about.ico', about),
                ('-----', None, do_nothing),
                ('Quit', "quit.ico", SysTrayIcon.QUIT),
               )
sysTrayIcon = SysTrayIcon("main.ico", hover_text, menu_options, on_quit=bye, default_menu_index=1)
sysTrayIcon.start()
           
 
