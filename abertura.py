import tkinter as tk
import subprocess
from PIL import Image, ImageTk

WIDTH = 360
HEIGHT = 600


def abrir_player(nome_arquivo):
    subprocess.Popen(["python", nome_arquivo])


root = tk.Tk()
root.title("SpotTI")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="#121212")


tk.Label(
    root,
    text="Sua Biblioteca",
    bg="#121212",
    fg="white",
    font=("Arial", 18, "bold")
).pack(pady=15)


tk.Label(
    root,
    text="Playlists",
    bg="#121212",
    fg="#aaaaaa",
    font=("Arial", 11)
).pack(anchor="w", padx=20)


# para saber o que cada playlist abre
def playlist(nome, img_path, arquivo_py):
    frame = tk.Frame(root, bg="#121212")
    frame.pack(fill="x", pady=6, padx=15)

    img = Image.open(img_path).resize((45, 45))
    foto = ImageTk.PhotoImage(img)

    label_img = tk.Label(frame, image=foto, bg="#121212")
    label_img.image = foto
    label_img.pack(side="left", padx=10)

    btn = tk.Button(
        frame,
        text=nome,
        command=lambda: abrir_player(arquivo_py),
        bg="#121212",
        fg="white",
        bd=0,
        font=("Arial", 13, "bold"),
        activebackground="#1e1e1e",
        activeforeground="white"
    )
    btn.pack(side="left", anchor="w")



playlist("🎵 Triste - Azul", "gatito.jpg", "azul.py")
playlist("🎵 HELP", "home.jpg", "teste main.py")
playlist("AAAAAAAA", "home.jpg", "teste main.py")
playlist("AAAAAAAA", "home.jpg", "teste main.py")
playlist("Sam e Caty", "home.jpg", "teste main.py")


root.mainloop()
