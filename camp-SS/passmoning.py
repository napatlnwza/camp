from tkinter import *
from turtle import *
import random
from PIL import Image as PILImage,ImageTk


tk = Tk()

def limit_input(P):
    return len(P) <= 4

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
    if ran == 1:
        pic=Toplevel(tk)
        pic.title("pear")
        img=PILImage.open('pear.jpg')
        img=img.resize((400,400))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500,pic.destroy)
    elif ran == 2:
        pic=Toplevel(tk)
        pic.title("")
        img=PILImage.open('cat.jpg')                   
        img=img.resize((400,400))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500,pic.destroy)
    elif ran == 3:
        pic=Toplevel(tk)
        pic.title("")
        img=PILImage.open('')                   #รูป
        img=img.resize((400,400))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500,pic.destroy)
    elif ran == 4:
        pic=Toplevel(tk)
        pic.title("")
        img=PILImage.open('')                   #รูป
        img=img.resize((400,400))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500,pic.destroy)
    elif ran == 5:
        pic=Toplevel(tk)
        pic.title("")
        img=PILImage.open('')                   #รูป
        img=img.resize((400,400))
        photo=ImageTk.PhotoImage(img)
        putphoto=Label(pic,image=photo)
        putphoto.image=photo
        putphoto.pack()
        pic.after(1500,pic.destroy)


def check():
    password = input1.get()

    if password == "1234" or password == "9999" or password == "0000":
        setup(width=600, height=600)
        title("")
        penup()
        hideturtle()
        sety(-200)
        setx(-75)
        write("Good Boy!",move=True,font=('Arial',26))
        color('green')
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
        hideturtle()
        penup()
        pensize(60)
        setx(-150)
        sety(150)
        right(45)
        speed(5)
        color('red')
        pendown()
        forward(350)
        penup()
        show_image_incorect()
        setx(-150)
        left(90)
        pendown()
        forward(350)
        penup()
        home()
        goto(-125,-250)
        write("ไปคิดใหม่ไปน้อง!!",move=True,font=('Arial',26))
        tk.after(1200, lambda: bye())
        
limit=(tk.register(limit_input),'%P')

tk.geometry("1200x700")
tk.title("Password checker")
bt = Button(tk,text="Check",command=check,width=15,height=2,bg='blue',font=('Arial',20),fg='white')
text=Label(text="กรอกเลยยย",font=('Arial',25))
input1 = Entry(bd=5,width=25,font=('Arial',25),validate="key",validatecommand=limit,justify="center",fg='red')
text.pack()
ling=PILImage.open('monkey.jpg')
ling2=ling.resize((300,300))
mon=ImageTk.PhotoImage(ling2)
putling=Label(tk,image=mon)

dog = PILImage.open("dog.jpg")
dog=dog.resize((250,250))
imgdog=ImageTk.PhotoImage(dog)
putdog=Label(tk,image=imgdog)

aum=PILImage.open('aum.jpg')
aum=ImageTk.PhotoImage(aum.resize((300,300)))
putaum=Label(tk,image=aum)

putdog.place(x=500,y=435)
putling.place(x=850,y=150)
putaum.place(x=100,y=150)
input1.place(x=450,y=270,height=50,width=350)
bt.place(x=500,y=325)
text.place(y=225,x=550)

tk.mainloop()