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

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
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
        self.original_cover = Image.open("maisninquem.gif").resize((220, 220))
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
            "Mais Ninquém",
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
            troughcolor="#2E0404",   
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
            bg="#550f0f",
            fg="white",
            command=self.toggle_music
        )

        self.canvas.create_window(
            WIDTH // 2,
            530,
            window=self.play
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
        img = self.original_cover.rotate(-self.angle)
        self.cover = ImageTk.PhotoImage(img)

        self.canvas.itemconfig(
            self.cover_id,
            image=self.cover
        )
        self.root.after(75, self.rotate)


    def rotate(self): 
        if not self.playing or self.paused:
            return
        self.angle = (self.angle + 3) % 360
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



root = tk.Tk()

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Custom.Horizontal.TProgressbar",
    troughcolor ="#555555",
    background="white"
)

MusicPlayer(root)
root.mainloop()
