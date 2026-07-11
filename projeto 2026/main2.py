import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import json
# Se você ainda tiver o arquivo separado, pode importar, mas a lógica mudou:
# from salve_suas_musicas import SalvarMusicas 

# 1. PEGA O USUÁRIO LOGADO (Fecha se não estiver logado)
USUARIO_LOGADO = sys.argv[1] if len(sys.argv) > 1 else sys.exit()

WIDTH = 360
HEIGHT = 600

janela = tk.Tk()
janela.title(f"SpotTI - {USUARIO_LOGADO}")
janela.geometry(f"{WIDTH}x{HEIGHT}")
janela.configure(bg="#121212")

# --- FUNÇÕES DE AUDIO ---
def Play_Wonderwall(root):
    print("Tocando Wonderwall...")

def Play_BringMeToLife(root):
    print("Tocando Bring me to Life...")

def Play_Musica_Customizada(root, nome_musica):
    print(f"Tocando a música do usuário: {nome_musica}")
    # Aqui você coloca o código do pygame.mixer para tocar o arquivo mp3 específico

def Abrir_Gerenciador_Pastas(root, usuario):
    print("Abrindo tela para selecionar novas pastas...")
    # Aqui você ainda pode abrir a classe antiga para o usuário adicionar mais músicas


# --- SUA FUNÇÃO PLAYLIST PADRÃO ---
def playlist(nome, img_path, comando_lambda):
    frame = tk.Frame(janela, bg="#121212")
    frame.pack(fill="x", pady=6, padx=15)

    # Proteção simples caso a imagem não exista
    try:
        img = Image.open(img_path).resize((45, 45))
        foto = ImageTk.PhotoImage(img)
    except:
        # Imagem padrão de fallback caso dê erro
        img = Image.new('RGB', (45, 45), color='#1db954')
        foto = ImageTk.PhotoImage(img)

    label_img = tk.Label(frame, image=foto, bg="#121212")
    label_img.image = foto
    label_img.pack(side="left", padx=10)

    btn = tk.Button(
        frame,
        text=nome,
        command=comando_lambda,
        bg="#121212",
        fg="white",
        bd=0,
        font=("Arial", 13, "bold"),
        activebackground="#1e1e1e",
        activeforeground="white"
    )
    btn.pack(side="left", anchor="w")

tk.Label(janela, text="Sua Biblioteca", bg="#121212", fg="white", font=("Arial", 18, "bold")).pack(pady=15)
tk.Label(janela, text="Playlists Globais", bg="#121212", fg="#aaaaaa", font=("Arial", 11)).pack(anchor="w", padx=20)

# 2. PLAYLISTS QUE TODO MUNDO VÊ
playlist("Wonderwall", "Wonderwall.jpg", lambda: Play_Wonderwall(janela))
playlist("Bring me to Life", "evanescence.jpg", lambda: Play_BringMeToLife(janela))

# Botão fixo apenas para abrir o gerenciador/importador de arquivos se ele quiser adicionar mais
playlist("➕ Importar mais músicas", "musica.jpg", lambda: Abrir_Gerenciador_Pastas(janela, USUARIO_LOGADO))

# --- 3. O SEGREDO: RENDERIZAÇÃO DINÂMICA E EXCLUSIVA ---
tk.Label(janela, text="Suas Músicas Salvas", bg="#121212", fg="#1db954", font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(15, 5))

nome_arquivo_json = "usuarios.json"
if os.path.exists(nome_arquivo_json):
    try:
        with open(nome_arquivo_json, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            
            # Procura o usuário atual dentro do JSON
            if USUARIO_LOGADO in dados:
                musicas_do_usuario = dados[USUARIO_LOGADO].get("musicas", [])
                
                # Para cada música da lista dele, cria um componente 'playlist' único na tela!
                for nome_musica in musicas_do_usuario:
                    # Usamos uma subfunção ou passamos direto o argumento para prender o valor correto da string no laço
                    playlist(
                        nome_musica, 
                        "musica.jpg", 
                        lambda m=nome_musica: Play_Musica_Customizada(janela, m)
                    )
    except Exception as e:
        print("Erro ao carregar músicas exclusivas:", e)

janela.mainloop()