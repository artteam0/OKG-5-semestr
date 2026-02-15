import tkinter as tk
import math
import sys

class BladeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №5 - Лопасть")
        self.root.geometry("800x600")
        
        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
        self.canvas.pack()

        self.create_control_panel()
        
        self.base_width = 10
        self.tip_width = 60
        self.h = 200
        self.angle = 0
        self.rotating = False
        self.blades_visible = False
        self.direction = 1

        self.target_rpm = 30    
        self.frame_delay_ms = 20 
        self.angle_per_frame = self.calculate_angle_per_frame(self.target_rpm, self.frame_delay_ms)
        self.num_blades = 2

        self.create_menu()
        
        self.canvas.bind("<Double-Button-1>", self.toggle_rotation)  
        self.canvas.bind("<Double-Button-3>", self.stop_rotation)    

    def create_control_panel(self):
        control_frame = tk.Frame(self.root, height=100)
        control_frame.pack(fill=tk.X, side=tk.BOTTOM)
        control_frame.pack_propagate(False)
        tk.Label(control_frame, text="лопасти:").grid(row=0, column=0, padx=5, pady=2)
        self.blades_var = tk.StringVar(value="2")
        blades_spinbox = tk.Spinbox(control_frame, from_=2, to=20, width=5, textvariable=self.blades_var,
                                   command=self.update_blades)
        blades_spinbox.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(control_frame, text="скорость:").grid(row=0, column=2, padx=5, pady=2)
        self.speed_var = tk.StringVar(value="5")
        speed_scale = tk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL, 
                              variable=self.speed_var, length=150, showvalue=True,
                              command=self.update_speed)
        speed_scale.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(control_frame, text="направление:").grid(row=0, column=4, padx=5, pady=2)
        self.direction_var = tk.StringVar(value="по часовой")
        direction_menu = tk.OptionMenu(control_frame, self.direction_var, "по часовой", "против часовой")
        direction_menu.grid(row=0, column=5, padx=5, pady=2)

        start_btn = tk.Button(control_frame, text="Старт", command=self.start_rotation)
        start_btn.grid(row=0, column=6, padx=5, pady=2)
        
        stop_btn = tk.Button(control_frame, text="Стоп", command=self.stop_rotation)
        stop_btn.grid(row=0, column=7, padx=5, pady=2)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)     
        lab_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Лабораторная №5", menu=lab_menu)
        lab_menu.add_command(label="Лопасть", command=self.show_blades)

    def show_blades(self):
        if not self.blades_visible:
            self.blades_visible = True
            self.draw_blades()

    def draw_blades(self):
        self.canvas.delete("all")
        
        center_x, center_y = 400, 250
        
        angle_rad = math.radians(self.angle)

        if self.num_blades %2==0:
            colors=["red", "blue"]
        else: 
            colors=["black", "cyan", "yellow"]
        
        for i in range(self.num_blades): 
            blade_angle = i * (360 / self.num_blades)
            current_angle_rad = angle_rad + math.radians(blade_angle)
            
            base_left_x = center_x - self.base_width * math.cos(current_angle_rad)
            base_left_y = center_y - self.base_width * math.sin(current_angle_rad)
            
            base_right_x = center_x + self.base_width * math.cos(current_angle_rad)
            base_right_y = center_y + self.base_width * math.sin(current_angle_rad)
            
            tip_x = center_x + self.h * math.sin(current_angle_rad)
            tip_y = center_y - self.h * math.cos(current_angle_rad)
            
            tip_left_x = tip_x - self.tip_width * math.cos(current_angle_rad)
            tip_left_y = tip_y - self.tip_width * math.sin(current_angle_rad)
            
            tip_right_x = tip_x + self.tip_width * math.cos(current_angle_rad)
            tip_right_y = tip_y + self.tip_width * math.sin(current_angle_rad)

            color=colors[i%len(colors)]
            
            self.canvas.create_polygon(
                base_left_x, base_left_y,
                base_right_x, base_right_y,
                tip_right_x, tip_right_y,
                tip_left_x, tip_left_y,
                fill=color, outline="black", width=1
            )
        
        self.canvas.create_oval(
            center_x - 20, center_y - 20,
            center_x + 20, center_y + 20,
            fill="green", outline="green"
        )

    def calculate_angle_per_frame(self, rpm, delay_ms):
        frames_per_second = 1000 / delay_ms
        degrees_per_second = rpm * 360 / 60
        angle_delta = degrees_per_second / frames_per_second
        return angle_delta

    def update_blades(self):
        self.num_blades = int(self.blades_var.get())
        if self.blades_visible:
            self.draw_blades()

    def update_speed(self, value):
        self.target_rpm = int(value)
        self.angle_per_frame = self.calculate_angle_per_frame(self.target_rpm, self.frame_delay_ms)

    def start_rotation(self):
        if not self.rotating and self.blades_visible:
            self.rotating = True
            self.direction = 1 if self.direction_var.get() == "по часовой" else -1
            self.rotate()

    def stop_rotation(self, event=None):
        if self.blades_visible:
            self.rotating = False

    def toggle_rotation(self, event):
        if self.blades_visible:
            self.rotating = not self.rotating
            if self.rotating:
                self.direction = 1 if self.direction_var.get() == "по часовой" else -1
                self.rotate()

    def rotate(self):
        if self.rotating and self.blades_visible:
            self.angle = (self.angle + self.angle_per_frame * self.direction) % 360
            self.draw_blades()
            self.root.after(self.frame_delay_ms, self.rotate)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = BladeApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Нажмите Enter для выхода...")