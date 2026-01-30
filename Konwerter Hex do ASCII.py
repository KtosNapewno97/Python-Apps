# pylint: disable=import-error
import tkinter as tk
from tkinter import messagebox

# Tworzymy okno
root = tk.Tk()
root.title("ASCII ↔ hex konwerter")
root.geometry("400x200")

ascii_entry = tk.Entry(root, width=50)
ascii_entry.pack(pady=(20, 10))

hex_entry = tk.Entry(root, width=50)
hex_entry.pack(pady=(20, 10))

# Użycie konwersji
def ascii_to_hex():
    text = ascii_entry.get()
    if not text:
        messagebox.showwarning("Błąd", "Wpisz tekst ASCII!")
        return
    hex_text = text.encode("utf-8").hex()
    hex_entry.delete(0, tk.END)
    hex_entry.insert(0, hex_text)

def hex_to_ascii():
    text = hex_entry.get()
    if not text:
        messagebox.showwarning("Błąd", "Wpisz tekst w hex!")
        return
    try:
        ascii_text = bytes.fromhex(text).decode("utf-8")
    except ValueError:
        messagebox.showerror("Błąd", "Nieprawidłowy format hex!")
        return
    ascii_entry.delete(0, tk.END)
    ascii_entry.insert(0, ascii_text)

# Przyciski
tk.Button(root, text="ASCII → Hex", command=ascii_to_hex).pack(side=tk.LEFT, padx=20, pady=20)
tk.Button(root, text="Hex → ASCII", command=hex_to_ascii).pack(side=tk.RIGHT, padx=20, pady=20)

# Uruchomienie pętli GUI
root.mainloop()