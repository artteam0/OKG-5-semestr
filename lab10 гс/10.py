import tkinter as tk
from tkinter import colorchooser
import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length == 0: return Vector3(0, 0, 0)
        return Vector3(self.x / length, self.y / length, self.z / length)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def sub(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def mul(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def add(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

class SphereApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №10: 3D Шар (Сплошной)")
        self.width = 800
        self.height = 600
        
        self.draw_mode = 0 
        self.radius = 180.0

        self.light_r = 600.0
        self.light_phi = 45.0
        self.light_theta = 45.0
        self.light_color = (255, 255, 0)

        self.cam_r = 500.0
        self.cam_phi = 0.0
        self.cam_theta = 90.0

        self.create_menu()
        self.create_widgets()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        figure_menu = tk.Menu(menubar, tearoff=0)
        sphere_menu = tk.Menu(figure_menu, tearoff=0)
        
        sphere_menu.add_command(label="Диффузная модель", command=lambda: self.set_mode(1))
        sphere_menu.add_command(label="Зеркальная модель", command=lambda: self.set_mode(2))
        
        figure_menu.add_cascade(label="Шар", menu=sphere_menu)
        menubar.add_cascade(label="Фигура", menu=figure_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        control_frame = tk.Frame(self.root, width=200, bg="lightgray")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(control_frame, text="Источник света", bg="lightgray", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(control_frame, text="Phi (град)", bg="lightgray").pack()
        self.s_l_phi = tk.Scale(control_frame, from_=0, to=360, orient=tk.HORIZONTAL, command=self.on_param_change)
        self.s_l_phi.set(self.light_phi)
        self.s_l_phi.pack()
        
        tk.Label(control_frame, text="Theta (град)", bg="lightgray").pack()
        self.s_l_theta = tk.Scale(control_frame, from_=0, to=180, orient=tk.HORIZONTAL, command=self.on_param_change)
        self.s_l_theta.set(self.light_theta)
        self.s_l_theta.pack()

        tk.Button(control_frame, text="Выбрать цвет света", command=self.choose_color).pack(pady=5)
        
        tk.Label(control_frame, text="----------", bg="lightgray").pack(pady=5)
        tk.Label(control_frame, text="Камера (Наблюдатель)", bg="lightgray", font=("Arial", 10, "bold")).pack(pady=5)
        
        tk.Label(control_frame, text="Phi (град)", bg="lightgray").pack()
        self.s_c_phi = tk.Scale(control_frame, from_=0, to=360, orient=tk.HORIZONTAL, command=self.on_param_change)
        self.s_c_phi.set(self.cam_phi)
        self.s_c_phi.pack()
        
        tk.Label(control_frame, text="Theta (град)", bg="lightgray").pack()
        self.s_c_theta = tk.Scale(control_frame, from_=0, to=180, orient=tk.HORIZONTAL, command=self.on_param_change)
        self.s_c_theta.set(self.cam_theta)
        self.s_c_theta.pack()
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.info_text = self.canvas.create_text(10, 10, anchor=tk.NW, text="", font=("Courier", 10))

    def set_mode(self, mode):
        self.draw_mode = mode
        self.draw_scene()

    def on_param_change(self, val):
        self.light_phi = float(self.s_l_phi.get())
        self.light_theta = float(self.s_l_theta.get())
        self.cam_phi = float(self.s_c_phi.get())
        self.cam_theta = float(self.s_c_theta.get())
        self.draw_scene()

    def choose_color(self):
        color = colorchooser.askcolor(title="Цвет источника света")[0]
        if color:
            self.light_color = tuple(map(int, color))
            self.draw_scene()

    def sph_to_cart(self, r, phi_deg, theta_deg):
        rad_phi = math.radians(phi_deg)
        rad_theta = math.radians(theta_deg)
        x = r * math.sin(rad_theta) * math.cos(rad_phi)
        y = r * math.sin(rad_theta) * math.sin(rad_phi)
        z = r * math.cos(rad_theta)
        return Vector3(x, y, z)

    # Функция проекции точки (с учетом поворота камеры)
    def project_point(self, P_world, cx, cy):
        # 1. Поворот камеры (инвертированный)
        # Вокруг Z на -cam_phi
        cp = math.cos(math.radians(-self.cam_phi))
        sp = math.sin(math.radians(-self.cam_phi))
        x1 = P_world.x * cp - P_world.y * sp
        y1 = P_world.x * sp + P_world.y * cp
        z1 = P_world.z
        
        # Вокруг X на -cam_theta
        ct = math.cos(math.radians(-self.cam_theta))
        st = math.sin(math.radians(-self.cam_theta))
        y2 = y1 * ct - z1 * st # Это будет глубина (depth)
        z2 = y1 * st + z1 * ct
        x2 = x1
        
        # Проекция на экран
        scr_x = cx + x2
        scr_y = cy - z2
        return scr_x, scr_y, y2

    def draw_scene(self):
        self.canvas.delete("all")
        info = f"Light: r={self.light_r:.0f}, phi={self.light_phi:.0f}, theta={self.light_theta:.0f}\n"
        info += f"Camera: r={self.cam_r:.0f}, phi={self.cam_phi:.0f}, theta={self.cam_theta:.0f}"
        self.canvas.create_text(10, 10, anchor=tk.NW, text=info, font=("Courier", 10))
        
        if self.draw_mode == 0:
            return

        cx, cy = self.width / 2, self.height / 2
        light_pos = self.sph_to_cart(self.light_r, self.light_phi, self.light_theta)
        cam_pos = self.sph_to_cart(self.cam_r, self.cam_phi, self.cam_theta)
        
        polygons = []
        
        # Увеличим шаг для производительности, так как теперь рисуем полигоны
        d_theta = 10 
        d_phi = 10

        # Мы идем до 180 (theta) и 360 (phi), но range не включает правую границу,
        # поэтому для полигонов берем range так, чтобы i+d_theta не вылетал
        for theta in range(0, 180, d_theta):
            for phi in range(0, 360, d_phi):
                
                # 4 вершины одного "квадратика" на сфере
                # P1 -- P4
                # |    |
                # P2 -- P3
                
                # Углы для 4 точек
                t1, p1 = theta, phi
                t2, p2 = theta + d_theta, phi
                t3, p3 = theta + d_theta, phi + d_phi
                t4, p4 = theta, phi + d_phi

                # Координаты 4 точек в 3D
                V1 = self.sph_to_cart(self.radius, p1, t1)
                V2 = self.sph_to_cart(self.radius, p2, t2)
                V3 = self.sph_to_cart(self.radius, p3, t3)
                V4 = self.sph_to_cart(self.radius, p4, t4)

                # --- РАСЧЕТ ОСВЕЩЕНИЯ ---
                # Считаем освещение для ЦЕНТРА полигона (плоское затенение)
                center_theta = theta + d_theta/2
                center_phi = phi + d_phi/2
                P_center = self.sph_to_cart(self.radius, center_phi, center_theta)
                
                N = P_center.normalize() # Нормаль
                L = light_pos.sub(P_center).normalize() # Вектор света
                V = cam_pos.sub(P_center).normalize() # Вектор взгляда
                
                intensity = 0.0
                dot_nl = max(0.0, N.dot(L))
                diffuse = dot_nl
                
                if self.draw_mode == 1: # Диффузная
                    intensity = diffuse
                elif self.draw_mode == 2: # Зеркальная
                    R = N.mul(2 * dot_nl).sub(L).normalize()
                    spec_pow = 30
                    specular = 0.0
                    if dot_nl > 0:
                        specular = pow(max(0.0, R.dot(V)), spec_pow)
                    ambient = 0.2
                    intensity = ambient + 0.6 * diffuse + 0.5 * specular
                
                intensity = min(1.0, max(0.0, intensity))
                r_c = int(self.light_color[0] * intensity)
                g_c = int(self.light_color[1] * intensity)
                b_c = int(self.light_color[2] * intensity)
                hex_color = f'#{r_c:02x}{g_c:02x}{b_c:02x}'

                # --- ПРОЕКЦИЯ НА ЭКРАН ---
                sx1, sy1, d1 = self.project_point(V1, cx, cy)
                sx2, sy2, d2 = self.project_point(V2, cx, cy)
                sx3, sy3, d3 = self.project_point(V3, cx, cy)
                sx4, sy4, d4 = self.project_point(V4, cx, cy)
                
                # Средняя глубина полигона для сортировки
                avg_depth = (d1 + d2 + d3 + d4) / 4.0
                
                # Сохраняем полигон
                polygons.append({
                    'depth': avg_depth,
                    'coords': [sx1, sy1, sx2, sy2, sx3, sy3, sx4, sy4],
                    'color': hex_color
                })

        # Сортировка по глубине (алгоритм художника)
        # Рисуем от самых дальних (меньший depth) к ближним
        polygons.sort(key=lambda p: p['depth'])

        # Отрисовка
        for poly in polygons:
            # outline=poly['color'] убирает черные линии сетки, делая шар гладким
            self.canvas.create_polygon(poly['coords'], fill=poly['color'], outline=poly['color'])

if __name__ == "__main__":
    root = tk.Tk()
    app = SphereApp(root)
    root.mainloop()