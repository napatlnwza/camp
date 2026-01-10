from turtle import *
from tkinter import *

def hello():
    Label(root,text="Hello").pack()

root = Tk()
root.title("Password checker")
root.geometry("950x750")
bt=Button(root,text="Submit",command=hello).pack(pady=350)
root.mainloop()