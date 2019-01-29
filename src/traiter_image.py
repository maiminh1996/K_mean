from PIL import Image, ImageTk
import numpy as np
from tkinter import filedialog



def load_image():
    path = filedialog.askopenfilename()
    load = Image.open(path)
    baseheight = 180
    hpercent = (baseheight / float(load.size[1]))
    wsize = int((float(load.size[0]) * float(hpercent)))
    img = load.resize((wsize, baseheight), Image.ANTIALIAS)
    return img


class traiterImage():

    def __init__(self, img):
        self.load = img

    def arrayToTkImage(self, img):
        print(img.shape)
        #img = np.resize(img, (229, np.int(np.floor(img.shape[1]*229/img.shape[0])), 3))
        print(img.shape)
        image = Image.fromarray(img)
        render = ImageTk.PhotoImage(image)
        return render

    def toArray(self, img):
        image = np.array(img)
        return image

    def imageToBlack(self):
        image = self.toArray(self.load)
        image = np.ones_like(image)
        # print(image.dtype)
        render = self.arrayToTkImage(image)
        return render

    def normalisation(self):
        image = self.toArray(self.load)
        max = np.max(image)
        min = np.min(image)
        image = np.array((image - min)*(255/(max-min)), np.uint8)
        # print(image.dtype)
        render = self.arrayToTkImage(image)
        return render

    def blackWhite(self):
        """
        Image RGB
        :return:
        """
        image = self.toArray(self.load)
        # image = image[:,:,0]
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                # image[i, j] = np.mean(image[i, j])
                if image[i, j, 0] < 210 and image[i, j, 0] < 160:
                    image[i, j] = np.mean(image[i, j]) # mean of 3 chaines
        return image

    def grayscale(self):
        image = self.toArray(self.load)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                image[i, j] = np.mean(image[i, j])
        max = np.max(image)
        min = np.min(image)
        image = np.array((image - min) * (255 / (max - min)), np.uint8)
        return image

    def img1scale(self):
        image = self.toArray(self.load)
        image[:, :, 0] = 0
        image[:, :, 2] = 0
        return image



