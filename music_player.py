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
volume = 80
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
    global music_player
    directory = askdirectory()
    os.chdir(directory)
 
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            listofsongs.append(files)
            count += 1
    update_list()

    instance = vlc.Instance()
    music_player = instance.media_list_player_new()
    media_list= instance.media_list_new()
    for song in listofsongs:
        media_list.add_media(instance.media_new(song))
    #playlist = instance.media_list_new(listofsongs)
    music_player.set_media_list(media_list)


def donothing():
    print("Nothing is to be done")

    
def update_list():
    listofsongs.reverse()
    for items in listofsongs:
        listbox.insert(0,items)     
    listofsongs.reverse()

def update_display():
    global index
    displaybox.delete(0, END) 
    displaybox.insert(0, listofsongs[index])

def updatelabel():
    global index
    global songname
    root.title("Music Player: "+ listofsongs[index])

def update_details():
	audio = MP3(listofsongs[index])
	total_length = audio.info.length
	mins = int(total_length / 60)
	sec = round(total_length % 60)
	thread_1 = threading.Thread(target = start_count, args = (total_length,))   
	thread_1.start()

def start_count(total_length):
    global paused
    global music_player
    global song
    current_time = 0
    total_min = int(total_length / 60)
    total_sec = round(total_length % 60)
    total_time = (total_min * 60) + total_sec
    visual_detail["to"] = total_time
    pointer = index
    while current_time < total_time and music_player.is_playing():
        if pointer != index:
            return
        if paused:
            continue
        else:
            time.sleep(1)        
            current_time = int(song.get_time()/1000)
            current_mins = int(current_time / 60)
            current_sec = round(current_time % 60)
            time_detail["text"] = "{:02d} : {:02d} / {:02d} : {:02d}".format(current_mins, current_sec, total_min, total_sec)
            visual_detail.set(current_time)
    if current_time == total_time:
        if not (repeat):
            nextsong("<Button-1>")
        else:
            stopsong("<Button-1>")
            playsong("<Button-2>")

def prevsong(event):
    global paused
    global shuffled
    global repeated
    global index
    global music_player
    try:
        if shuffled:

            if index == 0:
                index = (count - 7)
            else:
                index = (index - 7) % count
        else:
            if index == 0:
                index = (count - 1)
            else:
                index = index - 1
        music_player.stop()
        music_player.play_item_at_index(index)
        statusbar['text'] = "Playing: " + listofsongs[index]
        paused = False
        update_details()
        update_display()


    except:
        tkinter.messagebox.showerror('Error', 'Select a directory')

def playsong(event):
    global index
    global paused
    global muted
    global music_player
    global song
    try:

        selected_song = listbox.curselection()
        if selected_song:
            index = int(selected_song[0])
            listbox.selection_clear(0, END)

        music_player.play_item_at_index(index)
        song =  music_player.get_media_player()
        song.audio_set_volume(volume)
        statusbar['text'] = "Playing: " + listofsongs[index]
        paused = False
        muted = False
        update_details()
        update_display()
    except:
        tkinter.messagebox.showerror('Error', 'Select a directory')

def pausesong(event):
    global index
    global paused
    global music_player
    if paused:
        music_player.pause()
        pausebutton.configure(image=pause_button)
        statusbar['text'] = "Playing: " + listofsongs[index]
        paused = False
    else:
        music_player.pause()
        pausebutton.configure(image=play_button)
        statusbar['text'] = "Paused: " + listofsongs[index]
        paused = True

def nextsong(event):
    # global paused

    global index
    global shuffled
    global music_player


    try:
        if shuffled:
            index = (index + 7) % count
        else:
            index = (index + 1) % count
        music_player.stop()
        music_player.play_item_at_index(index)
        statusbar['text'] = "Playing: " + listofsongs[index]
        update_details()
        update_display()
    except:
        tkinter.messagebox.showerror('Error', 'Select a directory')

def stopsong(event):
	global music_player
	if music_player.is_playing():
		music_player.stop()
		statusbar['text'] = "Stoped playing: "+ listofsongs[index]
		v.set("")

def set_vol(val):
    global volume
    global music_player
    global song
    volume = int(val)
    song.audio_set_volume(volume)

def mute_music(event):
    global muted
    global initial_volume
    global music_player
    global song
    if muted:  # Music is muted
        mutebutton.configure(image=unmute_button)
        song.audio_toggle_mute()
        volume_scale.set(initial_volume)
        statusbar['text'] = "Playing: " + listofsongs[index]
        muted = False
    else:  # Music is not muted
        initial_volume = volume
        mutebutton.configure(image=mute_button)
        song.audio_toggle_mute()
        volume_scale.set(0)
        statusbar['text'] = "Muted "
        muted = True

