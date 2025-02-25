import tkinter as tk
from tkinter import messagebox
from line import LineDrawer
from curves import Curves

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
        self.debug_mode = False
        self.create_menu()
        self.algorithm = ""
        self.lines = LineDrawer()
        self.curves = Curves()
        

    def create_menu(self):
        self.menu = tk.Menu(self)

        algorithm_menu = tk.Menu(self.menu, tearoff=0)
        algorithm_menu.add_command(label="Алгоритм ЦДА", command=lambda: self.select_algorithm("Алгоритм ЦДА"))
        algorithm_menu.add_command(label="Алгоритм Брезенхэма", command=lambda: self.select_algorithm("Алгоритм Брезенхэма"))
        algorithm_menu.add_command(label="Алгоритм Ву", command=lambda: self.select_algorithm("Алгоритм Ву"))


        self.menu.add_cascade(label="Алгоритмы", menu=algorithm_menu)

        circle_algorithm = tk.Menu(self.menu, tearoff=0)
        circle_algorithm.add_command(label="Окружность", command=lambda: self.select_algorithm("Окружность"))
        circle_algorithm.add_command(label="Эллипс", command = lambda: self.select_algorithm("Эллипс"))
        circle_algorithm.add_command(label="Гипербола", command = lambda: self.select_algorithm("Гипербола"))
        circle_algorithm.add_command(label="Парабола", command=lambda: self.select_algorithm("Парабола"))
        self.menu.add_cascade(label="Алгоритмы кривых", menu=circle_algorithm)

        self.menu.add_command(label="Очистить", command=self.clear_canvas)
        self.debug_mode_var = tk.BooleanVar(value=self.debug_mode)
        self.menu.add_checkbutton(label="Режим отладки", variable=self.debug_mode_var, command=self.toggle_debug_mode)

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
        if self.algorithm == "Эллипс" and len(self.points) == 2:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")
        else: 
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
        if self.algorithm == "Окружность":
            self.draw_lines(self.curves.bresenham_circle(self.points[0], self.points[1]))
        if self.algorithm == "Эллипс":
            self.draw_lines(self.curves.bresenham_ellipse(self.points[0], self.points[1]))
        if self.algorithm == "Гипербола":
            self.draw_lines(self.curves.bresenham_hyperbola(self.points[0], self.points[1]))
        if self.algorithm == "Парабола":
            self.draw_lines(self.curves.bresenham_parabola(self.points[0], self.points[1]))
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
        self.debug_mode = self.debug_mode_var.get()

if __name__ == "__main__":
    app = App()
    app.mainloop()
