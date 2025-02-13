import tkinter as tk
from tkinter import messagebox
import math

class LineDrawer:
    def __init__(self):
        self.points = []
        

    def dda(self, points):
        self.points = []
        x0 = points[0][0]
        y0 = points[0][1]
        x1 = points[1][0]
        y1 = points[1][1]
        dx = x1 - x0
        dy = y1 - y0
        steps = int(max(abs(dx), abs(dy)))
        if steps == 0:
            self.points.append([x0, y0])
            #self.draw_pixel(x0, y0)
            return self.points
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x0, y0
        for _ in range(steps + 1):
            self.points.append([round(x), round(y)])
            #self.draw_pixel(round(x), round(y))
            x += x_inc
            y += y_inc

        return self.points
    
    def bresenham(self, points):
        self.points = []
        x0 = points[0][0]
        y0 = points[0][1]
        x1 = points[1][0]
        y1 = points[1][1]

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            #self.draw_pixel(x0, y0)
            self.points.append([x0, y0])
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return self.points

    def wu(self, points):
        self.points = []
        x0, y0 = points[0]
        x1, y1 = points[1]

        if x0 == x1 and y0 == y1:
            return [(x0, y0, "black")]

        dx = x1 - x0
        dy = y1 - y0
        steep = abs(dy) > abs(dx)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            dx, dy = dy, dx

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            dx, dy = -dx, -dy

        gradient = dy / dx if dx != 0 else 1.0

        def plot(x, y, intensity):
            intensity = max(0.0, min(intensity, 1.0))
            gray = int(255 * (1 - intensity))
            color = f"#{gray:02x}{gray:02x}{gray:02x}"
            if steep:
                self.points.append((y, x, color))
            else:
                self.points.append((x, y, color))

        xend = round(x0)
        yend = y0 + gradient * (xend - x0)
        xgap = self._rfpart(x0 + 0.5)
        xpxl1 = xend
        ypxl1 = math.floor(yend)
        plot(xpxl1, ypxl1, self._rfpart(yend) * xgap)
        plot(xpxl1, ypxl1 + 1, self._fpart(yend) * xgap)

        intery = yend + gradient

        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = self._fpart(x1 + 0.5)
        xpxl2 = xend
        ypxl2 = math.floor(yend)
        plot(xpxl2, ypxl2, self._rfpart(yend) * xgap)
        plot(xpxl2, ypxl2 + 1, self._fpart(yend) * xgap)

        for x in range(xpxl1 + 1, xpxl2):
            plot(x, math.floor(intery), self._rfpart(intery))
            plot(x, math.floor(intery) + 1, self._fpart(intery))
            intery += gradient

        return self.points

    @staticmethod
    def _fpart(x):
        return x - math.floor(x)

    @staticmethod
    def _rfpart(x):
        return 1 - LineDrawer._fpart(x)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Редактор")
        self.geometry("800x800")
        self.points = []
        self.canvas = tk.Canvas(self, bg="white", width=600, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Configure>", lambda event: self.draw_grid())
        self.create_menu()
        self.algorithm = ""
        self.lines = LineDrawer()
        self.debug_mode = False

    def create_menu(self):
        self.menu = tk.Menu(self)

        algorithm_menu = tk.Menu(self.menu, tearoff=0)
        algorithm_menu.add_command(label="Алгоритм ЦДА", command=lambda: self.select_algorithm("Алгоритм ЦДА"))
        algorithm_menu.add_command(label="Алгоритм Брезенхэма", command=lambda: self.select_algorithm("Алгоритм Брезенхэма"))
        algorithm_menu.add_command(label="Алгоритм Ву", command=lambda: self.select_algorithm("Алгоритм Ву"))


        self.menu.add_cascade(label="Алгоритмы", menu=algorithm_menu)
        self.menu.add_command(label="Очистить", command=self.clear_canvas)
        self.menu.add_command(label="Режим отладки", command=self.toggle_debug_mode)

        self.config(menu=self.menu)

    def draw_grid(self):
        self.canvas.delete("grid")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.grid_size = 5
        for x in range(0, width, self.grid_size):
            self.canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid")

        for y in range(0, height, self.grid_size):
            self.canvas.create_line(0, y, width, y, fill="lightgray", tags="grid")

    def select_algorithm(self, name):
        self.algorithm = name

    def on_canvas_click(self, event):
        if self.algorithm == "":
            messagebox.showerror("Error", "Не выбран алгоритм")
            return 
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
        print(self.points)
        if len(self.points) == 2:
            self.draw()
            self.points = []

    def draw(self):
        if self.algorithm == "Алгоритм ЦДА":
            self.draw_lines(self.lines.dda(self.points))
        if self.algorithm == "Алгоритм Брезенхэма":
            self.draw_lines(self.lines.bresenham(self.points))
        if self.algorithm == "Алгоритм Ву":
            self.draw_lines(self.lines.wu(self.points))
        print(self.algorithm, self.debug_mode)


    def draw_lines(self, points):
        for index, point in enumerate(points):
            if len(point) == 2:  
                x, y = point
                color = "black"
            elif len(point) == 3:  
                x, y, color = point

            
            if self.debug_mode:
                self.after(index * 10, self.draw_line, x, y, color)
                print(x, y)  
            else:
                self.draw_line(x, y, color)

    def draw_line(self, x, y, color):
        self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill=color)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.points = []
    
    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode

if __name__ == "__main__":
    app = App()
    app.mainloop()
