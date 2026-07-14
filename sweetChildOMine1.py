import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import pygame
import os

WIDTH = 360
HEIGHT = 600

class Play_SweetChildoMine:

    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.title("SpotTI")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#05042E",
            background="white"
        )

        
        self.playing = False
        self.paused = False
        self.singing = False 
        self.angle = 0
        self.lyric_index = 0 

        pygame.mixer.init()
        self.atual_song = "sweet child o' mine.mp3"

        def make_image_circular(image_path, size):
            img = Image.open(image_path).convert("RGBA")
            img = img.resize(size, Image.Resampling.LANCZOS)

            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((2, 2, size[0]-2, size[1]-2), fill=255)

            circular_img = Image.new("RGBA", size, (0, 0, 0, 0))
            circular_img.paste(img, (0, 0), mask)

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

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

      
        self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg)

       
        self.animate_bg()

       
        self.canvas.create_rectangle(
            0,
            0,
            WIDTH,
            HEIGHT,
            fill="#000000",
            stipple="gray50",
            outline=""
        )

       
        tamanho_foto = (220, 220)

        self.original_cover = make_image_circular(
            "bandaft.jpg",
            tamanho_foto
        )
        self.cover = ImageTk.PhotoImage(self.original_cover)

        self.cover_id = self.canvas.create_image(
            WIDTH // 2,
            190,
            image=self.cover
        )

        self.music_title = self.canvas.create_text(
            WIDTH // 2,
            340,
            text="",
            fill="white",
            font=("Arial", 16, "bold")
        )

        self.artist = self.canvas.create_text(
            WIDTH // 2,
            365,
            text="",
            fill="#bbbbbb",
            font=("Arial", 11)
        )

      
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#05042E",  
            background="white"       
        )
        self.progress = ttk.Progressbar(
            self.root,
            length=270,
            maximum=100,
            style="Custom.Horizontal.TProgressbar"
        )

        self.canvas.create_window(
            WIDTH // 2,
            410,
            window=self.progress
        )

    
        self.lyric = self.canvas.create_text(
            WIDTH // 2,
            470,
            text="",
            fill="white",
            font=("Arial", 14),
            width=300,
            justify="center"
        )

     
        self.play = tk.Button(
            self.root,
            text="▶",
            font=("Arial", 22),
            bg="#120d42",
            fg="white",
            command=self.toggle_music
        )

        self.canvas.create_window(
            WIDTH // 2,
            530,
            window=self.play
        )

        self.write(
            "Sweet Child O' Mine",
            self.music_title,
            60,
            callback=lambda: self.write(
                "Guns N' Roses",
                self.artist,
                90
            )
        )

  

 

    def animate_bg(self):
        self.bg = self.frames[self.current_frame]
        self.canvas.itemconfig(self.bg_image_id, image=self.bg)
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(90, self.animate_bg)

  
    def rotate(self):
        if not self.playing:
            return
        self.angle = (self.angle + 3) % 360
        img = self.original_cover.rotate(-self.angle, resample=Image.BICUBIC)
        self.cover = ImageTk.PhotoImage(img)

        self.canvas.itemconfig(
            self.cover_id,
            image=self.cover
        )
        self.root.after(75, self.rotate)

    def progress_bar(self):
        if not self.playing:
            return
        value = self.progress["value"] + 0.1

        if value > 100:
            value = 0
        self.progress["value"] = value
        self.root.after(450, self.progress_bar)

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


            self.rotate()
            self.progress_bar()
            if not self.singing:  
                self.sing()
            
        else:
            self.play.config(text="▶")
            pygame.mixer.music.pause()
            self.paused = True


    def write(self, text, item, speed=80, callback=None):
        def typing(index=0):
     
            if not self.playing and item == self.lyric:
                self.singing = False
                return
            if index <= len(text):
                self.canvas.itemconfig(
                    item,
                    text=text[:index]
                )
                self.root.after(
                    speed,
                    lambda: typing(index + 1)
                )
            elif callback:
                callback()
        typing()

    def sing(self):
        self.singing = True
        lyrics = [
            ("", 45150),
            ("She's got a smile that it seems to me", 90),
            ("Reminds me of childhood memories", 95),
            ("Where everything was as fresh as the bright blue sky", 90),
            ("Now and then when I see her face", 90),
            ("She takes me away to that special place", 95),
            ("And if I stared too long, I'd probably break down and cry", 90),
            ("", 150),

            ("Woah, oh, oh, sweet child of mine", 140),
            ("Woah, oh, oh, oh, sweet love of mine", 160),
            ("", 16550),

            ("She's got eyes of the bluest skies", 90),
            ("As if they thought of rain", 100),
            ("I'd hate to look into those eyes and see an ounce of pain", 150),
            ("Her hair reminds me of a warm, safe place", 100),
            ("Where, as a child, I'd hide", 90),
            ("And pray for the thunder and the rain to quietly pass me by", 100),
            ("", 100),

            ("Woah, oh, oh, sweet child of mine", 140),
            ("Woah-woah, oh, oh, oh, sweet love of mine", 150),
            ("", 15000),

            ("not tempo decompletar a letra, dsclp :(", 500),
            ("", 18000),
            ("melhor solo da vida, ta?", 100),
            ("AMOOOOOOOOOOOO", 100),

        
    ]
    

        def next_line():
           
            if not self.playing:
                self.singing = False
                return
                
            if self.lyric_index >= len(lyrics):
                self.lyric_index = 0 
                self.singing = False
                return

            texto, velocidade = lyrics[self.lyric_index]
            self.lyric_index += 1

            self.write(
                texto,
                self.lyric,
                velocidade,
                callback=lambda: self.root.after(
                    700, lambda: next_line()
                )
            )
        
        next_line()

