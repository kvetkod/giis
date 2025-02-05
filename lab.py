import tkinter as tk
from tkinter import ttk
import math


class LineDrawer:
    def __init__(self, canvas, scale=1.0):
        """
        :param canvas: Холст для рисования.
        :param scale: Масштаб – все координаты умножаются на этот коэффициент (по умолчанию 1.0).
        """
        self.canvas = canvas
        self.scale = scale
        self.thickness = 1.1  # для алгоритма Ву по умолчанию толщина фиксирована на 1

    def draw_pixel(self, x, y, color="black", alpha=1.0):
        """
        Рисует «пиксель» (окружность) с учетом масштабирования и прозрачности.
        Толщина используется как self.thickness.
        """
        x_scaled = x * self.scale
        y_scaled = y * self.scale
        r = (self.thickness * self.scale) / 2  # радиус = (толщина/2) * scale
        color_mod = self._fade_color(color, alpha)
        self.canvas.create_oval(
            x_scaled - r, y_scaled - r,
            x_scaled + r, y_scaled + r,
            fill=color_mod, outline=""
        )

    def _fade_color(self, color, alpha):
        """
        Имитация прозрачности для чёрного цвета:
          alpha = 1 дает чистый чёрный,
          alpha < 1 приближает цвет к белому.
        """
        if alpha < 1.0:
            shade = int(255 * (1 - alpha))
            return f"#{shade:02x}{shade:02x}{shade:02x}"
        return color

    def dda(self, x0, y0, x1, y1):
        """Алгоритм ЦДА"""
        dx = x1 - x0
        dy = y1 - y0
        steps = int(max(abs(dx), abs(dy)))
        if steps == 0:
            self.draw_pixel(x0, y0)
            return
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x0, y0
        for _ in range(steps + 1):
            self.draw_pixel(round(x), round(y))
            x += x_inc
            y += y_inc

    def bresenham(self, x0, y0, x1, y1):
        """Алгоритм Брезенхэма"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.draw_pixel(x0, y0)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def wu(self, x0, y0, x1, y1):
        """
        Алгоритм Ву
        """
        smoothing_range = 2.0

        # Определяем, является ли линия крутой. Если да, меняем оси.
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Гарантируем, что линия идёт слева направо.
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0
        gradient = dy / dx if dx != 0 else 0

        half_thickness = self.thickness / 2.0  # всегда 0.5, так как self.thickness == 1

        for x in range(x0, x1 + 1):
            ideal_y = y0 + gradient * (x - x0)
            y_min = int(math.floor(ideal_y - half_thickness - smoothing_range))
            y_max = int(math.ceil(ideal_y + half_thickness + smoothing_range))
            for y in range(y_min, y_max + 1):
                d = abs(y - ideal_y)
                if d <= half_thickness:
                    intensity = 1.0
                else:
                    intensity = max(0, 1 - (d - half_thickness) / smoothing_range)
                if intensity > 0.01:
                    if steep:
                        self.draw_pixel(y, x, alpha=intensity)
                    else:
                        self.draw_pixel(x, y, alpha=intensity)


class GraphicsEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Графический редактор")
        self.geometry("800x600")
        self.points = []  # Список для хранения точек
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="white", width=600, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        frame = tk.Frame(self)
        frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(frame, text="Алгоритм:").pack(pady=5)
        self.algorithm_combo = ttk.Combobox(
            frame, values=["Алгоритм ЦДА", "Алгоритм Брезенхэма", "Алгоритм Ву"],
            state="readonly"
        )
        self.algorithm_combo.current(0)
        self.algorithm_combo.pack(pady=5)

        ttk.Button(frame, text="Очистить", command=self.clear_canvas).pack(pady=5)
        self.info_label = ttk.Label(frame, text="Кликните для выбора точек.")
        self.info_label.pack(pady=10)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
        if len(self.points) == 2:
            self.draw_line()
            self.points = []

    def draw_line(self):
        x0, y0 = self.points[0]
        x1, y1 = self.points[1]
        algorithm = self.algorithm_combo.get()

        if algorithm == "Алгоритм Ву":
            drawer = LineDrawer(self.canvas, scale=1.0)
        else:
            drawer = LineDrawer(self.canvas, scale=1.0)
            drawer.thickness = 3  # Толщина для ЦДА и Брезенхэма

        if algorithm == "Алгоритм ЦДА":
            drawer.dda(x0, y0, x1, y1)
        elif algorithm == "Алгоритм Брезенхэма":
            drawer.bresenham(x0, y0, x1, y1)
        elif algorithm == "Алгоритм Ву":
            drawer.wu(x0, y0, x1, y1)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []


if __name__ == "__main__":
    app = GraphicsEditor()
    app.mainloop()