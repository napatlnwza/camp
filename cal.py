from tkinter import *


tk=Tk()
tk.title("Calculator")
tk.geometry("500x500")

t1=Label(tk,text="Number 1:")
t2=Label(tk,text="Number 2:")
t3=Label(tk,text="Result:")
t1.grid(row=0,column=0)
t2.grid(row=1,column=0)
t3.grid(row=3,column=0)
num1=Entry(tk)
num2=Entry(tk)
num1.grid(row=0,column=1)
num2.grid(row=1,column=1)
choice=IntVar()
ch1=Radiobutton(text="Plus",variable=choice,value=1)
ch1.var=choice
ch1.grid(row=2,column=0)
ch2=Radiobutton(text="Minus",variable=choice,value=2)
ch2.var=choice
ch2.grid(row=2,column=1)
ch3=Radiobutton(text="Times",variable=choice,value=3)
ch3.var=choice
ch3.grid(row=2,column=2)
ch4=Radiobutton(text="Divide",variable=choice,value=4)
ch4.var=choice
ch4.grid(row=2,column=3)
ch5=Radiobutton(text="Power",variable=choice,value=5)
ch5.var=choice
ch5.grid(row=2,column=4)

def calculate():
    n1=int(num1.get())
    n2=int(num2.get())
    r=0
    if choice.get()==1:
        r=n1+n2
    elif choice.get()==2:
        r=n1-n2
    elif choice.get()==3:
        r=n1*n2
    elif choice.get()==4:
        if n2==0:
            r="Can't not divide by Zero"
        else:
            r=n1/n2
    elif choice.get()==5:
        r=n1**n2
    out.delete(0,END)
    out.insert(0,r)


bt=Button(tk,text="Calculate",command=calculate)
bt.grid(row=4,column=0)
out=Entry(tk)
out.grid(row=3,column=1)
tk.mainloop()