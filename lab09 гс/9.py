import tkinter as tk
from tkinter import colorchooser
import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def sub(self, v):
        return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)

    def add(self, v):
        return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length == 0: return Vector3(0, 0, 0)
        return Vector3(self.x / length, self.y / length, self.z / length)

    def cross(self, v):
        return Vector3(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x
        )

class LabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("№9")
        self.root.geometry("800x600")

        self.cam_r = 10.0
        self.cam_phi = 45
        self.cam_theta = 60
        
        self.light_r = 100
        self.light_phi = 45
        self.light_theta = 45
        self.light_color = (255, 255, 255)

        self.is_drawn = False

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Фигура", menu=file_menu)
        file_menu.add_command(label="Пирамида", command=self.activate_scene)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.draw) # Перерисовка при изменении размера

        self.controls = tk.Frame(self.main_frame, width=200, padx=10, pady=10)
        self.controls.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_controls()

    def create_controls(self):
        tk.Label(self.controls, text="Камера", font=("Arial", 10)).pack(pady=(0, 5))
        
        tk.Label(self.controls, text="Phi (φ) градусы:").pack()
        self.s_cam_phi = tk.Scale(self.controls, from_=0, to=360, orient=tk.HORIZONTAL, command=self.update_params)
        self.s_cam_phi.set(self.cam_phi)
        self.s_cam_phi.pack(fill=tk.X)

        tk.Label(self.controls, text="Theta (θ) градусы:").pack()
        self.s_cam_theta = tk.Scale(self.controls, from_=0, to=180, orient=tk.HORIZONTAL, command=self.update_params)
        self.s_cam_theta.set(self.cam_theta)
        self.s_cam_theta.pack(fill=tk.X)

        tk.Label(self.controls, text="Источник света", font=("Arial", 10)).pack(pady=(0, 5))

        tk.Label(self.controls, text="Phi (φ) градусы:").pack()
        self.s_light_phi = tk.Scale(self.controls, from_=0, to=360, orient=tk.HORIZONTAL, command=self.update_params)
        self.s_light_phi.set(self.light_phi)
        self.s_light_phi.pack(fill=tk.X)

        tk.Label(self.controls, text="Theta (θ) градусы:").pack()
        self.s_light_theta = tk.Scale(self.controls, from_=0, to=180, orient=tk.HORIZONTAL, command=self.update_params)
        self.s_light_theta.set(self.light_theta)
        self.s_light_theta.pack(fill=tk.X)

        tk.Button(self.controls, text="Выбрать цвет света", command=self.choose_color).pack(pady=10)

    def activate_scene(self):
        self.is_drawn = True
        self.draw()

    def update_params(self, _=None):
        if self.is_drawn:
            self.cam_phi = self.s_cam_phi.get()
            self.cam_theta = self.s_cam_theta.get()
            self.light_phi = self.s_light_phi.get()
            self.light_theta = self.s_light_theta.get()
            self.draw()

    def choose_color(self):
        color = colorchooser.askcolor(title="цвет света")[0]
        if color:
            self.light_color = color
            self.draw()

    def spherical_to_cartesian(self, r, phi_deg, theta_deg):
        phi = math.radians(phi_deg)
        theta = math.radians(theta_deg)
        
        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)
        return Vector3(x, y, z)

    def get_pyramid_geometry(self):
        size_base = 150
        h_base = size_base * math.sqrt(3) / 2
        p1 = Vector3(-size_base/2, -h_base/3, -50)
        p2 = Vector3(size_base/2, -h_base/3, -50)
        p3 = Vector3(0, 2*h_base/3, -50)

        size_top = 70
        h_top = size_top * math.sqrt(3) / 2
        z_top = 100
        p4 = Vector3(-size_top/2, -h_top/3, z_top)
        p5 = Vector3(size_top/2, -h_top/3, z_top)
        p6 = Vector3(0, 2*h_top/3, z_top)

        vertices = [p1, p2, p3, p4, p5, p6]

        faces = [
            [0, 2, 1],       # Нижняя
            [3, 4, 5],       # Верхняя
            [0, 1, 4, 3],    # Боковая 1
            [1, 2, 5, 4],    # Боковая 2
            [2, 0, 3, 5]     # Боковая 3
        ]
        return vertices, faces

    def project_point(self, v, width, height):
        rad_phi = math.radians(self.cam_phi)
        rad_theta = math.radians(self.cam_theta)

        x1 = v.x * math.cos(-rad_phi) - v.y * math.sin(-rad_phi)
        y1 = v.x * math.sin(-rad_phi) + v.y * math.cos(-rad_phi)
        z1 = v.z

        x2 = x1
        y2 = y1 * math.cos(-rad_theta) - z1 * math.sin(-rad_theta)
        z2 = y1 * math.sin(-rad_theta) + z1 * math.cos(-rad_theta)

        screen_x = width / 2 + x2
        screen_y = height / 2 - y2 # Y на экране вниз, поэтому минус
        
        return screen_x, screen_y, z2

    def calculate_lighting(self, face_verts, light_pos):

        center = Vector3(0,0,0)
        for v in face_verts:
            center = center.add(v)
        center.x /= len(face_verts)
        center.y /= len(face_verts)
        center.z /= len(face_verts)

        v1 = face_verts[1].sub(face_verts[0])
        v2 = face_verts[2].sub(face_verts[0])
        normal = v1.cross(v2).normalize()

        light_dir = light_pos.sub(center).normalize()

        diffuse = max(0, normal.dot(light_dir))

        base_color = (200, 200, 200) 
        
        r = int(base_color[0] * (self.light_color[0]/255) * diffuse)
        g = int(base_color[1] * (self.light_color[1]/255) * diffuse)
        b = int(base_color[2] * (self.light_color[2]/255) * diffuse)
        
        ambient = 40
        r = min(255, r + ambient)
        g = min(255, g + ambient)
        b = min(255, b + ambient)

        return f'#{r:02x}{g:02x}{b:02x}'

    def draw(self, event=None):
        self.canvas.delete("all")
        
        if not self.is_drawn:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        #info_text = (f"Камера (r, φ, θ): ({self.cam_r}, {self.cam_phi}°, {self.cam_theta}°)\n"
        #            f"Свет (r, φ, θ): ({self.light_r}, {self.light_phi}°, {self.light_theta}°)")
        #self.canvas.create_text(10, 10, anchor="nw", text=info_text, font=("Consolas", 10))

        light_pos = self.spherical_to_cartesian(self.light_r, self.light_phi, self.light_theta)
        
        vertices, faces = self.get_pyramid_geometry()

        faces_to_draw = []

        for face_indices in faces:
            face_verts_3d = [vertices[i] for i in face_indices]
            
            color = self.calculate_lighting(face_verts_3d, light_pos)

            proj_points = []
            z_sum = 0
            for v in face_verts_3d:
                sx, sy, sz = self.project_point(v, w, h)
                proj_points.append(sx)
                proj_points.append(sy)
                z_sum += sz
            
            avg_z = z_sum / len(face_indices)
            
            faces_to_draw.append({
                "points": proj_points,
                "z": avg_z,
                "color": color
            })

        faces_to_draw.sort(key=lambda x: x["z"])
        for face in faces_to_draw:
            self.canvas.create_polygon(face["points"], fill=face["color"], outline="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = LabApp(root)
    root.mainloop()