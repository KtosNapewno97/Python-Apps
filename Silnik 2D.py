import customtkinter as ctk
from tkinter import Canvas, messagebox
import threading
import time
import random

# ----------------------------
# Global settings
# ----------------------------
FPS = 30
objects = []
running = True
current_tool = "platform"  # narzędzie edytora: "platform", "enemy"

# ----------------------------
# Game object
# ----------------------------
class GameObject:
    def __init__(self, x, y, w, h, color="red", dx=0, dy=0, logic_code=None, obj_type="platform"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.dx = dx
        self.dy = dy
        self.logic_code = logic_code
        self.obj_type = obj_type

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def run_logic(self):
        if self.logic_code:
            local_vars = {"self": self, "objects": objects, "random": random}
            try:
                exec(self.logic_code, {}, local_vars)
            except Exception as e:
                print(f"Logic error in object: {e}")

# ----------------------------
# Advanced AI
# ----------------------------
def ai_generate_level():
    """
    Generuje poziom logicznie:
    - Platformy w różnych wysokościach
    - Wrogowie na platformach
    - Przeszkody między platformami
    """
    global objects
    objects = []
    # Platformy
    y = 400
    while y > 50:
        plat_width = random.randint(100, 200)
        x = random.randint(50, 500)
        plat = GameObject(x=x, y=y, w=plat_width, h=20, color="green", obj_type="platform")
        objects.append(plat)
        # Dodaj wroga na platformie
        if random.random() < 0.5:
            enemy_logic = f"""
if self.x < objects[0].x: self.dx = 2
elif self.x > objects[0].x: self.dx = -2
else: self.dx = 0
"""
            enemy = GameObject(x=x + plat_width//2, y=y-30, w=30, h=30, color="blue",
                               logic_code=enemy_logic, obj_type="enemy")
            objects.append(enemy)
        y -= random.randint(80, 150)
    messagebox.showinfo("AI", "Poziom wygenerowany logicznie przez AI!")

# ----------------------------
# Editor logic
# ----------------------------
def apply_code():
    code = code_editor.get("1.0","end-1c")
    if not objects:
        messagebox.showinfo("Info", "Dodaj gracza lub wybierz obiekt!")
        return
    objects[0].logic_code = code
    messagebox.showinfo("Info", "Kod przypisany do obiektu 0 (gracza)!")

# ----------------------------
# Draw objects
# ----------------------------
def draw_objects():
    canvas.delete("all")
    for obj in objects:
        canvas.create_rectangle(obj.x, obj.y, obj.x+obj.w, obj.y+obj.h, fill=obj.color)

# ----------------------------
# Handle collisions
# ----------------------------
def handle_collisions():
    for i in range(len(objects)):
        for j in range(i+1, len(objects)):
            a = objects[i]
            b = objects[j]
            if (a.x < b.x + b.w and a.x + a.w > b.x and
                a.y < b.y + b.h and a.y + a.h > b.y):
                # Prosta reakcja: zatrzymanie
                if a.obj_type=="enemy" or b.obj_type=="enemy":
                    a.dx = a.dy = b.dx = b.dy = 0

# ----------------------------
# Game loop
# ----------------------------
def game_loop():
    global running
    while running:
        for obj in objects:
            obj.run_logic()
            obj.move()
        handle_collisions()
        draw_objects()
        time.sleep(1/FPS)

# ----------------------------
# Mouse editor
# ----------------------------
def on_canvas_click(event):
    global current_tool
    x, y = event.x, event.y
    if current_tool == "platform":
        plat = GameObject(x=x, y=y, w=100, h=20, color="green", obj_type="platform")
        objects.append(plat)
    elif current_tool == "enemy":
        enemy_logic = f"""
if self.x < objects[0].x: self.dx = 2
elif self.x > objects[0].x: self.dx = -2
else: self.dx = 0
"""
        enemy = GameObject(x=x, y=y, w=30, h=30, color="blue", logic_code=enemy_logic, obj_type="enemy")
        objects.append(enemy)

# ----------------------------
# GUI
# ----------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1300x700")
root.title("Advanced 2D Engine with AI and Level Editor")

# Panel boczny
panel = ctk.CTkFrame(root, width=300)
panel.pack(side="left", fill="y", padx=5, pady=5)

# Canvas gry
canvas = Canvas(root, width=950, height=700, bg="black")
canvas.pack(side="right", padx=5, pady=5)
canvas.bind("<Button-1>", on_canvas_click)

# --- Buttons ---
def add_player():
    player = GameObject(x=100, y=100, w=40, h=40, color="red", obj_type="player")
    objects.insert(0, player)
    messagebox.showinfo("Info", "Gracz dodany!")

def stop_game():
    global running
    running = False

def set_tool_platform(): 
    global current_tool
    current_tool = "platform"
def set_tool_enemy():
    global current_tool
    current_tool = "enemy"

ctk.CTkButton(panel, text="Dodaj gracza", command=add_player).pack(pady=5)
ctk.CTkButton(panel, text="AI: Generuj poziom", command=ai_generate_level).pack(pady=5)
ctk.CTkButton(panel, text="Narzędzie: Platforma", command=set_tool_platform).pack(pady=5)
ctk.CTkButton(panel, text="Narzędzie: Wróg", command=set_tool_enemy).pack(pady=5)
ctk.CTkButton(panel, text="Zastosuj kod do gracza", command=apply_code).pack(pady=5)
ctk.CTkButton(panel, text="Zatrzymaj grę", command=stop_game).pack(pady=5)

# --- Edytor kodu ---
ctk.CTkLabel(panel, text="Kod gracza (Python):").pack(pady=5)
code_editor = ctk.CTkTextbox(panel, width=280, height=150)
code_editor.pack(pady=5)

# --- Sterowanie graczem ---
def key_press(event):
    if not objects: return
    player = objects[0]
    if event.keysym == "Left": player.dx = -5
    elif event.keysym == "Right": player.dx = 5
    elif event.keysym == "Up": player.dy = -5
    elif event.keysym == "Down": player.dy = 5

def key_release(event):
    if not objects: return
    player = objects[0]
    player.dx = 0
    player.dy = 0

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# --- Start game loop ---
threading.Thread(target=game_loop, daemon=True).start()
root.mainloop()
running = False
