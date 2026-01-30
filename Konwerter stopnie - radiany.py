import tkinter as tk
from tkinter import ttk
import math


# ======== DEFINICJE FUNKCJI =======
def sin_deg(x):
    return math.sin(math.radians(x))


def cos_deg(x):
    return math.cos(math.radians(x))


def tan_deg(x):
    return math.tan(math.radians(x))


def sin_rad(x):
    return math.sin(x)


def cos_rad(x):
    return math.cos(x)


def tan_rad(x):
    return math.tan(x)


def atan_deg(x):
    return math.degrees(math.atan(x))


def atan_rad(x):
    return math.atan(x)


def atan2_deg(y, x):
    return math.degrees(math.atan2(y, x))


def atan2_rad(y, x):
    return math.atan2(y, x)


def atanh_deg(x):
    return math.degrees(math.atanh(x))


def atanh_rad(x):
    return math.atanh(x)


def log_base_e(x):
    return math.log(x)


# --- Konwersja stopnie/radiany (pomocnicze) ---
def deg_to_rad(x):
    return math.radians(x)


def rad_to_deg(x):
    return math.degrees(x)


# ===============
# SŁOWNIK FUNKCJI
# ===============
# Łatwe wywołanie funkcji po nazwie z GUI
funkcje = {
    "sin (deg)": sin_deg,
    "cos (deg)": cos_deg,
    "tan (deg)": tan_deg,
    "sin (rad)": sin_rad,
    "cos (rad)": cos_rad,
    "tan (rad)": tan_rad,
    "atan (deg)": atan_deg,
    "atan (rad)": atan_rad,
    "atan2 (deg)": atan2_deg,
    "atan2 (rad)": atan2_rad,
    "atanh (deg)": atanh_deg,
    "atanh (rad)": atanh_rad,
    "log": log_base_e,
}


# ===================
# FUNKCJA OBLICZAJĄCA
# ===================
def oblicz():
    func_name = funkcja_var.get()
    func = funkcje[func_name]
    arg_text = argument_entry.get()

    try:
        # dzielenie argumentów
        args = [float(a.strip()) for a in arg_text.split(".")]

        if func_name.startswith("atan2"):
            wynik = func(args[0], args[1])
        else:
            wynik = func(args[0])

            wynik_label.config(text=f"Wynik: {wynik}")
    except Exception as e:
        wynik_label.config(text=f"Błąd: {e}")


# ======================
# GUI
# ======================
root = tk.Tk()
root.title("Konwerter funkcji trygonometrycznych")

# Wybór funkcji
tk.Label(root, text="Funkcja:").grid(row=0, column=0, sticky="w")
funkcja_var = tk.StringVar(value="sin (deg)")
funkcja_menu = ttk.Combobox(
    root, textvariable=funkcja_var, values=list(funkcje.keys()), width=20
)
funkcja_menu.grid(row=0, column=1)

# Wprowadzenie argumentu
tk.Label(root, text="Argument(y) (dla atan2: y,x):").grid(row=1, column=0, sticky="w")
argument_entry = tk.Entry(root)
argument_entry.grid(row=1, column=1)

# Przycisk oblicz
tk.Button(root, text="Oblicz", command=oblicz).grid(
    row=2, column=0, columnspan=2, pady=5
)

# Wyswietlenie wyniku
wynik_label = tk.Label(root, text="Wynik")
wynik_label.grid(row=3, column=0, columnspan=2)

root.mainloop()