def shufflesong(event):
    global index
    global shuffled
    if shuffled:
        shuffled = False
        noshufflebutton.configure(image=noshuffle_button)
    else:
        shuffled = True
        noshufflebutton.configure(image=shuffle_button)
def repeatsong(event):
    global repeat
    if repeat:
        repeat = False
        repeatbutton.configure(image = repeat_button)
    else:
        repeat = True
        repeatbutton.configure(image = repeat1_button)

def set_song_time(val):
	global music_player
	global song
	total_length = song.get_length()
	val = int(val)
	time = int((val*total_length)/100)
	song.set_time(time)





drop_menu = Menu(root)
root.config(menu = drop_menu)


file_menu = Menu(drop_menu, tearoff = 0)
drop_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "Open", command = directorychooser)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command = root.quit)

options_menu = Menu(drop_menu, tearoff = 0)
drop_menu.add_cascade(label = "Options", menu = options_menu)
options_menu.add_command(label = "Equalizer", command = equalizer_window)

help_menu = Menu(drop_menu, tearoff = 0)
drop_menu.add_cascade(label = "Help", menu = help_menu)
help_menu.add_command(label = "About Us", command = about_us)



root.title("Music PLayer")
#Status Bar
statusbar = Label(root, text = "Waiting for directory to be choosen", bd=1, relief = SUNKEN, anchor = W)# bd = border, sunken makes status bar deep, anchor= W meaning text will always appear in left
statusbar.pack(side = BOTTOM, fill = X)

#CONTROL
control_frame = Frame(root)
control_frame.pack(side = BOTTOM, fill = X)

previous_button=PhotoImage(file="images/previous-button.png")
previousbutton = Button(control_frame,image = previous_button, anchor = W)
previousbutton.pack(side = LEFT)

play_button=PhotoImage(file="images/play-button.png")
playbutton = Button(control_frame,image = play_button)
playbutton.pack(side = LEFT)

pause_button = PhotoImage(file="images/pause-button.png")
pausebutton = Button(control_frame, image = pause_button)
pausebutton.pack(side = LEFT)
  
stop_button = PhotoImage(file="images/stop-button.png")
stopbutton = Button(control_frame,image = stop_button)
stopbutton.pack(side = LEFT)

next_button = PhotoImage(file="images/next-button.png")
nextbutton = Button(control_frame,image = next_button)
nextbutton.pack(side = LEFT)

shuffle_button = PhotoImage(file="images/shuffle-button.png")
noshuffle_button=PhotoImage(file="images/noshuffle-button.png")
noshufflebutton = Button(control_frame, image=noshuffle_button)
noshufflebutton.pack(side=LEFT, padx=10)

repeat1_button = PhotoImage(file="images/repeat-button1.png")


repeat_button = PhotoImage(file="images/repeat-button.png")
repeatbutton = Button(control_frame, image=repeat_button)
repeatbutton.pack(side=LEFT)

volume_scale = Scale(control_frame, from_ = 0, to = 100, orient = HORIZONTAL, command =set_vol)
volume_scale.set(80)
volume_scale.pack(side = RIGHT)

mute_button = PhotoImage(file="images/mute-button.png")
unmute_button = PhotoImage(file="images/unmute-button.png")
mutebutton = Button(control_frame,image = unmute_button)
mutebutton.pack(side = RIGHT, padx = 3, anchor = S)



previousbutton.bind("<Button-1>",prevsong)
playbutton.bind("<Button-1>",playsong)
pausebutton.bind("<Button-1>",pausesong)
stopbutton.bind("<Button-1>",stopsong)
nextbutton.bind("<Button-1>",nextsong)
mutebutton.bind("<Button-1>",mute_music)
noshufflebutton.bind("<Button-1>", shufflesong)
repeatbutton.bind("<Button-1>", repeatsong)

#LABEL #DETAIL
detail_frame = Frame(root)
detail_frame.pack(side = BOTTOM, fill = X)

time_detail = Label(detail_frame, text = '--:-- / --:--')
time_detail.pack(side = RIGHT, anchor = S)

visual_detail = Scale(detail_frame, orient = HORIZONTAL, showvalue = 0, command = set_song_time)
visual_detail.pack(fill = X, expand = 1, side = LEFT)


v = StringVar()
'''
songlabel = Label(detail_frame,textvariable=v, height = 2)
songlabel.pack(side = LEFT)'''



#LIST
list_frame = Frame(root)
list_frame.pack(side = RIGHT, fill = Y)
listbox = Listbox(list_frame, width = 40)
listbox.pack(fill = BOTH, expand = 1)



# MEDIA
media_frame = Frame(root)
media_frame.pack(side = LEFT, fill = BOTH, expand = YES)

displaybox = Listbox(media_frame)
displaybox.pack( expand = YES, fill = BOTH)


'''def close_program():
    stopsong("<Button-1>")
    root.destroy()






root.protocol("WM_DELETE_WINDOW", close_program)'''
root.mainloop()