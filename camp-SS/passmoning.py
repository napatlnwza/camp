from tkinter import *
from turtle import *
import random
from PIL import Image as PILImage,ImageTk


tk = Tk()

def show_image_correct():
    ran=random.randint(1,5)
    if ran == 1:
        pic=Toplevel(tk)
        pic.title("guea")
        img1=PILImage.open('guea.jpg')
        img=img1.resize((250,250))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500, pic.destroy)
    elif ran == 2:
        pic=Toplevel(tk)
        pic.title("win")
        img=PILImage.open("win.jpg")
        img=img.resize((250,250))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500, pic.destroy)
    elif ran == 3:
        pic=Toplevel(tk)
        pic.title('a-show')
        img=PILImage.open("ashow.jpg")
        img=img.resize((250,250))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500,pic.destroy)
    elif ran == 4:
        pic=Toplevel(tk)
        pic.title("teng")
        img=PILImage.open("teng.jpeg")
        img=img.resize((250,250))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500,pic.destroy)
    elif ran == 5:
        pic=Toplevel(tk)
        pic.title("aum")
        img=PILImage.open("plengsui.jpg")
        img=img.resize((250,250))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500,pic.destroy)

def show_image_incorect():
    ran=random.randint(1,5)


def check():
    password = input1.get()

    if password == "1234":
        setup(width=600, height=600)
        title("")
        penup()
        hideturtle()
        sety(-200)
        setx(-75)
        color('green')
        write("Good Boy!",move=True,font=('Arial',26))
        sety(50)
        setx(-100)
        speed(4)
        pensize(60)
        show_image_correct()
        pendown()
        right(45)
        forward(75)
        left(90)
        forward(300)
        tk.after(1500, lambda: bye())
        input1.delete(0,END)
    else:
        setup(width=600, height=600)
        title("")
        penup()
        pensize(60)
        setx(-100)
        sety(100)
        right(45)
        speed(5)
        color('red')
        pendown()
        forward(350)
        penup()
        setx(-100)
        left(90)
        pendown()
        forward(350)
        hideturtle()
        tk.after(1500, lambda: bye())
        

tk.geometry("1200x700")
tk.title("Password checker")
input1 = Entry(bd=5,width=25,font=('Arial',25))
bt = Button(tk,text="Check",command=check,width=25,height=5)
text=Label(text="กรอกเลยยย",font=('Arial',25))
text.pack()
ling=PILImage.open('monkey.jpg')
ling2=ling.resize((300,300))
mon=ImageTk.PhotoImage(ling2)
putling=Label(tk,image=mon)

pleng1=PILImage.open('aum.jpg')
pleng2=ImageTk.PhotoImage(pleng1.resize((300,300)))
putpleng=Label(tk,image=pleng2)

putling.place(x=850,y=150)
putpleng.place(x=100,y=150)
input1.place(x=450,y=270,height=50,width=350)
bt.place(x=525,y=350)
text.place(y=225,x=550)

tk.mainloop()