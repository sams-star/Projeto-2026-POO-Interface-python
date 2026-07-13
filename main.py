import tkinter as tk
from PIL import Image, ImageTk, ImageDraw  
import sys

from sweetChildOMine import Play_SweetChildoMine
from wonderwall import Play_Wonderwall
from bringMeToLife import Play_BringMeToLife
from Mais_Ninquem import Play_MaisNinguem
from AiAiAmor import Play_AiAiAmor
from salvar_musicas2 import SalvarMusicas

WIDTH = 360
HEIGHT = 600

janela = None

USUARIO_LOGADO = sys.argv if len(sys.argv) > 1 else sys.exit("Erro: Nenhum usuário foi informado.")

def playlist(nome, img_path, command):

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
        command=command,
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


    # --- CÓDIGO DA LOGO CIRCULAR (SEU BLOCO ATUALIZADO) ---
    tamanho_logo = (52, 52) 
    img_logo = Image.open("logo.jpg").convert("RGBA").resize(tamanho_logo, Image.Resampling.LANCZOS)
    
    mascara = Image.new("L", tamanho_logo, 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((0, 0) + tamanho_logo, fill=255)
    
    img_circular = Image.new("RGBA", tamanho_logo, (0, 0, 0, 0))
    img_circular.paste(img_logo, (0, 0), mask=mascara)
    
    foto_logo = ImageTk.PhotoImage(img_circular)

    frame_cabecalho = tk.Frame(janela, bg="#121212")
    frame_cabecalho.pack(fill="x", padx=20, pady=(20, 10))

   

    def abrir_perfil():
        import subprocess
        import os
    
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_perfil = os.path.join(diretorio_atual, "perfil.py")

    
        if isinstance(USUARIO_LOGADO, list) and len(USUARIO_LOGADO) > 1:
            usuario_envio = USUARIO_LOGADO[1]
        else:
            usuario_envio = str(USUARIO_LOGADO)

        try:
        
         subprocess.Popen([sys.executable, caminho_perfil, usuario_envio])
        except Exception as erro:
            print(f"Erro ao tentar abrir o arquivo perfil.py: {erro}")

 

    botao_logo = tk.Button(
        frame_cabecalho, 
        image=foto_logo, 
        bg="#121212",
        activebackground="#121212", 
        bd=0,                       
        command=abrir_perfil,       
        cursor="hand2"              # Mostra a mãozinha de clique
    )
    botao_logo.image = foto_logo
    botao_logo.pack(side="left", padx=(0, 12))

   
    label_texto_biblioteca = tk.Label(
        frame_cabecalho,
        text="Sua Biblioteca",
        bg="#121212",
        fg="white",
        font=("Arial", 18, "bold")
    )
    label_texto_biblioteca.pack(side="left")
   
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
        lambda: SalvarMusicas(janela, USUARIO_LOGADO)
    )

    janela.mainloop()


if __name__ == "__main__":
    main()
