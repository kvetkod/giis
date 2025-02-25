import math

class Curves:
    def __init__(self):
        self.points = []

    def bresenham_circle(self, p1, p2):
        self.points = []
        
        xc, yc = p1  
        r = round(math.sqrt((p2[0] - xc) ** 2 + (p2[1] - yc) ** 2)) 

        x = 0
        y = r
        delta = 3 - 2 * r  
        
        self.plot_circle_points(xc, yc, x, y)

        while x <= y:
            x += 1
            if delta > 0:
                y -= 1
                delta += 4 * (x - y) + 10
            else:
                delta += 4 * x + 6
            
            self.plot_circle_points(xc, yc, x, y)

        return self.points

    def plot_circle_points(self, xc, yc, x, y):
        self.points.extend([
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ])

    def bresenham_ellipse(self, center, axes):
        self.points = []
        
        xc, yc = center
        #a, b = axes  # a - полуось по X, b - полуось по Y
        a = abs(xc - axes[0])
        b = abs(yc - axes[1])

        # Изменим полуоси на половину
        #a //= 2
        #b //= 2

        x = 0
        y = b
        a2 = a * a
        b2 = b * b

        # Параметры для первой половины (x < a, y < b)
        d1 = b2 - a2 * b + 0.25 * a2
        dx = 2 * b2 * x
        dy = 2 * a2 * y

        # Рисуем первую половину эллипса
        while dx < dy:
            self.plot_ellipse_points(xc, yc, x, y)
            x += 1
            if d1 < 0:
                dx += 2 * b2
                d1 += dx + b2
            else:
                y -= 1
                dx += 2 * b2
                dy -= 2 * a2
                d1 += dx - dy + b2

        # Параметры для второй половины (y < b)
        d2 = b2 * (x + 0.5) ** 2 + a2 * (y - 1) ** 2 - a2 * b2

        # Рисуем вторую половину эллипса
        while y >= 0:
            self.plot_ellipse_points(xc, yc, x, y)
            y -= 1
            if d2 > 0:
                dy -= 2 * a2
                d2 += a2 - dy
            else:
                x += 1
                dy -= 2 * a2
                dx += 2 * b2
                d2 += a2 - dy + dx

        return self.points

    def plot_ellipse_points(self, xc, yc, x, y):
        self.points.extend([
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y)
        ])

    def bresenham_hyperbola(self, center, axes, limit=500):
        self.points = []
        
        xc, yc = center
        a = abs(xc - axes[0])
        b = abs(yc - axes[1])

        x = a
        y = 0
        a2 = a * a
        b2 = b * b

        # Первая часть (x > a, y растет)
        d1 = b2 * (x + 0.5) ** 2 - a2 * (y + 1) ** 2 - a2 * b2
        dx = 2 * b2 * x
        dy = 2 * a2 * y

        count = 0
        while dx > dy and count < limit:
            self.plot_hyperbola_points(xc, yc, x, y)
            y += 1
            if d1 < 0:
                dy += 2 * a2
                d1 += dy + a2
            else:
                x += 1
                dx += 2 * b2
                dy += 2 * a2
                d1 += dy - dx + a2
            count += 1

        # Вторая часть (x продолжает увеличиваться)
        d2 = b2 * (x + 1) ** 2 - a2 * (y + 0.5) ** 2 - a2 * b2
        
        while x <= xc + 2 * a and count < limit:
            self.plot_hyperbola_points(xc, yc, x, y)
            x += 1
            if d2 > 0:
                dx += 2 * b2
                d2 += b2 - dx
            else:
                y += 1
                dx += 2 * b2
                dy += 2 * a2
                d2 += b2 - dx + dy
            count += 1

        return self.points

    def plot_hyperbola_points(self, xc, yc, x, y):
        self.points.extend([
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y)
        ])


    def bresenham_parabola(self, p1, p2):
        x1, y1 = p1  # Вершина параболы
        x2, y2 = p2  # Точка, задающая форму параболы

        # Определяем направление параболы
        upward = y2 > y1  # Если True, парабола направлена вверх. Если False — вниз.

        # Коэффициент крутизны параболы "a" в уравнении y = a * x^2
        a = abs(y2 - y1) / ((x2 - x1) ** 2)

        self.points = []  # Список для хранения точек
        x = 0
        y = 0

        # Первая часть (x растет быстрее)
        while 2 * a * x < 1:
            actual_y = y + y1 if upward else y1 - y  # Учитываем направление
            self.points.append((x + x1, actual_y))
            self.points.append((-x + x1, actual_y))  # Симметричная точка
            y = round(a * x ** 2)
            x += 1

        # Вторая часть (y растет быстрее)
        while y <= abs(y2 - y1):
            actual_y = y + y1 if upward else y1 - y  # Учитываем направление
            self.points.append((x + x1, actual_y))
            self.points.append((-x + x1, actual_y))  # Симметричная точка
            x = round((y / a) ** 0.5)
            y += 1

        return self.points

