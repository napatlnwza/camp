from tkinter import *

tk=Tk()

def check():
    password=input1.get()
    if password=="1234":
        out.delete(0,END)
        out.insert(0,"Correct")
    else:
        out.delete(0,END)
        out.insert(0,"Incorrect")


tk.title("Password checker")
tk.geometry("350x100")
text=Label(tk,text="Password:")
output=Label(tk,text="Result:")
input1=Entry(bd=2)
out=Entry(bd=2)
bt=Button(tk,text="Check",command=check)

text.grid(row=0,column=0)
output.grid(row=1,column=0)
input1.grid(row=0,column=1)
bt.grid(row=0,column=3,padx=15,pady=15)
out.grid(row=1,column=1)


tk.mainloop()