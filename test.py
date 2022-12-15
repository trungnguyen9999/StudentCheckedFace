from distutils.cmd import Command
from tkinter import Tk, Frame, BOTH
from tkinter.ttk import *
from turtle import bgcolor
import tkinter as tk

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    def initUI(self):
        self.parent.title("Diem danh sinh vien")
        self.style=Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        #txtMasoSV = tk.Label(self, text = "Name").place(x = 30, y = 50)
        entry1 = tk.Entry(self).place(x = 85, y = 50)
        
        btnCheckUser = Button(self, text="Kiem Tra", command=self.quit)
        btnCheckUser.place(x=220, y=350)
root = Tk()
root.geometry("500x400")
app = Example(root)
root.mainloop()