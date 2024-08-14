import pyqrcode
import png
from pyqrcode import QRCode
import tkinter as Tk
from tkinter import *
from PIL import Image, ImageTk

window = Tk()  
window.geometry('300x350')
window.title('QR-Code Generator')
 
Label(window,text='Let’s Create QR Code',font='arial 15').pack()
s = StringVar()
image_label = None

def create_qrcode():
    global image_label
    s1=s.get()
    qr = pyqrcode.create(s1)
    qr.png('myqr.png', scale = 6)

    # načtení QR kódu
    img = Image.open('myqr.png')
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel = Label(window, image=img)
    panel.image = img  
    panel.pack()

    # Pokud QR existuje, nahraďte jej novým QR
    if image_label:
        image_label.destroy()
        image_label = panel
    else:
        image_label = panel

        
Entry(window,textvariable = s,font='arial 15').pack()
Button(window,text='create',bg='light green',command=create_qrcode).pack()



window.mainloop()
