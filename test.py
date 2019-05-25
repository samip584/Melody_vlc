import os
import time
from tkinter.filedialog import askdirectory

from eq import equalizer_window
from mutagen.mp3 import MP3
import threading 

import vlc
from tkinter import *
import tkinter.messagebox
import json

listofsongs = []
index = 0
count = 0
volume = 0.8
muted = False
song_changed = False
shuffled = False
repeat = False
paused = False


root = Tk()
root.minsize(800,500)
#root.iconbitmap(r'logo.ico')


def about_us():
    tkinter.messagebox.showinfo('About Us', 'We are a group of friends making a music player')

def directorychooser():
    global count
    global directory
    global player
    directory = askdirectory()
    os.chdir(directory)
 
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            listofsongs.append(files)
            count += 1
    instance = vlc.Instance()
    music_player = instance.media_list_player_new()
    media_list= instance.media_list_new()
    for song in listofsongs:
        media_list.add_media(instance.media_new(song))
    #playlist = instance.media_list_new(listofsongs)
    music_player.set_media_list(media_list)
    song = music_player.get_media_player()
    '''for i in range(1,18):
                    print(i,vlc.libvlc_audio_equalizer_get_preset_name(i))'''
    '''
    rock = vlc.libvlc_audio_equalizer_new_from_preset(7)
    song.set_equalizer(rock)
    print(vlc.libvlc_audio_equalizer_get_amp_at_index(rock,1))
    music_player.play()'''
    hiphop = vlc.libvlc_audio_equalizer_new()
    song.set_equalizer(hiphop)
    music_player.play()

drop_menu = Menu(root)
root.config(menu = drop_menu)
directorychooser()
file_menu = Menu(drop_menu, tearoff = 0)
drop_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "Open", command = directorychooser)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command = root.quit)
root.mainloop()