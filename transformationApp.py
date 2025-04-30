import tkinter as tk
import numpy as np

class Transformation3DApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("3D Transformations")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.LEFT, padx=10)
        
        self.instructions = tk.Label(self.frame, text="Управление:\n"
                                      "Стрелки - перемещение\n"
                                      "A/D - поворот\n"
                                      "W/S - масштабирование\n"
                                      "P - перспектива\n"
                                      "Меню - выбор фигуры", justify=tk.LEFT)
        self.instructions.pack()
        
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.RIGHT)
        
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.shape_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Выбрать фигуру", menu=self.shape_menu)
        self.shape_menu.add_command(label="Куб", command=self.set_cube)
        self.shape_menu.add_command(label="Пирамида", command=self.set_pyramid)
        
        self.perspective_enabled = True  
        self.translation = np.array([0, 0, 0])  
        
        self.set_cube()  
        
        self.root.bind("<KeyPress>", self.on_key_press)
        self.draw()
        self.root.mainloop()
    
    def set_cube(self):
        self.object3D = np.array([
            [100, 100, 100, 1], [-100, 100, 100, 1], [-100, -100, 100, 1], [100, -100, 100, 1],
            [100, 100, -100, 1], [-100, 100, -100, 1], [-100, -100, -100, 1], [100, -100, -100, 1]
        ])
        self.edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
        self.draw()
    
    def set_pyramid(self):
        self.object3D = np.array([
            [0, 100, 0, 1],  
            [-100, -100, 100, 1], [100, -100, 100, 1], 
            [100, -100, -100, 1], [-100, -100, -100, 1]
        ])
        self.edges = [(0,1), (0,2), (0,3), (0,4), (1,2), (2,3), (3,4), (4,1)]
        self.draw()
    
    def transform(self, matrix):
        self.object3D = np.dot(self.object3D, matrix.T)
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")
        for edge in self.edges:
            p1 = self.project(self.object3D[edge[0]])
            p2 = self.project(self.object3D[edge[1]])
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="black")
    
    def project(self, point):
        adjusted_point = point[:3] + self.translation  
        if self.perspective_enabled:
            d = 400  
            perspective = d / (d + adjusted_point[2])  
            x = adjusted_point[0] * perspective + 300  
            y = -adjusted_point[1] * perspective + 300  
        else:
            x, y = adjusted_point[0] + 300, -adjusted_point[1] + 300  
        return x, y
    
    def on_key_press(self, event):
        if event.keysym == "Right":
            self.translation += np.array([10, 0, 0])
        elif event.keysym == "Left":
            self.translation += np.array([-10, 0, 0])
        elif event.keysym == "Up":
            self.translation += np.array([0, 10, 0])
        elif event.keysym == "Down":
            self.translation += np.array([0, -10, 0])
        elif event.keysym == "a":
            angle = np.radians(5)
            self.transform(np.array([
                [np.cos(angle), 0, np.sin(angle), 0], 
                [0, 1, 0, 0], 
                [-np.sin(angle), 0, np.cos(angle), 0], 
                [0, 0, 0, 1]
            ]))
        elif event.keysym == "d":
            angle = np.radians(-5)
            self.transform(np.array([
                [np.cos(angle), 0, np.sin(angle), 0], 
                [0, 1, 0, 0], 
                [-np.sin(angle), 0, np.cos(angle), 0], 
                [0, 0, 0, 1]
            ]))
        elif event.keysym == "s":
            self.transform(np.array([
                [1.1, 0, 0, 0], 
                [0, 1.1, 0, 0], 
                [0, 0, 1.1, 0], 
                [0, 0, 0, 1]
            ]))
        elif event.keysym == "w":
            self.transform(np.array([
                [0.9, 0, 0, 0], 
                [0, 0.9, 0, 0], 
                [0, 0, 0.9, 0], 
                [0, 0, 0, 1]
            ]))
        elif event.keysym == "p":
            self.perspective_enabled = not self.perspective_enabled  
        
        self.draw()

if __name__ == "__main__":
    Transformation3DApp()