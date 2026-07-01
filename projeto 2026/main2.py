from tkinter import *
from tkinter import filedialog
import pygame
import os

janela = Tk()
janela.title('Reprodutor de música')
janela.geometry("500x300")

pygame.mixer.init()


songs = []
atual_song = ""
paused = False

songlist = Listbox(janela, bg="black", fg="white", width=100, height=15)
songlist.pack()

play_btn_image = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image = PhotoImage(file='next.png')
prev_btn_image = PhotoImage(file='previous.png')

control_frame = Frame(janela)
control_frame.pack()


def carregar_musica():
    global atual_song
    
    janela.directory = filedialog.askdirectory(parent=janela)

    if not janela.directory: 
        return

    for song in os.listdir(janela.directory):
        name, ext = os.path.splitext(song) 
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    songlist.select_set(0)
    atual_song = songs[songlist.curselection()[0]]

def play_music():
    global atual_song, paused

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
        songlist.select_clear(0, END)
        songlist.select_set(songs.index(atual_song) + 1)
        atual_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    global atual_song, paused
    try:
        songlist.select_clear(0, END)
        songlist.select_set(songs.index(atual_song) - 1)
        atual_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

barra_menu = Menu(janela)
janela.config(menu=barra_menu)

organizar_menu = Menu(barra_menu, tearoff=False)
organizar_menu.add_command(label='Selecione a pasta', command=carregar_musica)
barra_menu.add_cascade(label='Organizar', menu=organizar_menu)

janela.mainloop()