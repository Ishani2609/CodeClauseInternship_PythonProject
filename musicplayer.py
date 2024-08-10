import os
import tkinter as tk
from tkinter import filedialog, ttk
from pygame import mixer
from mutagen.mp3 import MP3
import time

# Initialize the mixer
mixer.init()

# Create the main application window
root = tk.Tk()
root.title("Enhanced Python Music Player")
root.geometry("600x400")  # Ensure the window size is appropriate for new features

# Global variables
current_song = ""
paused = False
playlist = []

# Function to load a song
def load_song():
    global current_song
    current_song = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    add_to_playlist(current_song)

# Function to add a song to the playlist
def add_to_playlist(song):
    song_name = os.path.basename(song)
    playlist_box.insert(tk.END, song_name)
    playlist.append(song)

# Function to play the selected song
def play_song():
    global paused
    selected_song = playlist_box.curselection()
    if selected_song:
        song = playlist[selected_song[0]]
        mixer.music.load(song)
        mixer.music.play()
        show_details(song)
        paused = False

# Function to pause the song
def pause_song():
    global paused
    mixer.music.pause()
    paused = True

# Function to stop the song
def stop_song():
    mixer.music.stop()
    status_bar.config(text="Music Stopped")

# Function to load and play all songs from a folder
def load_and_play_folder():
    folder = filedialog.askdirectory()
    if folder:
        for song in os.listdir(folder):
            if song.endswith(".mp3") or song.endswith(".wav"):
                add_to_playlist(os.path.join(folder, song))

# Function to set volume
def set_volume(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

# Function to show details of the song
def show_details(song):
    file_data = os.path.splitext(song)
    if file_data[1] == ".mp3":
        audio = MP3(song)
        total_length = audio.info.length
    else:
        total_length = mixer.Sound(song).get_length()
    
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    status_bar.config(text="Playing... " + time_format)

    start_count(total_length)

# Function to update the progress bar and time
def start_count(t):
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            current_time_label.config(text="Current Time: " + time_format)
            progress_bar['value'] = (current_time / t) * 100
            time.sleep(1)
            current_time += 1

# Create Playlist box
playlist_box = tk.Listbox(root, selectmode=tk.SINGLE, bg="lightyellow", fg="black", width=50, height=10)
playlist_box.pack(pady=20)

# Create buttons
control_frame = tk.Frame(root)
control_frame.pack(pady=20)

load_btn = tk.Button(control_frame, text="Load Song", command=load_song)
play_btn = tk.Button(control_frame, text="Play", command=play_song)
pause_btn = tk.Button(control_frame, text="Pause", command=pause_song)
stop_btn = tk.Button(control_frame, text="Stop", command=stop_song)
play_all_btn = tk.Button(control_frame, text="Load Folder", command=load_and_play_folder)

load_btn.grid(row=0, column=0, padx=10)
play_btn.grid(row=0, column=1, padx=10)
pause_btn.grid(row=0, column=2, padx=10)
stop_btn.grid(row=0, column=3, padx=10)
play_all_btn.grid(row=0, column=4, padx=10)

# Volume control
volume_frame = tk.Frame(root)
volume_frame.pack()

volume_label = tk.Label(volume_frame, text="Volume")
volume_label.grid(row=0, column=0)

volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume)
volume_slider.set(70)
volume_slider.grid(row=0, column=1, padx=20)

# Progress bar
progress_frame = tk.Frame(root)
progress_frame.pack(pady=20)

current_time_label = tk.Label(progress_frame, text="Current Time: --:--")
current_time_label.grid(row=0, column=0)

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=0, column=1, padx=20)

# Status bar
status_bar = tk.Label(root, text="Welcome to the Music Player", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)

# Start the application
root.mainloop()
