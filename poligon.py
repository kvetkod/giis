import numpy as np
from line import LineDrawer

class Poligon:

    def __init__(self):
        self.line = LineDrawer()


    def cross_product(self, o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def is_convex(self, polygon):
        n = 4

        convex = True
        sign = None
        for i in range(4):
            dot_sign = True
            if i == 3:
                o = polygon[3]
                a = polygon[0]
                b = polygon[1]
                cp = self.cross_product(o, a, b)
                if cp > 0:
                    if sign == None:
                        sign = True
                    else:
                        if sign == False:
                            return False
                elif cp < 0:
                    if sign == None:
                        sign = False
                    else:
                        if sign == True:
                            return False
            elif i == 2:
                o = polygon[2]
                a = polygon[3]
                b = polygon[0]
                cp = self.cross_product(o, a, b)
                if cp > 0:
                    if sign == None:
                        sign = True
                    else:
                        if sign == False:
                            return False
                elif cp < 0:
                    if sign == None:
                        sign = False
                    else:
                        if sign == True:
                            return False
            else:
                o = polygon[i]
                a = polygon[i+1]
                b = polygon[i+2]
                cp = self.cross_product(o, a, b)
                if cp > 0:
                    if sign == None:
                        sign = True
                    else:
                        if sign == False:
                            return False
                elif cp < 0:
                    if sign == None:
                        sign = False
                    else:
                        if sign == True:
                            return False


        sign = None
        for i in range(n):
            o, a, b = polygon[i], polygon[(i+1) % n], polygon[(i+2) % n]
            cp = self.cross_product(o, a, b)

            if cp != 0:  
                if sign is None:
                    sign = cp > 0
                elif sign != (cp > 0):
                    return False  

        return True

    
    def find_normals(self, polygon):
        normals = []
        for i in range(len(polygon)):
            p1, p2 = polygon[i], polygon[(i + 1) % len(polygon)]
            edge = np.array([p2[0] - p1[0], p2[1] - p1[1]])
            normal = np.array([-edge[1], edge[0]]) 
            normal = normal / np.linalg.norm(normal) 
            normals.append((p1, normal))
        return normals
    
    def convex_hull_graham(self, points):
        
        points = sorted(points)
        lower, upper = [], []
        
        for p in points:
            while len(lower) >= 2 and self.cross_product(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        for p in reversed(points):
            while len(upper) >= 2 and self.cross_product(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        p = lower[:-1] + upper[:-1]
        print("Полигон выпуклый:", self.is_convex(p))
        print("Нормали:", self.find_normals(p))
        return p
        
    def convex_hull_jarvis(self, points):
        
        if len(points) < 3:
            return points
        
        hull = []
        point_on_hull = min(points, key=lambda p: p[0])  
        
        while True:
            hull.append(point_on_hull)
            endpoint = points[0]
            
            for p in points[1:]:
                if endpoint == point_on_hull or self.cross_product(hull[-1], endpoint, p) < 0:
                    endpoint = p
                    
            point_on_hull = endpoint
            if endpoint == hull[0]:
                break
        print("Полигон выпуклый:", self.is_convex(hull))
        print("Нормали:", self.find_normals(hull))
        return hull
    