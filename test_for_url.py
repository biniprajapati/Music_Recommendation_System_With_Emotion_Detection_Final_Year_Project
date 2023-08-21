import tkinter as tk
from tkinter import filedialog
import pygame
import youtube_dl
from pytube import YouTube
import os

def add_many_songs():
    # Prompt the user to enter URLs for songs
    url_input = tk.simpledialog.askstring("Add Songs from URL", "Enter the URL(s) of the song(s) to add (separated by commas):")
    urls = url_input.split(',')
    for url in urls:
        url = url.strip()
        if url.startswith('https://www.youtube.com/watch?v='):
            song_info = get_youtube_audio(url)
            if song_info:
                song_name = "Numb"  # Specify the song name
                song_box.insert(tk.END, song_name)
                download_song(song_info['url'], song_name)
        else:
            print(f"Invalid YouTube URL: {url}")




def get_youtube_audio(url):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        if audio:
            return {
                'title': yt.title,
                'url': audio.url,
            }
        else:
            print(f"No audio stream found for {yt.title}")
            return None
    except Exception as e:
        print(f"Failed to download audio from YouTube: {str(e)}")
        return None

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return {
                'title': info['title'],
                'url': info['url'],
            }
        except youtube_dl.DownloadError as e:
            print(f"Failed to download audio from YouTube: {str(e)}")
            return None

def download_song(url, song_name):
    pass

def play():
    global stopped
    stopped = False
    song = song_box.get(tk.ACTIVE)
    song_path = f'audio/{song}.mp3'

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)

# Create a Tkinter window
window = tk.Tk()

# Create a song_box object (e.g., a Listbox) to display the songs
song_box = tk.Listbox(window)
song_box.pack()

# Create buttons for adding songs and playing the selected song
add_songs_button = tk.Button(window, text="Add Songs", command=add_many_songs)
add_songs_button.pack()

play_button = tk.Button(window, text="Play", command=play)
play_button.pack()

# Initialize Pygame Mixer
pygame.mixer.init()

# Start the Tkinter event loop
window.mainloop()
