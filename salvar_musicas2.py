import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import json

WIDTH = 360
HEIGHT = 600

class SalvarMusicas:
        def __init__(self, master, usuario_logado):
            self.usuario_logado = usuario_logado
            self.nome_arquivo_json = "usuarios.json"
            self.root = tk.Toplevel(master)
            self.root.title(f"SpotTI - Músicas de {self.usuario_logado}")
            self.root.geometry(f"{WIDTH}x{HEIGHT}")
            self.root.configure(bg="#121212")
            self.root.resizable(False, False)


            pygame.mixer.init()
                
            self.songs = []
            self.atual_song = ""
            self.paused = False
            
            self.root.grab_set()

            tk.Label(
                self.root, 
                text=f"Músicas de {self.usuario_logado}", 
                bg="#121212", 
                fg="white", 
                font=("Arial", 16, "bold")
            ).pack(pady=15)

        
            self.songlist = tk.Listbox(
                self.root, 
                bg="#1e1e1e", 
                fg="white", 
                selectbackground="#541B1B", 
                selectforeground="white", 
                bd=0, 
                highlightthickness=0, 
                font=("Arial", 11)
            )
            self.songlist.pack(
                pady=10, 
                padx=20,
                fill="both",
                expand=True)

        
            self.btn_carregar = tk.Button(
                self.root, 
                text="Selecionar Pasta", 
                command=self.carregar_musica,
                bg="#740707", 
                fg="white",  
                bd=0,
                activebackground="#4F0606",
                activeforeground="white"
            )
            self.btn_carregar.pack(fill="x", padx=20, pady=15, ipady=8)


            frame = tk.Frame(self.root,bg="#121212")
            frame.pack(pady=15)

            tk.Button(frame,text="⏮",command=self.prev,width=3).grid(row=0,column=0,padx=5)
            tk.Button(frame,text="▶",command=self.play,width=3).grid(row=0,column=1,padx=5)
            tk.Button(frame,text="⏸",command=self.pause,width=3).grid(row=0,column=2,padx=5)
            tk.Button(frame,text="⏭",command=self.next,width=3).grid(row=0,column=3,padx=5)

            self.carregar_historico_json()

        

        def carregar_historico_json(self):
            if os.path.exists(self.nome_arquivo_json):
                try:
                    with open(self.nome_arquivo_json, "r", encoding="utf-8") as arquivo:
                        dados = json.load(arquivo)
                        if self.usuario_logado in dados:
                            self.songs = dados[self.usuario_logado].get("musicas", [])
                            for song in self.songs:
                                self.songlist.insert(tk.END, os.path.basename(song))

                            if self.songs:
                                self.songlist.select_set(0)
                                self.atual_song = self.songs[0]
                except Exception as e:
                    print("Erro ao ler histórico do JSON:", e)

        def carregar_musica(self):
            diretorio = filedialog.askdirectory(parent=self.root)

            if not diretorio: 
                return
            

            novas_musicas = []

            for item in os.listdir(diretorio):
                caminho = os.path.join(diretorio, item)
                name, ext = os.path.splitext(item)

                if ext.lower() == ".mp3":
                    if caminho not in self.songs:
                        self.songs.append(caminho)
                        novas_musicas.append(caminho)

            for song in novas_musicas:
                self.songlist.insert(tk.END, os.path.basename(song))

            if os.path.exists(self.nome_arquivo_json):
                try:
                    with open(self.nome_arquivo_json, "r", encoding="utf-8") as arquivo:
                        dados_usuarios = json.load(arquivo)
                    
                    if self.usuario_logado in dados_usuarios:
                        dados_usuarios[self.usuario_logado]["musicas"] = self.songs
                        
                        with open(self.nome_arquivo_json, "w", encoding="utf-8") as arquivo:
                            json.dump(dados_usuarios, arquivo, indent=4, ensure_ascii=False)
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível salvar no JSON: {e}", parent=self.root)

            if self.songs:
                self.songlist.select_set(0)
                self.atual_song = self.songs[0]

           


        def play(self):
            if not self.songs:
                return

            try:
                indice = self.songlist.curselection()[0]
                self.atual_song = self.songs[indice]
            except:
                pass

            if not self.paused:
                pygame.mixer.music.load(self.atual_song)
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