import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class K_mean():

    def __init__(self, image, k, epsilon=1, iteration=10):
        """
        initialisation
        :param k: number of centroids
        :param epsilon: erreur acceptable
        """
        self.img = image
        self.shape_image = self.img.shape
        self.k = k
        self.esl = epsilon
        self.itera = iteration

    def random_k_centroid(self):
        """
        colection of the points
        :param image: anh 3D
        :return: tra ve k pixels bat ki
        """
        centroids = self.img.copy()  # ko lam thay doi point khi centroid thay doi
        np.random.shuffle(centroids)
        print(centroids[0:self.k, 0, :])
        return centroids[0:self.k, 0, :]  # return k first element

    def distance(self, p1, p2):
        """
        the distance between 2 points in 3D
        :param p1: (x,y,z)
        :param p2: (x,y,z)
        :return: khoang cach giua 1 diem va diem centroid
        """
        dist = np.sqrt(np.power((p1[0]-p2[0]), 2) + np.power((p1[1]-p2[1]), 2) + np.power((p1[2]-p2[2]), 2))
        return dist

    def classement(self, pixel, centroids):
        """
        sap xep cac diem vao class
        :param pixel: 1 diem
        :param centroids: cac centroids
        :return:
        """
        dem = 0
        dist_min = 10000 # self.distance(point, centroids[0])
        for count, i in enumerate(range(self.k)):
            distance = self.distance(pixel, centroids[i])
            if dist_min >= distance:
                dist_min = distance
                dem = count+1
        return dem

    def classe_image(self, centroids):
        """

        :param centroids:
        :return:
        """
        classe = np.zeros(shape=self.shape_image[0:2])
        for i in range(self.shape_image[0]):
            for j in range(self.shape_image[1]):
                classe[i, j] = self.classement(self.img[i, j], centroids)
        return classe

    def classTocentroid(self, centroids, classe):
        """

        :param centroids:
        :param classe:
        :return:
        """
        for i in range(self.shape_image[0]):
            for j in range(self.shape_image[1]):
                g = int(classe[i,j]-1)
                self.img[i, j] = centroids[g]
        return self.img

    def update_centroids(self, classe):
        """
        :param image: (H,W,3)
        :param classe: matrix 2D avec matrix.shape == image.shape[:,:,0] == (H,W) ex [[1,2,2,1,2], [2,2,2,1,1]]
        :return: centroid moi
        TEST
        img1 = np.array([[[1,2,3],[4,5,6], [7,8,9]], [[11,2,31],[40,51,6], [70,88,92]]])  #(1,2,3)
        classe = np.array([[1,1,3],[2,1,2]]), k=3
        a = update_centroids(img1,classe)
        """
        index = np.zeros_like(classe)
        ind = None
        centroids = np.array([[0, 0, 0]]) # wrap
        get_indexes = lambda ind, xs: [i for (y, i) in zip(xs, range(len(xs))) if ind == y]

        for i in range(self.k):  # chay cho k class
            count = 0
            x = y = z = 0
            for a in range(self.shape_image[0]):  # Hang thu a
                ind = get_indexes(i + 1, classe[a])  # [1,2,2,1,2] if a=0, return [0,3]
                for b in ind:  # Hang thu a, cot thu b
                    count += 1  # dem so luong cua moi group
                    index[a, b] = 1  # [1,0,0,1,0]
                    x += self.img[a, b, 0]
                    y += self.img[a, b, 1]
                    z += self.img[a, b, 2]

            k = np.array([[int(x / (count+0.00001)), int(y / (count+0.00001)), int(z / (count+0.00001))]])
            centroids = np.concatenate((centroids, k), axis=0)
            index = np.zeros_like(classe)
        centroids = centroids[1:]
        print("The new centroids is: \n", centroids)
        return centroids

    def output(self):
        centroids = self.random_k_centroid()
        for i in range(self.itera):
            print("Iteration ", i)
            a = self.classe_image(centroids)
            centroids = self.update_centroids(a)

        image = self.classTocentroid(centroids, a)
        return centroids, image

    def decalage_update(self, centroids, new_centroids):
        """

        :param centroids:
        :param new_centroids:
        :return:
        """
        erreur = 0
        for i in range(self.k):
            erreur += self.distance(centroids[i], new_centroids[i])
        return erreur


if __name__=='__main__':
    img = Image.open("dunglan.jpg")
    img = np.array(img)
    centroids, image = K_mean(img, 2).output()
    a = Image.fromarray(image)
    a.save("luu.png")

    plt.imshow(image)
    plt.show()
