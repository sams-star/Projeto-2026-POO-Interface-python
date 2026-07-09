import tkinter as tk
from PIL import Image, ImageTk

from sweetChildOMine import Play_SweetChildoMine
from wonderwall import Play_Wonderwall
from bringMeToLife import Play_BringMeToLife
from Mais_Ninquem import Play_MaisNinguem
from AiAiAmor import Play_AiAiAmor
from salvar_musicas2 import SalvarMusicas

WIDTH = 360
HEIGHT = 600

janela = None



def playlist(nome, img_path, comando):

    frame = tk.Frame(janela, bg="#121212")
    frame.pack(fill="x", padx=15, pady=6)

    img = Image.open(img_path).resize((45, 45))
    foto = ImageTk.PhotoImage(img)

    label = tk.Label(
        frame,
        image=foto,
        bg="#000000"
    )
    label.image = foto
    label.pack(side="left", padx=10)

    botao = tk.Button(
        frame,
        text=nome,
        command=comando,
        bg="#121212",
        fg="white",
        bd=0,
        font=("Arial", 13, "bold"),
        activebackground="#1e1e1e",
        activeforeground="white"
    )
    botao.pack(side="left")


def main():

    global janela

    janela = tk.Tk()

    janela.title("SpotTI")
    janela.geometry(f"{WIDTH}x{HEIGHT}")
    janela.configure(bg="#121212")

    tk.Label(
        janela,
        text="Sua Biblioteca",
        bg="#121212",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        janela,
        text="Playlists",
        bg="#121212",
        fg="#aaaaaa",
        font=("Arial", 11)
    ).pack(anchor="w", padx=20)

    playlist(
        "Sweet Child O' Mine",
        "bandaft.jpg",
        lambda: Play_SweetChildoMine(janela)
    )

    playlist("Evidências",
             "maisninquem.jpg",
             lambda: Play_MaisNinguem(janela)
             )
    
    playlist(" Ai, Amor",
             "Anavitória.jpg",
             lambda: Play_AiAiAmor(janela)
             )

    playlist(
    "Wonderwall",
    "Wonderwall.jpg",
    lambda: Play_Wonderwall(janela)
    )

    playlist(
        "Bring me to Life",
        "evanescence.jpg",
        lambda: Play_BringMeToLife(janela)
    )

    playlist(
        "Salve suas musicas",
        "musica.jpg",
        lambda: SalvarMusicas(janela)
    )
    

    janela.mainloop()


if __name__ == "__main__":
    main()