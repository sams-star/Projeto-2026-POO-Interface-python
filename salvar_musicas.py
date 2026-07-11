import tkinter as tk
from tkinter import filedialog
import pygame
import os
import json

WIDTH = 360
HEIGHT = 600


class SalvarMusicass:

    def __init__(self, master):

        self.root = tk.Toplevel(master)
        self.root.title("SpotTI - Minhas Músicas")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        pygame.mixer.init()

        self.songs = []
        self.atual_song = ""
        self.paused = False
        self.directory = ""

        tk.Label(
            self.root,
            text="Suas Músicas",
            bg="#121212",
            fg="white",
            font=("Arial",18,"bold")
        ).pack(pady=15)

        self.songlist = tk.Listbox(
            self.root,
            bg="#1e1e1e",
            fg="white",
            selectbackground="#1db954",
            selectforeground="white",
            bd=0,
            highlightthickness=0,
            font=("Arial",11)
        )

        self.songlist.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        tk.Button(
            self.root,
            text="📁 Selecionar Pasta",
            command=self.carregar_musicas,
            bg="#1db954",
            fg="white",
            bd=0
        ).pack(pady=10)

        frame = tk.Frame(self.root,bg="#121212")
        frame.pack(pady=15)

        tk.Button(frame,text="⏮",command=self.prev,width=3).grid(row=0,column=0,padx=5)
        tk.Button(frame,text="▶",command=self.play,width=3).grid(row=0,column=1,padx=5)
        tk.Button(frame,text="⏸",command=self.pause,width=3).grid(row=0,column=2,padx=5)
        tk.Button(frame,text="⏭",command=self.next,width=3).grid(row=0,column=3,padx=5)


    def carregar_musicas(self):

        pasta = filedialog.askdirectory(parent=self.root)

        if not pasta:
            return

        self.directory = pasta

        self.songs.clear()
        self.songlist.delete(0,tk.END)

        for arquivo in os.listdir(pasta):

            if arquivo.lower().endswith(".mp3"):

                self.songs.append(arquivo)
                self.songlist.insert(tk.END,arquivo)

        if self.songs:
            self.songlist.select_set(0)
            self.atual_song = self.songs[0]

        self.salvar_json()


    def salvar_json(self):

        dados = {
            "musicas": [
                os.path.join(self.directory, musica)
                for musica in self.songs
            ]
        }

        with open("musicas.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)


    def play(self):

        if not self.songs:
            return

        try:
            indice = self.songlist.curselection()[0]
            self.atual_song = self.songs[indice]
        except:
            pass

        caminho = os.path.join(
            self.directory,
            self.atual_song
        )

        if not self.paused:

            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play()

        else:

            pygame.mixer.music.unpause()
            self.paused = False



    def pause(self):

        pygame.mixer.music.pause()
        self.paused = True



    def next(self):

        if not self.songs:
            return

        indice = (self.songs.index(self.atual_song)+1)%len(self.songs)

        self.songlist.select_clear(0,tk.END)
        self.songlist.select_set(indice)

        self.atual_song=self.songs[indice]

        self.paused=False

        self.play()



    def prev(self):

        if not self.songs:
            return

        indice=(self.songs.index(self.atual_song)-1)%len(self.songs)

        self.songlist.select_clear(0,tk.END)
        self.songlist.select_set(indice)

        self.atual_song=self.songs[indice]

        self.paused=False

        self.play()