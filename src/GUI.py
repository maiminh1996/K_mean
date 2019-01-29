from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter as ttk
import traiter_image
import segmentation as KMEAN
import numpy as np
LARGE_FONT = ("Verdana", 12)


class GetShow(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_window()

        self.img = None  # par defaut
        self.img_type = None


    def init_window(self):
        self.parent.title("Image Processing")
        ####################### FRAME 1 #######################
        self.frame = ttk.Frame(self.parent, relief=RAISED, borderwidth=1, background="white")
        self.frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.l1 = ttk.Label(self.frame, text="Choose an image and show it here", background="white")
        # self.l1.place(x=50, y=50)  # pack(fill=BOTH)
        # self.l2 = ttk.Label(self.frame, text="", width=40)
        self.l1.pack(side='top')
        # self.l2.pack(side="top")
        self.l1.bind("<Enter>", self.on_enter)
        self.l1.bind("<Leave>", self.on_leave)
        # self.pack(fill=BOTH, expand=True)
        ####################### FRAME 2 #######################
        self.frame2 = ttk.Frame(self.parent)
        self.frame2.configure(relief=RAISED, borderwidth=1)
        self.frame2.pack(side='bottom', fill=BOTH, padx=5, pady=5)

        quitButton = ttk.Button(self.frame2, text="Cancel", command=self.exitt, font=LARGE_FONT)
        quitButton.pack(side=RIGHT, padx=5, pady=5)
        # quitButton2 = ttk.Button(self.frame, text="Can11cel")
        # quitButton2.pack(side=RIGHT, padx=5, pady=5)


        insertButton = ttk.Button(self.frame2, text="Choose", command=self.show_image, font=LARGE_FONT)
        insertButton.pack(side=RIGHT, padx=5, pady=5)
        clearButton = ttk.Button(self.frame2, text="Clear", command=self.clear_image, font=LARGE_FONT)
        clearButton.pack(side=LEFT, padx=5, pady=5)
        ####################### CREATE A MENU BAR #######################
        menu = ttk.Menu(self.parent)
        self.parent.config(menu=menu)
        # create an file
        file = Menu(menu)
        file.add_command(label="Exit", command=self.exitt)
        file.add_command(label="Saver Result", command=self.saver_image)
        menu.add_cascade(label="File", menu=file, font=LARGE_FONT)  # add file into menu barre
        # create an edit
        edit = Menu(menu)
        # edit.add_command(label="Show Image", command=self.saver_image)
        edit.add_command(label="Grayscale Image", command=self.grayscale)
        edit.add_command(label="One scale", command=self.image1scale)
        edit.add_command(label="Segmentation", command=self.Kmean)
        menu.add_cascade(label="Edit", menu=edit, font=LARGE_FONT)  # add edit into menu barre

    def on_enter(self, event):
        self.l1.configure(text="Hello world")

    def on_leave(self, enter):
        self.l1.configure(text="Choose an image and show it here")

    def exitt(self):
        exit()

    def load_image(self):
        path = filedialog.askopenfilename()  # get path of image
        try:
            load = Image.open(path)
        except AttributeError:
            # in the cas, you choose nothing
            print("Let's choose an image")
            return 0
        # Resize image
        if load.size[0] <= load.size[1]:
            baseheight = 180
            hpercent = (baseheight / float(load.size[1]))
            wsize = int((float(load.size[0]) * float(hpercent)))
            img = load.resize((wsize, baseheight), Image.ANTIALIAS)
            return img
        else:
            basewidth = 180
            hpercent = (basewidth / float(load.size[0]))
            hsize = int((float(load.size[1]) * float(hpercent)))
            img = load.resize((basewidth, hsize), Image.ANTIALIAS)
            return img

    def show_image(self):
        load = self.load_image()
        if load == 0:
            return 0

        # img_save0: image entrée, img_save: image après traiter
        self.img_save0 = load

        imgTk = ImageTk.PhotoImage(load)
        self.img = Label(self.frame, image=imgTk)
        self.img.image = imgTk
        self.img.pack(side=LEFT, padx=10, pady=10)
        self.l1.pack_forget()

    def grayscale(self):
        load = 0
        if self.img_save0 is not None:
            self.img_save = self.img_save0
            load = traiter_image.traiterImage(self.img_save).grayscale()

        self.img_save = Image.fromarray(load)

        self.create_label(load)

    def image1scale(self):
        load = 0
        if self.img_save0 is not None:
            self.img_save = self.img_save0
            load = traiter_image.traiterImage(self.img_save).img1scale()

        self.img_save = Image.fromarray(load)

        self.create_label(load)

    def Kmean(self):
        load = 0
        if self.img_save0 is not None:
            self.img_save = np.array(self.img_save0)
            c, load = KMEAN.K_mean(self.img_save, 4).output()

        self.img_save = Image.fromarray(load)

        self.create_label(load)

    def create_label(self, load):
        """
        Afficher image
        :param load: Image after traiter en form array
        :return:
        """
        a = Image.fromarray(load)
        imgTk = ImageTk.PhotoImage(a)
        self.img_type = Label(self.frame, image=imgTk)  # Label(self, image=render)
        self.img_type.image = imgTk
        self.img_type.pack(side=RIGHT, padx=10, pady=10)
        self.l1.pack_forget()

    def clear_image(self):
        if self.img_type is not None:
            self.img_type.pack_forget()
            self.img_type = None
            self.img_save = None
        elif self.img is not None:
            self.img.pack_forget()  # destroy() # grid_forget()
            self.img = None
            self.img_save0 = None

    def saver_image(self):
        a = new_window()
        ten_save = a.saisir_text()
        print(ten_save)
        ten_save += ".jpg"
        # print(ten_save)
        self.img_save.save("kmean.png")


class new_window():

    def __init__(self):
        self.t = None
        self.ten = None

    def box_check_color(self):
        self.t = ttk.Toplevel()

        self.t.wm_title("Color")
        l = ttk.Label(self.t, text="This is window")
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def saisir_text(self):
        self.t = ttk.Toplevel()

        self.t.wm_title("Color")
        username = ttk.StringVar()
        self.name = ttk.Entry(self.t, textvariable=username)
        self.name.pack()
        self.name.focus_set()
        #self.name.bind('<Return>', self.nhap)
        b = ttk.Button(self.t, text="get", width=10, command=self.callback)
        b.pack()
        # b.bind('<Button-1>', self.callback)

        # l = ttk.Label(self.t, text="This is window")
        # l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        print("sds",self.ten)
        self.ten = self.callback()
        print("minh",self.ten)
        return self.ten


    def callback(self):
        self.ten = self.name.get()
        return self.ten#self.t.destroy()

    def __del__(self):
        self.t.destroy()

if __name__=='__main__':
    root = ttk.Tk()
    root.geometry("400x400+800+30")
    w_screen = root.winfo_screenwidth()
    h_screen = root.winfo_screenheight()
    a = GetShow(root)
    root.mainloop()

