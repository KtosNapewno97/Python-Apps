import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import soundfile as sf
import sounddevice as sd
import threading
import time
import os
import random

# ================== APPEARANCE ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================== APP ==================
app = ctk.CTk()
app.title("Media Player")
app.geometry("800x450")
app.resizable(False, False)

# ================== STATE ==================
audio_data = None
samplerate = 44100
duration = 0.0
current_pos = 0.0
playing = False
current_file = None

# ================== AUDIO ==================
def load_file():
    global audio_data, samplerate, duration, current_pos, current_file

    file = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.wav *.flac")]
    )
    if not file:
        return

    audio_data, samplerate = sf.read(file)
    duration = len(audio_data) / samplerate
    current_pos = 0.0
    current_file = file

    title_label.configure(text=os.path.basename(file))
    slider.configure(to=duration)
    slider.set(0)
    time_label.configure(text=f"00:00 / {format_time(duration)}")

def play():
    global playing
    if audio_data is None or playing:
        return

    playing = True
    threading.Thread(target=play_thread, daemon=True).start()
    animate_notes()

def play_thread():
    global current_pos, playing

    start_sample = int(current_pos * samplerate)
    sd.play(audio_data[start_sample:], samplerate)

    last_time = time.time()
    while playing and sd.get_stream().active:
        now = time.time()
        current_pos += now - last_time
        last_time = now

        if current_pos >= duration:
            break

        slider.set(current_pos)
        time_label.configure(
            text=f"{format_time(current_pos)} / {format_time(duration)}"
        )
        time.sleep(0.1)

    playing = False

def stop():
    global playing, current_pos
    sd.stop()
    playing = False
    current_pos = 0.0
    slider.set(0)
    time_label.configure(text=f"00:00 / {format_time(duration)}")
    canvas.delete("all")

def seek(value):
    global current_pos
    if audio_data is None:
        return

    current_pos = float(value)
    if playing:
        sd.stop()
        play()

# ================== UTILS ==================
def format_time(seconds):
    seconds = int(seconds)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

# ================== UI ==================

# HEADER
header = ctk.CTkFrame(app, height=60)
header.pack(fill="x", padx=15, pady=(15, 5))

title_label = ctk.CTkLabel(
    header,
    text="Nie wybrano pliku",
    font=ctk.CTkFont(size=16, weight="bold")
)
title_label.pack(side="left", padx=15)

open_btn = ctk.CTkButton(
    header,
    text="📂 Otwórz",
    width=120,
    command=load_file
)
open_btn.pack(side="right", padx=15)

# SLIDER
slider = ctk.CTkSlider(
    app,
    from_=0,
    to=100,
    command=seek
)
slider.pack(fill="x", padx=30, pady=20)

time_label = ctk.CTkLabel(
    app,
    text="00:00 / 00:00"
)
time_label.pack()

# ================== ANIMATION CANVAS ==================
canvas = tk.Canvas(
    app,
    height=120,
    bg="#1a1a1a",
    highlightthickness=0
)
canvas.pack(fill="x", padx=20, pady=10)

notes = []

def spawn_note():
    x = random.randint(20, 780)
    y = 120
    note = canvas.create_text(
        x, y,
        text="♪",
        fill="white",
        font=("Segoe UI", 18)
    )
    notes.append(note)

def animate_notes():
    if not playing:
        return

    if random.random() < 0.15 and len(notes) < 7:
        spawn_note()

    for note in notes[:]:
        canvas.move(note, 0, -3)
        _, y = canvas.coords(note)
        if y < -10:
            canvas.delete(note)
            notes.remove(note)

    app.after(50, animate_notes)

# ================== CONTROLS ==================
controls = ctk.CTkFrame(app)
controls.pack(pady=20)

play_btn = ctk.CTkButton(
    controls,
    text="▶ Play",
    width=120,
    height=40,
    command=play
)
play_btn.grid(row=0, column=0, padx=15)

stop_btn = ctk.CTkButton(
    controls,
    text="■ Stop",
    width=120,
    height=40,
    command=stop
)
stop_btn.grid(row=0, column=1, padx=15)

# ================== RUN ==================
app.mainloop()
