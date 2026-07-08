import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

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
        self.angle = 0

        def make_image_circular(image_path, size):
            img = Image.open(image_path).convert("RGBA")
            img = img.resize(size, Image.Resampling.LANCZOS)

            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((2, 2, size[0]-2, size[1]-2), fill=255)

            circular_img = Image.new("RGBA", size, (0, 0, 0, 0))
            circular_img.paste(img, (0, 0), mask)

            return circular_img    

        #gif
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

        # Coloca o frame
        self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg)

        # loop - gif
        self.animate_bg()

        # filtro preto
        self.canvas.create_rectangle(
            0,
            0,
            WIDTH,
            HEIGHT,
            fill="#030303",
            stipple="gray50",
            outline=""
        )

        # Capa
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

        # Nome da musiguinha
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
            "Mais ninquem",
            self.music_title,
            60,
            callback=lambda: self.write(
                "SpotTI",
                self.artist,
                90
            )
        )

        # Barra de progresso
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#05042E",   # fundo
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

        # Letras
        self.lyric = self.canvas.create_text(
            WIDTH // 2,
            470,
            text="",
            fill="white",
            font=("Arial", 14),
            width=300,
            justify="center"
        )

        # Play
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

    #A ANIMAÇÃO DO GIF 
    def animate_bg(self):
        self.bg = self.frames[self.current_frame]
        self.canvas.itemconfig(self.bg_image_id, image=self.bg)
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        # 60 milisg por frame- ELE NEGOSA O TEMPO PRA DEIXAR MAIS RAPIDO OU DIVAGAR
        self.root.after(90, self.animate_bg)

     #animaçãozinha DA FOTO
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
