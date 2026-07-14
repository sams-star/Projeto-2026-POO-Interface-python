import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import pygame
import os

WIDTH = 360
HEIGHT = 600

class Play_MaisNinguem:

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
        self.atual_song = "evidencias.mp3"

        def make_image_circular(image_path, size):
            img = Image.open(image_path).convert("RGBA")
            img = img.resize(size, Image.Resampling.LANCZOS)

            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((2, 2, size[0]-2, size[1]-2), fill=255)

            circular_img = Image.new("RGBA", size, (0, 0, 0, 0))
            circular_img.paste(img, (0, 0), mask)

            return circular_img    

 
        self.gif = Image.open("maisninquem.gif")
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
            "maisninquem.jpg",
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
            "Evidências",
            self.music_title,
            60,
            callback=lambda: self.write(
                "Chitãozinho & Xororó",
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
        self.root.after(300, self.progress_bar)

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
            ("", 20150), 
            ("Quando eu digo que deixei de te amar", 140),
            ("É porque eu te amo", 120),
            ("Quando eu digo que não quero mais você", 150),
            ("É porque eu te quero", 150),
            ("Eu tenho medo de te dar meu coração", 130),
            ("E confessar que eu estou em tuas mãos", 130),
            ("Mas não posso imaginar", 100),
            ("O que vai ser de mim", 90),
            ("Se eu te perder um dia", 150),
            ("", 100), 
            ("Eu me afasto e me defendo de você", 130),
            ("Mas depois me entrego", 130),
            ("Faço tipo, falo coisas que eu não sou", 130),
            ("Mas depois eu nego", 100),
            ("Mas a verdade", 100),
            ("É que eu sou louco por você", 140),
            ("E tenho medo de pensar em te perder", 110),
            ("Eu preciso aceitar que não dá mais", 100),
            ("Pra separar as nossas vidas", 100),
            ("", 120),
            ("E nessa loucura de dizer que não te quero", 100),
            ("Vou negando as aparências", 90),
            ("Disfarçando as evidências", 75),
            ("Mas pra que viver fingindo", 80),
            ("Se eu não posso enganar meu coração?", 80),
            ("Eu sei que te amo!", 90),
            ("", 90), 
            ("Chega de mentiras", 80),
            ("De negar o meu desejo", 70),
            ("Eu te quero mais que tudo", 70),
            ("Eu preciso do seu beijo", 75),
            ("Eu entrego a minha vida", 75),
            ("Pra você fazer o que quiser de mim", 75),
            ("Só quero ouvir você dizer que sim!", 70),
            ("", 900), 
            ("Diz que é verdade, que tem saudade", 90),
            ("Que ainda você pensa muito em mim", 80),
            ("Diz que é verdade, que tem saudade", 70),
            ("Que ainda você quer viver pra mim", 70),
            ("", 5000), 
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

