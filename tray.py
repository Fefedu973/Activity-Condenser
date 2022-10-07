from infi.systray import SysTrayIcon
import os
import time
import subprocess as sp
import os



extProc = sp.Popen(['python','bot.py'])
time.sleep(10)
extProc2 = sp.Popen(['python','app.py'])


hover_text = "Activity condenser"
icon = "main.ico"
z = 0
def settings(sysTrayIcon):
    os.system("python settings.pyw")
def bye(sysTrayIcon):
    sp.Popen.terminate(extProc)
    sp.Popen.terminate(extProc2)
def do_nothing(sysTrayIcon):
    pass
def about(sysTrayIcon):
    os.system("python about.pyw")

menu_options = (('Settings...', 'settings.ico', settings),
                ('About', 'about.ico', about),
                ('-----', None, do_nothing),
                ('Quit', "quit.ico", SysTrayIcon.QUIT),
               )
sysTrayIcon = SysTrayIcon("main.ico", hover_text, menu_options, on_quit=bye, default_menu_index=1)
sysTrayIcon.start()
           
 
