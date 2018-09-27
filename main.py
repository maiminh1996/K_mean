import numpy as np
import matplotlib.pyplot as plt


class K_mean():

    def __init__(self, k, epsilon=1, iteration=100):
        """
        initialisation
        :param k: number of centroids
        :param epsilon: erreur acceptable
        """
        self.k = k
        self.esl = epsilon
        self.itera = iteration

    def random_k_centroid(self, point):
        """
        colection of the points
        :param point:
        :return:
        """
        centroids = point.copy()  # ko lam thay doi point khi centroid thay doi
        np.random.shuffle(centroids)
        # print(point)
        return centroids[:self.k]  # return k first element

    def distance(self, a, b):
        """
        the distance between 2 points
        :param a: (2,)
        :param b: (2,)
        :return:
        """
        # print(a, b)
        dist = np.sqrt(np.power((a[0]-b[0]), 2) + np.power((a[1]-b[1]), 2))
        return dist

    def classement(self, point, centroids):
        """
        sap xep cac diem vao class
        :param point: 1 diem
        :param centroids: cac centroids
        :return:
        """
        # a= np.ones(shape=self.k)
        classe = []
        dem = 0
        # count =
        dist_min = 100000 # self.distance(point, centroids[0])
        for count, i in enumerate(range(self.k)):
            distance = self.distance(point, centroids[i])
            # print(count)
            if distance == 0:
                dist_min = distance
                dem = count + 1
                break
            elif distance < dist_min:
                dist_min = distance
                dem = count+1

        classe.append(dem)
        return classe

    def update_centroids(self, point, ind):
        """

        :param point: tap cac diem
        :param ind: index cua cac diem (1,2,3,4,5,6...), moi diem thuoc nhom nao LIST
        :return: centroid moi
        """
        x = y = 0
        j = 0
        centroids=np.array([[0, 0]]) # wrap
        get_indexes = lambda ind, xs: [i for (y, i) in zip(xs, range(len(xs))) if ind == y]

        for i in range(self.k):
            index = get_indexes(i + 1, ind)
            # print(index) # debug
            for j in index:
                # print(j) # debug
                x += point[j][0]
                y += point[j][1]
            k = np.array([[x/(j+1), y/(j+1)]])
            centroids = np.append(centroids, k, axis=0)
        centroids = centroids[1:]
        print(centroids)
        return centroids

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
    les_points = np.vstack(((np.random.randn(150, 2) * 0.75 + np.array([1, 0])),
                  (np.random.randn(50, 2) * 0.25 + np.array([-0.5, 0.5])),
                  (np.random.randn(50, 2) * 0.5 + np.array([-0.5, -0.5])))) # np.array([[0, 1], [1, 2], [0, 3], [500, 600], [10, 120], [40, 15]])
    # index = [1,2,1,3,2,2]
    # plt.scatter(les_points[:, 0], les_points[:, 1])
    # plt.show()
    a = K_mean(3)
    # choose randomly k centroids
    centroids = a.random_k_centroid(les_points)
    print(centroids)

    # vong lap traning
    for i in range(100):
        classe = []

        for j in les_points:
            # regroupe class for chaque point
            add = a.classement(j, centroids)
            # print(add)
            classe.append(add)
        classe = np.array(classe)
        classe = np.reshape(classe, (np.shape(les_points)[0],))
        print(classe)
        older = centroids

        # update centroids
        centroids = a.update_centroids(les_points, classe)

        if a.decalage_update(older, centroids)<0.000000000005:
            print("Centroids: \n", centroids)
            plt.scatter(les_points[:, 0], les_points[:, 1])
            plt.scatter(centroids[:, 0], centroids[:, 1], c='r', s=100)
            plt.show()
            break



    # b = a.random_k_centroid(les_points) # test random
    # c = a.distance(les_points[0], les_points[1]) # test distance
    # d=a.update_centroids(les_points, index)
    # e = a.classement([50,1], les_points)
    # print(e)

    # print(d)
    # print("distance test", c)
    # print(b)