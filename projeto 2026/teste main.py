import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk, ImageFilter

WIDTH = 360
HEIGHT = 600

class MusicPlayer:

    def __init__(self, root):
        self.root = root
        self.root.title("SpotTI")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        self.playing = False
        self.angle = 0

      
        bg = Image.open("home.jpg").resize((WIDTH, HEIGHT))
        bg = bg.filter(ImageFilter.GaussianBlur(radius=5))
        self.bg = ImageTk.PhotoImage(bg)

        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        self.canvas.create_rectangle(
            0,
            0,
            WIDTH,
            HEIGHT,
            fill="#000000",
            stipple="gray50",
            outline=""
        )

  
        self.original_cover = Image.open("home.jpg").resize((220, 220))
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

        self.write(
            "Sam e Caty",
            self.music_title,
            60,
            callback=lambda: self.write(
                "SpotTI",
                self.artist,
                90
            )
        )

        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#3D0505", 
            background="white"       
        )
        self.progress = ttk.Progressbar(
            root,
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
            root,
            text="▶",
            font=("Arial", 22),
            bg="#420d0d",
            fg="white",
            command=self.toggle_music
        )

        self.canvas.create_window(
            WIDTH // 2,
            530,
            window=self.play
        )



    def rotate(self):

        if not self.playing:
            return
        self.angle = (self.angle + 3) 
        img = self.original_cover.rotate(-self.angle)
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
        self.root.after(95, self.progress_bar)



    def toggle_music(self):

        self.playing = not self.playing

        if self.playing:
            self.play.config(text="⏸")
            self.rotate()
            self.progress_bar()
            self.sing()
        else:
            self.play.config(text="▶")

    def write(self, text, item, speed=80, callback=None):
        def typing(index=0):
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

        lyrics = [
            ("Véu e grinalda", 100),
            ("Lua de mel", 100),
            ("", 500),
            ("Chuva de arroz e tudo depois", 70),
            ("Dama de honra pega o buquê", 70),
            ("", 500),
            ("Ninguém mais feliz que eu e você...", 80),
        ]

        def next_line(index=0):
            if index >= len(lyrics):
                return
            texto, velocidade = lyrics[index]
            self.write(
                texto,
                self.lyric,
                velocidade,
                callback=lambda: self.root.after(
                    700,
                    lambda: next_line(index + 1)
                )
            )
        next_line()

root = tk.Tk()

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Custom.Horizontal.TProgressbar",
    troughcolor ="#BD5A5A",
    background="white"
)

MusicPlayer(root)

root.mainloop()

