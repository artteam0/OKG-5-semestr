import tkinter as tk
from tkinter import simpledialog
import math
import numpy as np

class CPlot3D:
    def __init__(self):
        # Начальные значения координат камеры
        self.r = 10      
        self.theta = 45  
        self.phi = 45    
        self.scale = 40
        
    def set_camera(self, theta, phi, r=None):
        self.theta = theta
        self.phi = phi
        if r is not None:
            self.r = r
        
    def project_point(self, x, y, z):
        """Аксонометрическая проекция 3D точки в 2D (относительно 0,0)"""
        theta_rad = math.radians(self.theta)
        phi_rad = math.radians(self.phi)
        
        # Поворот вокруг оси Y
        x_rot = x * math.cos(theta_rad) + z * math.sin(theta_rad)
        z_rot = -x * math.sin(theta_rad) + z * math.cos(theta_rad)
        
        # Поворот вокруг оси X
        y_rot = y * math.cos(phi_rad) - z_rot * math.sin(phi_rad)
        z_final = y * math.sin(phi_rad) + z_rot * math.cos(phi_rad)
        
        # Проекция (масштабирование)
        x_2d = x_rot * self.scale
        y_2d = -y_rot * self.scale
        
        return x_2d, y_2d, z_final
        
    def elliptic_paraboloid(self, u, v):
        x = u
        y = v
        z = u**2 + v**2
        return x, y, z
        
    def hyperbolic_paraboloid(self, u, v):
        x = u
        y = v
        z = u**2 - v**2
        return x, y, z
        
    def hemisphere(self, u, v):
        R=3
        x = u
        y = v
        r = math.sqrt(u**2 + v**2)
        if r <= R:
            z = math.sqrt(R**2 - r**2)
        else:
            z = 0
        return x, y, z

class SurfaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №8 - Поверхности второго порядка")
        self.root.geometry("800x600")
        
        # Переменные для хранения текущего размера холста
        self.width = 800
        self.height = 600
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # ПРИВЯЗКА СОБЫТИЯ ИЗМЕНЕНИЯ РАЗМЕРА
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.plot3d = CPlot3D()
        self.current_surface = None
        
        self.create_menu()
        self.update_camera_display()

    def on_resize(self, event):
        """Обработчик изменения размера окна"""
        self.width = event.width
        self.height = event.height
        
        # Если поверхность уже выбрана, перерисовываем её под новый размер
        if self.current_surface:
            self.show_surface(self.current_surface)
        else:
            # Если поверхность не выбрана, просто обновляем инфо о камере (чтобы текст не уполз)
            self.update_camera_display()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        figure_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Фигура", menu=figure_menu)
        figure_menu.add_command(label="Эллиптический параболоид", command=lambda: self.show_surface("elliptic"))
        figure_menu.add_command(label="Гиперболический параболоид", command=lambda: self.show_surface("hyperbolic"))
        figure_menu.add_command(label="Полусфера", command=lambda: self.show_surface("hemisphere"))
        
        camera_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Положение камеры", menu=camera_menu)
        camera_menu.add_command(label="По умолчанию", command=self.set_default_camera)
        camera_menu.add_command(label="Изменить", command=self.change_camera_position)
        
    def update_camera_display(self):
        self.canvas.delete("camera_info")
        self.canvas.create_text(100, 20, text=f"θ={self.plot3d.theta}°, φ={self.plot3d.phi}°", 
                                font=("Arial", 12), tags="camera_info")
        
    def set_default_camera(self):
        self.plot3d.set_camera(45, 45, 10)
        if self.current_surface:
            self.show_surface(self.current_surface)
            
    def change_camera_position(self):
        try:
            theta = simpledialog.askfloat("Угол theta", "Введите угол theta:", initialvalue=self.plot3d.theta)
            phi = simpledialog.askfloat("Угол phi", "Введите угол phi:", initialvalue=self.plot3d.phi)
            if theta is not None and phi is not None:
                self.plot3d.set_camera(theta, phi)
                if self.current_surface:
                    self.show_surface(self.current_surface)
        except ValueError:
            pass
            
    def generate_surface_points(self, surface_type, steps=25):
        points = []
        if surface_type == "elliptic":
            func = self.plot3d.elliptic_paraboloid
            u_range = np.linspace(-2, 2, steps)
            v_range = np.linspace(-2, 2, steps)
        elif surface_type == "hyperbolic":
            func = self.plot3d.hyperbolic_paraboloid
            u_range = np.linspace(-2, 2, steps)
            v_range = np.linspace(-2, 2, steps)
        elif surface_type == "hemisphere":
        #self.plot3d.scale=100
            func = self.plot3d.hemisphere
            u_range = np.linspace(-3, 3, steps)
            v_range = np.linspace(-3, 3, steps)
        
        for u in u_range:
            row = []
            for v in v_range:
                x, y, z = func(u, v)
                x2d, y2d, depth = self.plot3d.project_point(x, y, z)
                row.append((x2d, y2d, depth))
            points.append(row)
        return points
        
    def painter_algorithm_draw(self, surface_type):
        points = self.generate_surface_points(surface_type)
        
        # 1. Находим границы проекции фигуры
        all_x = []
        all_y = []
        for row in points:
            for p in row:
                all_x.append(p[0])
                all_y.append(p[1])
        
        if not all_x: return

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        # 2. Вычисляем смещение для центра холста (динамически от текущих self.width/self.height)
        center_canvas_x = self.width / 2
        center_canvas_y = self.height / 2
        
        offset_x = center_canvas_x - (min_x + max_x) / 2
        offset_y = center_canvas_y - (min_y + max_y) / 2

        # 3. Создаем треугольники
        triangles = []
        for i in range(len(points) - 1):
            for j in range(len(points[i]) - 1):
                p1 = points[i][j]
                p2 = points[i][j+1]
                p3 = points[i+1][j+1]
                p4 = points[i+1][j]
                
                # Треугольник 1
                depth1 = (p1[2] + p2[2] + p3[2]) / 3
                triangles.append({'points': [p1, p2, p3], 'depth': depth1})
                
                # Треугольник 2
                depth2 = (p1[2] + p3[2] + p4[2]) / 3
                triangles.append({'points': [p1, p3, p4], 'depth': depth2})
        
        triangles.sort(key=lambda t: t['depth'])
        
        # 4. Рисуем со смещением
        for triangle in triangles:
            points_2d = [(p[0] + offset_x, p[1] + offset_y) for p in triangle['points']]
            
            # Раскраска
            if surface_type == "elliptic":
                val = (triangle['depth'] + 2) / 10
                depth_factor = max(0, min(1, val))
                blue = int(50 + 200 * depth_factor)
                color = f'#0000{blue:02x}'
            elif surface_type == "hyperbolic":
                val = (triangle['depth'] + 5) / 10
                depth_factor = max(0, min(1, val))
                red = int(50 + 200 * depth_factor)
                color = f'#{red:02x}0000'
            else:  # hemisphere
                val = (triangle['depth'] + 1) / 3
                depth_factor = max(0, min(1, val))
                green = int(50 + 200 * depth_factor)
                color = f'#00{green:02x}00'
            
            self.canvas.create_polygon(points_2d, fill=color, outline="black", width=1)
            
    def show_surface(self, surface_type):
        self.current_surface = surface_type
        self.canvas.delete("all")
        self.update_camera_display()
        
        self.painter_algorithm_draw(surface_type)
        
        titles = {
            "elliptic": "Эллиптический параболоид: z = x² + y²",
            "hyperbolic": "Гиперболический параболоид: z = x² - y²", 
            "hemisphere": "Верхняя полусфера: z = √(1 - x² - y²)"
        }
        
        # Подпись тоже центрируем относительно текущей ширины
        self.canvas.create_text(self.width/2, self.height - 30, text=titles[surface_type], 
                                font=("Arial", 14), fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = SurfaceApp(root)
    root.mainloop()