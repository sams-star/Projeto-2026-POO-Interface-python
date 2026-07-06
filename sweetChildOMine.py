import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import pygame
import os

WIDTH = 360
HEIGHT = 600

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("SpotTI")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

       
        pygame.mixer.init()

        self.atual_song = "sweet-child-o-mine.mp3"
        self.playing = False
        self.paused = False
        self.angle = 0

        
        def make_image_circular(image_path, size):
            """Abre a imagem, redimensiona, e aplica uma máscara para torná-la circular com anti-aliasing."""
            img = Image.open(image_path).convert("RGBA")
            img = img.resize(size, Image.Resampling.LANCZOS) 

            
            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            
            
            draw.ellipse((2, 2, size[0]-2, size[1]-2), fill=255)

            
            circular_img = Image.new("RGBA", size, (0, 0, 0, 0)) 
            circular_img.paste(img, (0, 0), mask=mask)
            return circular_img

        
        self.gif = Image.open("gunsroses.gif")
        self.frames = []
        try:
            while True:
                frame = self.gif.copy().convert("RGBA").resize((WIDTH, HEIGHT))
                self.frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(len(self.frames)) 
        except EOFError:
            pass 

        self.current_frame = 0
        self.bg = self.frames[self.current_frame]

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        
        self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg)

        
        self.animate_bg()

       
        self.canvas.create_rectangle(
            0, 0, WIDTH, HEIGHT,
            fill="#030303",
            stipple="gray50",
            outline=""
        )

        
        tamanho_foto = (220, 220)
        
       
        self.original_cover = make_image_circular("bandaft.jpg", tamanho_foto)
        self.cover = ImageTk.PhotoImage(self.original_cover)

        
        self.cover_id = self.canvas.create_image(
            WIDTH // 2, 190,
            image=self.cover
        )

        
        nome_exibicao = os.path.splitext(self.atual_song)[0].replace("_", " ").title()

        self.music_title = self.canvas.create_text(
            WIDTH // 2, 340,
            text=nome_exibicao,
            fill="white",
            font=("Arial", 14, "bold"),
            width=300,
            justify="center"
        )

        self.artist = self.canvas.create_text(
            WIDTH // 2, 375,
            text="SpotTI Player",
            fill="#bbbbbb",
            font=("Arial", 11)
        )

        
        self.progress = ttk.Progressbar(
            root,
            length=270,
            maximum=100,
            style="Custom.Horizontal.TProgressbar"
        )

        self.canvas.create_window(
            WIDTH // 2, 410,
            window=self.progress
        )

       
        self.lyric = self.canvas.create_text(
            WIDTH // 2, 470,
            text="",
            fill="white",
            font=("Arial", 14),
            width=300,
            justify="center"
        )

        # Botão Play/Pause
        self.play = tk.Button(
            root,
            text="▶",
            font=("Arial", 22),
            bg="#120d42",
            fg="white",
            bd=0, # Remove borda do botão para ficar mais limpo
            highlightthickness=0,
            command=self.toggle_music
        )

        self.canvas.create_window(
            WIDTH // 2, 530,
            window=self.play
        )

    
    def toggle_music(self):
        if not os.path.exists(self.atual_song):
            self.canvas.itemconfig(self.music_title, text="Arquivo não encontrado!")
            return

        self.playing = not self.playing

        if self.playing:
            self.play.config(text="⏸")
            
            if not self.paused:
                pygame.mixer.music.load(self.atual_song)
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
                self.paused = False

            # Dispara as animações visuais
            self.rotate()
            self.progress_bar()
            self.sing()
        else:
            self.play.config(text="▶")
            pygame.mixer.music.pause()
            self.paused = True

    # Animação do GIF de fundo (sem mudanças)
    def animate_bg(self):
        self.bg = self.frames[self.current_frame]
        self.canvas.itemconfig(self.bg_image_id, image=self.bg)
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(90, self.animate_bg)

    # Animação de rotação da Capa (sem mudanças no algoritmo, mas agora gira a imagem redonda)
    def rotate(self): 
        if not self.playing or self.paused:
            return
        self.angle = (self.angle + 3) % 360
        img = self.original_cover.rotate(-self.angle, resample=Image.BICUBIC) # Gira com suavização
        self.cover = ImageTk.PhotoImage(img)

        self.canvas.itemconfig(
            self.cover_id,
            image=self.cover
        )
        self.root.after(75, self.rotate)

    # Simulação da Barra de Progresso (sem mudanças)
    def progress_bar(self):
        if not self.playing or self.paused:
            return
        value = self.progress["value"] + 0.1

        if value > 100:
            value = 0
        self.progress["value"] = value
        self.root.after(95, self.progress_bar)




root = tk.Tk()

style = ttk.Style(root)
style.theme_use("clam")
style.configure(
    "Custom.Horizontal.TProgressbar",
    troughcolor="#05042E",
    background="white" 
)

app = MusicPlayer(root)
root.mainloop()