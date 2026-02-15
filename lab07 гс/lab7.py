import tkinter as tk
from tkinter import simpledialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Pyramid3D:
    def __init__(self):
        #координаты усечённой пирамиды
        self.bottom = np.array([
            [-2, -2, 0],  # A: нижняя левая задняя
            [2, -2, 0],   # B: нижняя правая задняя  
            [2, 2, 0],    # C: нижняя правая передняя
            [-2, -2, 0]
        ])
        self.top = np.array([
            [-1, -1, 2],  # A1: верхняя левая задняя
            [1, -1, 2],   # B1: верхняя правая задняя
            [1, 1, 2],    # C1: верхняя правая передняя
            [-1, -1, 2]
        ])

    def faces(self):
        b, t = self.bottom, self.top
        return [
            [b[0], b[1], b[2], b[3]],  # нижняя грань
            [t[0], t[1], t[2], t[3]],  # верхняя грань
            [b[0], b[1], t[1], t[0]],  # задняя грань
            [b[1], b[2], t[2], t[1]],  # правая грань
            [b[2], b[3], t[3], t[2]],  # передняя грань
            [b[3], b[0], t[0], t[3]]   # левая грань
        ]

    def is_face_visible(self, face, camera_pos):
        """Определяет, видима ли грань с позиции камеры"""
        if len(face) < 3:
            return False
            
        # Вычисляем нормаль к грани (должна быть направлена ВНУТРЬ пирамиды)
        v1 = face[1] - face[0]
        v2 = face[2] - face[0]
        normal = np.cross(v1, v2)
        
        # Вычисляем вектор от центра грани к камере
        center = np.mean(face, axis=0)
        view_vector = camera_pos - center
        
        # Нормализуем векторы
        if np.linalg.norm(normal) > 0:
            normal = normal / np.linalg.norm(normal)
        if np.linalg.norm(view_vector) > 0:
            view_vector = view_vector / np.linalg.norm(view_vector)
        
        # Если скалярное произведение положительное, грань видима
        return np.dot(normal, view_vector) > 0


class PyramidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №7 — Усечённая пирамида")

        # Параметры камеры
        self.default_theta = 315
        self.default_phi = 45
        self.theta = self.default_theta
        self.phi = self.default_phi

        self.pyramid = Pyramid3D()
        self.mode_hidden = False  # "Удаление невидимых граней"

        # Настройка matplotlib
        self.fig = plt.Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Меню
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Пирамида", menu=menu)
        menu.add_command(label="С удалением невидимых граней", command=self.show_with_hidden)
        menu.add_command(label="Без удаления невидимых граней", command=self.show_all)
        menu.add_separator()
        menu.add_command(label="Изменить положение камеры", command=self.change_camera)
        menu.add_command(label="Положение камеры по умолчанию", command=self.reset_camera)
        menu.add_separator()
        menu.add_command(label="Выход", command=root.quit)

        self.draw()

    def get_camera_position(self):
        """Вычисляет позицию камеры на основе углов theta и phi"""
        # Преобразуем сферические координаты в декартовы
        theta_rad = np.radians(self.theta)
        phi_rad = np.radians(self.phi)
        
        # Камера находится на расстоянии от объекта
        r = 10
        
        x = r * np.sin(phi_rad) * np.cos(theta_rad)
        y = r * np.sin(phi_rad) * np.sin(theta_rad)
        z = r * np.cos(phi_rad)
        
        return np.array([x, y, z])

    def draw(self):
        """Отрисовка пирамиды"""
        self.ax.clear()
        self.ax.mouse_init(rotate_btn=None, zoom_btn=None)
        mode_text = "С удалением невидимых граней" if self.mode_hidden else "Все грани"
        self.ax.set_title(f"Камера: θ={self.theta}°, φ={self.phi}°\nРежим: {mode_text}")
        self.ax.set_box_aspect([1, 1, 1])
        self.ax.view_init(elev=self.phi, azim=self.theta)

        faces = self.pyramid.faces()
        colors = [
            'blue',    # низ
            'red',     # верх
            'white',   # задняя
            'white',  # правая
            'white',  # передняя
            'white'    # левая
        ]

        # Получаем позицию камеры
        camera_pos = self.get_camera_position()

        if self.mode_hidden:
            # С удалением невидимых граней - отображаем только видимые грани
            visible_faces = []
            visible_colors = []
            
            for i, face in enumerate(faces):
                if self.pyramid.is_face_visible(face, camera_pos):
                    visible_faces.append(face)
                    visible_colors.append(colors[i])
            
            # Рисуем только видимые грани (полностью непрозрачные)
            for i, face in enumerate(visible_faces):
                poly = Poly3DCollection([face], color=visible_colors[i], edgecolor='black', alpha=1.0, linewidth=2)
                self.ax.add_collection3d(poly)
                
        else:
            # Без удаления — все грани (полупрозрачные)
            for i, face in enumerate(faces):
                poly = Poly3DCollection([face], color=colors[i], edgecolor='black', alpha=0.6, linewidth=1)
                self.ax.add_collection3d(poly)

        # Настройка осей
        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)
        self.ax.set_zlim(0, 3)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        # Убираем фон для лучшей видимости
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.grid(True, alpha=0.3)
        
        self.canvas.draw()

    def show_all(self):
        """Показать все грани"""
        self.mode_hidden = False
        self.draw()

    def show_with_hidden(self):
        """Удалить невидимые грани"""
        self.mode_hidden = True
        self.draw()

    def change_camera(self):
        """Изменить положение камеры"""
        theta = simpledialog.askfloat("Положение камеры", "Введите азимут (θ, градусы):", initialvalue=self.theta)
        phi = simpledialog.askfloat("Положение камеры", "Введите угол подъёма (φ, градусы):", initialvalue=self.phi)
        if theta is not None:
            self.theta = theta
        if phi is not None:
            self.phi = phi
        self.draw()

    def reset_camera(self):
        """Сбросить положение камеры"""
        self.theta = self.default_theta
        self.phi = self.default_phi
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PyramidApp(root)
    root.mainloop()