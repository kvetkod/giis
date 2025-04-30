import numpy as np


class Parametric:

    def harmit_method(self, p1, p2, r1, r2):
        self.num_points = 1000
        H = np.array([[2, -2, 1, 1],
                  [-3, 3, -2, -1],
                  [0, 0, 1, 0],
                  [1, 0, 0, 0]])

        G = np.array([p1, p2, r1, r2])

        C = np.dot(H, G)

        self.points = []

        for t in np.linspace(0, 1, self.num_points):
            T = np.array([t**3, t**2, t, 1])
            point = np.dot(T, C)
            self.points.append(point)

        return np.array(self.points)


    def bezier_method(self, p1, p2, p3, p4):

        self.num_points = 1000

        H = np.array([[-1, 3, -3, 1],
                  [3, -6, 3, 0],
                  [-3, 3, 0, 0],
                  [1, 0, 0, 0]])

        G = np.array([p1, p2, p3, p4])

        C = np.dot(H, G)

        self.points = []

        for t in np.linspace(0, 1, self.num_points):
            T = np.array([t**3, t**2, t, 1])
            point = np.dot(T, C)
            self.points.append(point)

        return np.array(self.points)


    def b_spline_method(self, points):

        self.num_points = 200
        points = np.array(points)
        n = len(points)

        extended_points = np.concatenate((points, points[:3]), axis=0)

        M = np.array([
            [-1,  3, -3, 1],
            [ 3, -6,  3, 0],
            [-3,  0,  3, 0],
            [ 1,  4,  1, 0]
        ]) / 6.0

        spline_points = []

        for i in range(n):
            G = extended_points[i:i+4]

            C = M.dot(G)

            for t in np.linspace(0, 1, self.num_points):
                T = np.array([t**3, t**2, t, 1])
                point = T.dot(C)
                spline_points.append(point)

        self.points = np.array(spline_points)
        return self.points