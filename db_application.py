#importit
import sqlite3
import sys
import tkinter as app
from tkinter import *



#Application class
class Application():
    #initialize app
    def __init__(self):
        #app window size
        app_width = 1200
        app_height = 600
        #create main app tkinter instance
        self.appWindow = app.Tk()
        self.appWindow.title("Tietokantasovellus")
        self.appWindow.geometry(f'{app_width}x{app_height}')

    #main loop
    def runApplication(self):
            self.appWindow.mainloop()





program = Application()
program.runApplication()









#database_create = tk.Button(self.appWindow, text = "Luo", command=lambda: self.add_db(database_name))
