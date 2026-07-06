import tkinter as tk
from tkinter import filedialog
import pygame
import os

WIDTH = 360
HEIGHT = 600

# Inicialização da Janela com design SpotTI
janela = tk.Tk()
janela.title('SpotTI - Minhas Músicas')
janela.geometry(f"{WIDTH}x{HEIGHT}")
janela.configure(bg="#121212")
janela.resizable(False, False)

pygame.mixer.init()

songs = []
atual_song = ""
paused = False

# Título da Interface
tk.Label(
    janela, 
    text="Suas Músicas", 
    bg="#121212", 
    fg="white", 
    font=("Arial", 18, "bold")
).pack(pady=15)

# Lista de Músicas Customizada
songlist = tk.Listbox(
    janela, 
    bg="#1e1e1e", 
    fg="white", 
    selectbackground="#1db954", # Cor de destaque (estilo Spotify)
    selectforeground="white",
    bd=0,
    highlightthickness=0,
    font=("Arial", 11),
    width=35,
    height=15
)
songlist.pack(pady=10, padx=20, fill="both", expand=True)

# Botão para selecionar a pasta (substituindo a barra de menu por um botão limpo)
def carregar_musica():
    global atual_song
    janela.directory = filedialog.askdirectory(parent=janela)

    if not janela.directory: 
        return

    songs.clear()
    songlist.delete(0, tk.END)

    for song in os.listdir(janela.directory):
        name, ext = os.path.splitext(song) 
        if ext.lower() == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    if songs:
        songlist.select_set(0)
        atual_song = songs[0]

btn_carregar = tk.Button(
    janela,
    text="📁 Selecionar Pasta de Músicas",
    command=carregar_musica,
    bg="#1db954",
    fg="white",
    font=("Arial", 11, "bold"),
    bd=0,
    padx=15,
    pady=8,
    activebackground="#1aa34a",
    activeforeground="white"
)
btn_carregar.pack(pady=10)

# Controle de mídia
control_frame = tk.Frame(janela, bg="#121212")
control_frame.pack(pady=15)

def play_music():
    global atual_song, paused
    if not songs:
        return
        
    # Pega a música selecionada na lista pelo usuário em tempo real
    try:
        selecionada = songlist.curselection()[0]
        atual_song = songs[selecionada]
    except IndexError:
        pass

    if not paused:
        pygame.mixer.music.load(os.path.join(janela.directory, atual_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused 
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global atual_song, paused
    try:
        index_atual = songs.index(atual_song)
        proximo_index = (index_atual + 1) % len(songs)
        songlist.select_clear(0, tk.END)
        songlist.select_set(proximo_index)
        atual_song = songs[proximo_index]
        paused = False
        play_music()
    except:
        pass

def prev_music():
    global atual_song, paused
    try:
        index_atual = songs.index(atual_song)
        anterior_index = (index_atual - 1) % len(songs)
        songlist.select_clear(0, tk.END)
        songlist.select_set(anterior_index)
        atual_song = songs[anterior_index]
        paused = False
        play_music()
    except:
        pass

# Botões de mídia estilizados em formato texto/emoji modernos (dispensando imagens externas obrigatoriamente)
estilo_botoes = {
    "bg": "#121212", "fg": "white", "bd": 0, "font": ("Arial", 18),
    "activebackground": "#121212", "activeforeground": "#1db954"
}

prev_btn = tk.Button(control_frame, text="⏮", command=prev_music, **estilo_botoes)
play_btn = tk.Button(control_frame, text="▶", command=play_music, **estilo_botoes)
pause_btn = tk.Button(control_frame, text="⏸", command=pause_music, **estilo_botoes)
next_btn = tk.Button(control_frame, text="⏭", command=next_music, **estilo_botoes)

prev_btn.grid(row=0, column=0, padx=15)
play_btn.grid(row=0, column=1, padx=15)
pause_btn.grid(row=0, column=2, padx=15)
next_btn.grid(row=0, column=3, padx=15)

janela.mainloop()