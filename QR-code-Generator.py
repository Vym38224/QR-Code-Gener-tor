from tkinter import *
from tkinter import filedialog, colorchooser
import pyqrcode
from PIL import Image, ImageTk

class QRCodeGenerator:
    def __init__(self, root):
        self.window = root
        self.window.geometry('1000x600')
        self.window.title('QR-Code Generator')
        
        Label(self.window, text='Let’s Create QR Code', font='arial 15').pack(pady=10)
        self.s = StringVar()
        self.image_label = None
        
        Entry(self.window, textvariable=self.s, font='arial 15').pack()

        # Add set the size of the QR code in pixels
        size_frame = Frame(self.window)
        size_frame.pack(pady=10)
        Label(size_frame, text='Enter the size of the QR code in pixels:', font='arial 10').pack(side=LEFT)
        self.size = StringVar(value='200')  # Default size set to 200 pixels
        Entry(size_frame, textvariable=self.size, font='arial 10', width=5).pack(side=LEFT)

        # Create a frame for the buttons
        button_frame = Frame(self.window)
        button_frame.pack()

        Button(button_frame, text='Create', bg='light green', command=self.create_qrcode).pack(side=LEFT, padx=5)
        Button(button_frame, text='Create with Logo', bg='light green', command=self.create_qrcode_with_logo).pack(side=LEFT, padx=5)

        self.download_button = Button(self.window, text='Download', bg='light blue', command=self.download_qr)
        self.download_button.pack_forget()

        # Add color pickers for QR code and background
        color_frame = Frame(self.window)
        color_frame.pack(pady=10)
        self.qr_color = StringVar(value='#000000')  # Default QR code color is black
        self.bg_color = StringVar(value='#FFFFFF')  # Default background color is white
        Button(color_frame, text='Select QR Code Color', bg='beige', command=self.select_qr_color).pack(side=LEFT, padx=5)
        Button(color_frame, text='Select Background Color',bg='beige', command=self.select_bg_color).pack(side=LEFT, padx=5)
        
        Button(self.window, text='Upload & Decode', bg='light blue', command=self.upload_and_decode).pack()
        self.decoded_label = Label(self.window, text='', font='arial 12')
        self.decoded_label.pack()


    
    def select_qr_color(self):
        color_code = colorchooser.askcolor(title="Choose QR Code Color")
        if color_code:
            self.qr_color.set(color_code[1])
    
    def select_bg_color(self):
        color_code = colorchooser.askcolor(title="Choose Background Color")
        if color_code:
            self.bg_color.set(color_code[1])
    
    def create_qrcode(self):
        s1 = self.s.get()
        qr = pyqrcode.create(s1)
        qr.png('myqr.png', scale=6, module_color=self.qr_color.get(), background=self.bg_color.get())
        
        size = int(self.size.get())
        img = Image.open('myqr.png')
        img = img.resize((size, size), Image.LANCZOS)
        
        img = ImageTk.PhotoImage(img)
        panel = Label(self.window, image=img)
        panel.image = img  
        panel.pack()
        
        if self.image_label:
            self.image_label.destroy()
        self.image_label = panel
        
        self.download_button.pack_forget()
        self.download_button.pack(pady=10)

    def create_qrcode_with_logo(self):
        s1 = self.s.get()
        qr = pyqrcode.create(s1)
        qr.png('myqr.png', scale=6, module_color=self.qr_color.get(), background=self.bg_color.get())
        
        size = int(self.size.get())
        img = Image.open('myqr.png')
        img = img.resize((size, size), Image.LANCZOS)
        
        # Load the logo image
        logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if logo_path:
            logo = Image.open(logo_path)
            logo_size = size//2  
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            logo_position = ((size - logo_size) // 2, (size - logo_size) // 2)
            img.paste(logo, logo_position, logo)
        
        img = ImageTk.PhotoImage(img)
        panel = Label(self.window, image=img)
        panel.image = img  
        panel.pack()
        
        if self.image_label:
            self.image_label.destroy()
        self.image_label = panel
        
        self.download_button.pack_forget()
        self.download_button.pack(pady=10)
    
    def download_qr(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            size = int(self.size.get())
            img = Image.open('myqr.png')
            img = img.resize((size, size), Image.LANCZOS)
            img.save(file_path, 'PNG')
            print(f'QR Code Downloaded as {file_path}')
    
    def upload_and_decode(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            img = cv2.imread(file_path)
            detector = cv2.QRCodeDetector()
            data, bbox, _  = detector.detectAndDecode(img)
            if data:
                self.decoded_label.config(text=f'Decoded Data: {data}')
            else:
                self.decoded_label.config(text='No QR code found or unable to decode.')

if __name__ == "__main__":
    root = Tk()
    app = QRCodeGenerator(root)
    root.mainloop()