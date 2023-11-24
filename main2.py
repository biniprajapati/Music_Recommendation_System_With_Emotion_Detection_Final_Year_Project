import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import tensorflow as tf
from keras.models import load_model
from keras.utils import img_to_array
import dlib
import math
import psutil
from keras.preprocessing import image
import subprocess

import pygame
import os
import cv2
import numpy as np

from mutagen.mp3 import MP3



from time import sleep
from keras.preprocessing import image
import webbrowser
import subprocess


class MusicPlayerApp:

    def __init__(self, root1):
        self.root1 = root1
        self.root1.title("Music Player")
        self.playing = False

        # middle frame

        label3 = ttk.Label(root1, background='#0a4a54')

        # middle_layout
        label3.place(relx=0.015, rely=0.13, relwidth=0.45, relheight=0.7)
        self.my_button = tk.Button(label3, text="Playlist",width=15, height=2, font=("Courier New",15),fg="white", bg="#0a4a54", command=self.playlist)
        self.my_button.pack(pady=5)
        # Add your music file path here
        self.music_file = "path/to/your/music.mp3"
        self.song_box = tk.Listbox(label3, font=("Times new roman",10), bg="#0f6c7a", fg="black", selectbackground="lightblue", cursor="hand2", bd=0)
        self.song_box.place(relx=0.05, rely=0.15,relwidth=0.9, relheight=0.8)
        self.song_box.bind("<Double-Button-1>", self.play_selected_song)

        # Add songs to the Listbox (you can customize this part with your song list)
        song1 = "C:/Users/binee/PycharmProjects/final_year_project/audio"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/resampled", "")
            song = song.replace(".mp3", "")
            self.song_box.insert(tk.END, song)

        # Create a "Play" button to play the selected song

        self.play_image = Image.open('play.png')
        resized_image = self.play_image.resize((50, 50), Image.ANTIALIAS)
        self.play_button_img = ImageTk.PhotoImage(resized_image)

        self.back_image = Image.open('back.png')
        resized_image = self.back_image.resize((50, 50), Image.ANTIALIAS)
        self.back_button_img = ImageTk.PhotoImage(resized_image)

        self.front_image = Image.open('front.png')
        resized_image = self.front_image.resize((50, 50), Image.ANTIALIAS)
        self.front_button_img = ImageTk.PhotoImage(resized_image)

        self.pause_image = Image.open('pause.png')
        resized_image = self.pause_image.resize((50, 50), Image.ANTIALIAS)
        self.pause_button_img = ImageTk.PhotoImage(resized_image)

        self.stop_image = Image.open('stop.png')
        resized_image = self.stop_image.resize((50, 50), Image.ANTIALIAS)
        self.stop_button_img = ImageTk.PhotoImage(resized_image)
        # Create and configure the music player buttons

        label4 = ttk.Label(root1, background='#0f6c7a')
        label4.place(relx=0.475, rely=0.13, relwidth=0.3, relheight=0.7)



        self.player_text_box = tk.Label(label4, text="MUSIC PlAYER",font=("Courier New",15),fg="white", bg="#0a4a54")
        self.player_text_box.pack(side = tk.TOP,pady =30)

        # self.pause_button = tk.Button(label4, bg="#0f6c7a", bd=0, image=self.pause_button_img,
        #                               command=self.pause_music)
        # self.pause_button.place(relx=0.43, rely=0.25)
        self.back_button = tk.Button(label4, bg="#0f6c7a", bd=0, image=self.back_button_img,
                                     command=self.back_music)
        self.back_button.place(relx=0.15, rely=0.5)

        self.play_button = tk.Button(label4, bg="#0f6c7a", bd=0,image=self.play_button_img, command=self.toggle_play_pause)
        self.play_button.place(relx=0.43, rely=0.5)

        self.front_button = tk.Button(label4,bg="#0f6c7a", bd=0, image=self.front_button_img, command=self.front_music)
        self.front_button.place(relx=0.71, rely=0.5)

         #Create the slider with a transparent background

        self.my_slider = ttk.Scale(label4, from_=0, to=100, orient='horizontal', value=0, command=self.slide, length=450)
        self.my_slider.config(style='Horizontal.TScale')
        self.my_slider.place(relx=0.05, rely=0.8,relwidth=0.9)

        self.slider_label = Label(label4, text = "0")
        self.slider_label.pack(pady=10)
        photo = Image.open("captured_photo.png")
        resize1 = photo.resize((200, 200), Image.ANTIALIAS)
        label1 = ImageTk.PhotoImage(resize1)

        dframe = Frame(self.root1, width=300, height=250)
        dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

        self.image_label = tk.Label(dframe, image=label1)
        self.image_label.pack()
    # Initialize pygame mixer
        pygame.mixer.init()
    def playlist(self):
        self.song_box.delete(0, tk.END)
        song1 = "C:/Users/binee/PycharmProjects/final_year_project/resampled"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/resampled", "")
            song = song.replace(".mp3", "")
            self.song_box.insert(tk.END, song)

        if not self.playing and self.song_files:
            first_song = song_files[0]
            song_path = os.path.join(song1, first_song)
            self.play_music_auto(song_path)
    def play_selected_song(self, event):
        selected_song_index = self.song_box.curselection()
        if selected_song_index:
            self.current_track = selected_song_index[0]
            self.play_music()

    def toggle_play_pause(self):
        if self.playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.playing = not self.playing
        self.update_play_button()

    def update_play_button(self):
        if self.playing:
            self.play_button.configure(image=self.pause_button_img)
        else:
            self.play_button.configure(image=self.play_button_img)
    def play_music(self):
        global stopped
        stopped = False
        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/resampled/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.playing = True

    global stopped
    stopped = False

    def pause_music(self,is_paused):
        pygame.mixer.music.stop()

    def front_music(self):

        self.my_slider.config(value=0)

        next_one = self.song_box.curselection()
        next_one = next_one[0] + 1
        song = self.song_box.get(next_one)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/resampled/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.song_box.selection_clear(0, END)
        self.song_box.activate(next_one)

        self.song_box.selection_set(next_one, last=None)

    def back_music(self):

        self.my_slider.config(value=0)

        next_one = self.song_box.curselection()
        next_one = next_one[0] - 1
        song = self.song_box.get(next_one)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/resampled/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.song_box.selection_clear(0, END)
        self.song_box.activate(next_one)

        self.song_box.selection_set(next_one, last=None)

    def slide(self):
        pygame.mixer.music.stop()


class CameraApp:
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    json_file = open('model/fer.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    face_classifier = cv2.CascadeClassifier(r"C:\Users\binee\PycharmProjects\embp\haarcascade_frontalface_default1.xml")
    emotion_model = load_model(r'C:\Users\binee\PycharmProjects\embp\model.h5')
    capturing = False
    fer_model = load_model('best_fer_model.h5')




    # load weights into new model
    # emotion_model.load_weights("model/fer.h5")
    # print("Loaded model from disk")

    def __init__(self,parent,music_player_app_instance,video_source=0):
        self.parent = parent

        self.video_source = video_source
        self.music_player_app_instance = music_player_app_instance
        self.vid = cv2.VideoCapture(self.video_source)
        label3 = ttk.Label(parent, background='#0a4a54')
        self.playing = False


        label3 = ttk.Label(parent, background='#0a4a54')

        # middle_layout
        label3.place(relx=0.015, rely=0.13, relwidth=0.45, relheight=0.7)
        self.my_button = tk.Button(label3, text="Playlist", width=15, height=2, font=("Courier New", 15), fg="white",
                                   bg="#0a4a54", command=self.playlist)
        self.my_button.pack(pady=5)
        # Add your music file path here
        self.music_file = "path/to/your/music.mp3"
        self.song_box = tk.Listbox(label3, font=("Times new roman", 10), bg="#0f6c7a", fg="black",
                                   selectbackground="lightblue", cursor="hand2", bd=0)
        self.song_box.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.8)
        self.song_box.bind("<Double-Button-1>", self.play_selected_song)
        song1 = "C:/Users/binee/PycharmProjects/final_year_project/audio"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/resampled", "")
            song = song.replace(".mp3", "")
            self.song_box.insert(tk.END, song)


        label3 = ttk.Label(parent, background='#0a4a54')

        # middle_layout
        label3.place(relx=0.015, rely=0.13, relwidth=0.45, relheight=0.7)

        self.my_button = tk.Button(label3, text="Playlist", width=15, height=2, font=("Courier New", 15), fg="white",
                                   bg="#0a4a54", command=self.playlist)
        self.my_button.pack(pady=5)

        # middle_layout
        label3.place(relx=0.015, rely=0.13, relwidth=0.45, relheight=0.7)
        pygame.mixer.init()

        # Add your music file path here
        self.music_file = "path/to/your/music.mp3"
        self.song_box = tk.Listbox(label3, font=("Times new roman", 10), bg="#0f6c7a", fg="black",
                                   selectbackground="lightblue", cursor="hand2", bd=0)
        self.song_box.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.8)
        self.song_box.bind("<Double-Button-1>", self.play_selected_song)

        # Create a "Play" button to play the selected song

        self.play_image = Image.open('play.png')
        resized_image = self.play_image.resize((50, 50), Image.ANTIALIAS)
        self.play_button_img = ImageTk.PhotoImage(resized_image)

        self.back_image = Image.open('back.png')
        resized_image = self.back_image.resize((50, 50), Image.ANTIALIAS)
        self.back_button_img = ImageTk.PhotoImage(resized_image)

        self.front_image = Image.open('front.png')
        resized_image = self.front_image.resize((50, 50), Image.ANTIALIAS)
        self.front_button_img = ImageTk.PhotoImage(resized_image)

        self.pause_image = Image.open('pause.png')
        resized_image = self.pause_image.resize((50, 50), Image.ANTIALIAS)
        self.pause_button_img = ImageTk.PhotoImage(resized_image)

        self.stop_image = Image.open('stop.png')
        resized_image = self.stop_image.resize((50, 50), Image.ANTIALIAS)
        self.stop_button_img = ImageTk.PhotoImage(resized_image)
        # Create and configure the music player buttons

        label4 = ttk.Label(parent, background='#0f6c7a')
        label4.place(relx=0.475, rely=0.13, relwidth=0.3, relheight=0.7)
        label8 = ttk.Label(parent, background='#0f6c7a')
        label8.place(relx=0.475, rely=0.68, relwidth=0.3, relheight=0.09)

        self.player_text_box = tk.Label(label4, text="MUSIC PlAYER", font=("Courier New", 15), fg="white", bg="#0a4a54")
        self.player_text_box.pack(side=tk.TOP, pady=30)

        # self.pause_button = tk.Button(label4, bg="#0f6c7a", bd=0, image=self.pause_button_img,
        #                               command=self.pause_music)
        # self.pause_button.place(relx=0.43, rely=0.25)
        self.back_button = tk.Button(label4, bg="#0f6c7a", bd=0, image=self.back_button_img,
                                     command=self.back_music)
        self.back_button.place(relx=0.15, rely=0.5)

        self.play_button = tk.Button(label4, bg="#0f6c7a", bd=0, image=self.play_button_img,
                                     command=self.toggle_play_pause)
        self.play_button.place(relx=0.43, rely=0.5)

        self.front_button = tk.Button(label4, bg="#0f6c7a", bd=0, image=self.front_button_img, command=self.front_music)
        self.front_button.place(relx=0.71, rely=0.5)

        # Create the slider with a transparent background

        self.status_bar = Label(label4, text ='', bd=1, relief=GROOVE,bg="#0a4a54",  anchor= E )
        self.status_bar.pack(fill=X, side = BOTTOM,ipady = 2)

        self.my_slider = ttk.Scale(label4, from_=0, to=100, orient='horizontal', value=0, command=self.slide,
                                   )

        self.my_slider.place(relx=0.05, rely=0.8, relwidth=0.9)

        self.slider_label =ttk.Label(label4,text='0')
        self.slider_label.place(relx=0.2, rely=0.86)


        self.youtube_frame = tk.Frame(parent, bg="white")
        self.youtube_frame.place(relx=0.835, rely=0.84, relwidth=0.15, relheight=0.15)

        self.youtube_button = Image.open('youtube.png')
        self.youtube_resize = self.youtube_button.resize((60, 50), Image.ANTIALIAS)
        self.youtube_img = ImageTk.PhotoImage(self.youtube_resize)

        self.youtube_button = tk.Button(self.youtube_frame, bg="#0f1a2b", bd=0, image=self.youtube_img,
                                   command=self.youtube)
        self.youtube_button.place(relx=0.4,rely=0,relwidth=0.6,relheight=0.5)
        self.youtube_text_box = tk.Button(self.youtube_frame, text="Youtube \n Recommendation", font=('Italic', 10),
                                          bg='light grey',
                                          bd=0,
                                          command=self.youtube)
        self.youtube_text_box.place(relx=0.4,rely=0.5,relwidth=0.6,relheight=0.5)
        self.youtube_text_box_english = tk.Button(self.youtube_frame, text="English",bg="#0a4a54", font=("Courier New", 10), fg="white",

                                          bd=0,
                                          command=self.english)
        self.youtube_text_box_english.place(relx=0,rely=0,relwidth=0.4,relheight=0.35)
        self.youtube_text_box_hindi = tk.Button(self.youtube_frame, text="Hindi",bg="#0a4a54",font=("Courier New", 10), fg="white",

                                          bd=0,
                                          command=self.hindi)
        self.youtube_text_box_hindi.place(relx=0,rely=0.35,relwidth=0.4,relheight=0.35)
        self.youtube_text_box_nepali = tk.Button(self.youtube_frame, text="Nepali",bg="#0a4a54", font=("Courier New", 10), fg="white",

                                          bd=0,
                                          command=self.nepali)
        self.youtube_text_box_nepali.place(relx=0,rely=0.7,relwidth=0.4,relheight=0.35)
        fer_model = load_model('best_fer_model.h5')
        # label5 = ttk.Label(root, background='#0a4a54')
        # label5.place(relx=0.785, rely=0.13, relwidth=0.2, relheight=0.7)
        #
        # self.my_button2 = tk.Button(label5, text="Capture Photo", width=15, height=2, font=("Courier New", 10),
        #                        fg="white",
        #                        bg="#0a4a54", command=self.refresh_program())
        # self.my_button2.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.1)


        self.last_emotion = None
        label5 = ttk.Label(parent, background='#0a4a54')
        label5.place(relx=0.785, rely=0.13, relwidth=0.2, relheight=0.7)

        self.my_button2 = tk.Button(label5, text="Capture Photo", width=15, height=2, font=("Courier New", 10),
                                    fg="white",
                                    bg="#0a4a54", command=self.refresh_program)
        self.my_button2.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.1)

        #emotion buttons

        label6 = ttk.Label(parent, background='#0f6c7a')
        label6.place(relx=0.01, rely=0.85, relwidth=0.82, relheight=0.12)


        self.my_button1 = tk.Button(label6, text="Happy", width=8, height=1, font=("Courier New", 10), fg="white",
                                   bg="#0a4a54", command=self.happy)
        self.my_button1.pack(pady=5,side=LEFT,padx=5)

        self.my_button2 = tk.Button(label6, text="Sad", width=8, height=1, font=("Courier New", 10), fg="white",
                                   bg="#0a4a54", command=self.sad)
        self.my_button2.pack(pady=5, side=LEFT, padx=5)
        self.my_button3 = tk.Button(label6, text="Angry", width=8, height=1, font=("Courier New", 10), fg="white",
                                    bg="#0a4a54", command=self.angry)
        self.my_button3.pack(pady=5, side=LEFT, padx=5)
        self.my_button4 = tk.Button(label6, text="Normal",width=8, height=1, font=("Courier New", 10), fg="white",
                                    bg="#0a4a54", command=self.normal)
        self.my_button4.pack(pady=5, side=LEFT, padx=5)
        self.my_button5 = tk.Button(label6, text="Surprise", width=8, height=1, font=("Courier New", 10), fg="white",
                                    bg="#0a4a54", command=self.surprise)
        self.my_button5.pack(pady=5, side=LEFT, padx=5)

        photo = Image.open("captured_photo.png")
        resize1 = photo.resize((200, 200), Image.ANTIALIAS)
        label1 = ImageTk.PhotoImage(resize1)

        dframe = Frame(self.parent, width=300, height=250)
        dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

        self.image_label = tk.Label(dframe, image=label1)
        self.image_label.pack()

        # self.slider_label = Label(label4, text = "0")
        # self.slider_label.pack(pady=10)


        self.Capture_photo(fer_model)
    pygame.mixer.init()

    def happy(self):
        self.song_box.delete(0, END)

        song1 = "C:/Users/binee/PycharmProjects/final_year_project/predictn/happy"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/predictn/happy", "")
            song = song.replace(".mp3", "")
            self.song_box.insert(END, song)

            self.play_music()

    def sad(self):
        self.song_box.delete(0, END)

        song1 = "C:/Users/binee/PycharmProjects/final_year_project/predictn/sad"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/predictn/sad", "")
            song = song.replace(".mp3", "")
            self.song_box.insert(END, song)
            self.play_music()

    def angry(self):
        self.song_box.delete(0, END)

        song1 = "C:/Users/binee/PycharmProjects/final_year_project/predictn/angry"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/predictn/angry", "")
            song = song.replace(".mp3", "")
            self.song_box.insert(END, song)

            self.play_music()

    def normal(self):
        self.song_box.delete(0, END)

        song1 = "C:/Users/binee/PycharmProjects/final_year_project/predictn/neutral"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/predictn/neutral", "")
            song = song.replace(".mp3", "")
            self.song_box.insert(END, song)

            self.play_music()

    def surprise(self):
        self.song_box.delete(0, END)

        song1 = "C:/Users/binee/PycharmProjects/final_year_project/predictn/surprise"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/predictn/surprise", "")
            song = song.replace(".mp3", "")
            self.song_box.insert(END, song)
            self.play_music()
    def refresh_program(self):
        fer_model = load_model('best_fer_model.h5')
        self.Capture_photo(fer_model)
        photo = Image.open("capture_image.png")
        resize1 = photo.resize((200, 200), Image.ANTIALIAS)
        label1 = ImageTk.PhotoImage(resize1)

        dframe = Frame(self.parent, width=300, height=250)
        dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

        image_label = tk.Label(dframe, image=label1)
        image_label.pack()

    def toggle_play_pause(self):

        if self.playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.playing = not self.playing
        self.update_play_button()

    def update_play_button(self):

        if self.playing:
            self.play_button.configure(image=self.pause_button_img)
        else:
            self.play_button.configure(image=self.play_button_img)




    global stopped
    stopped = False
    global paused

    def pause_music(self, is_paused):


            pygame.mixer.music.pause()


    def front_music(self):

        self.my_slider.config(value=0)

        next_one = self.song_box.curselection()
        next_one = next_one[0] + 1
        song = self.song_box.get(next_one)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/resampled/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.song_box.selection_clear(0, END)
        self.song_box.activate(next_one)

        self.song_box.selection_set(next_one, last=None)

    def back_music(self):

        self.my_slider.config(value=0)

        next_one = self.song_box.curselection()
        next_one = next_one[0] - 1
        song = self.song_box.get(next_one)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/resampled/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.song_box.selection_clear(0, END)
        self.song_box.activate(next_one)

        self.song_box.selection_set(next_one, last=None)
    def play_time(self):
        # grab current song elapsed time
        current_time = pygame.mixer.music.get_pos()/1000
        #thro up temp label to get data
        self.slider_label.config(text=f'Slider: {int(self.my_slider.get())} and Song Pos: {int(current_time)}')
        current_time += 1
        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/resampled/{song}.mp3'



        global song_length
        song_mut = MP3(song)
        song_length = song_mut.info.length

        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))



        if int(self.my_slider.get()) == int(song_length):
            self.status_bar.config(text=f'Time Elapsed:{converted_song_length} ')


        elif int(self.my_slider.get()) != int(current_time):
            slider_position=int(song_length)
            self.my_slider.config(to=slider_position, value=int(current_time))

        else:
            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=int(self.my_slider.get()))
            converted_current_time = time.strftime('%M:%S', time.gmtime(int(self.my_slider.get())))
            self.status_bar.config(text=f'Time Elapsed:{converted_current_time} of {converted_song_length} ')

            next_time = int(self.my_slider.get()) + 1
            self.my_slider.config(value=next_time)



        # update time
        self.status_bar.after(1000, self.play_time)

    def playlist(self):
        self.song_box.delete(0, tk.END)
        song1 = "C:/Users/binee/PycharmProjects/final_year_project/resampled"
        song_files = os.listdir(song1)
        for song in song_files:

            song_name = os.path.splitext(song)[0]
            self.song_box.insert(tk.END, song_name)


        if not self.playing and self.song_files:
            first_song = song_files[0]
            self.song_path = os.path.join(song1, first_song)
            self.play_music_auto(self.song_path)
            self.toggle_play_pause()


    def play_selected_song(self, event):
        selected_song_index = self.song_box.curselection()
        if selected_song_index:


            self.current_track = selected_song_index[0]
            self.play_music()
    def play_music(self):

        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/resampled/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)




        self.play_time()




    def play_happy_music(self):
        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/predictn/happy/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)




    def play_sad_music(self):
        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/predictn/sad/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)




    def play_neutral_music(self):
        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/predictn/neutral/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)



    def play_angry_music(self):
        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/predictn/angry/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)




    def play_surprise_music(self):
        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/predictn/surprise/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)


        self.play_music()


    def play_music_auto(self,song_path):

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0)
        self.toggle_play_pause()
        self.update_play_button()

        # call the play_time() function
        self.play_time()



    def slide(self,x):
        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/resampled/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0, start=int(self.my_slider.get()))





        # load json and create modelS

    emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
    clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(2, 3))
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def rect_to_bb(self,rect):
        # take a bounding predicted by dlib and convert it  to the format (x, y, w, h) as we would normally do with OpenCV
        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y
        return x, y, w, h

    def shape_to_np(self,shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)
        # loop over the 68 facial landmarks and convert them to a 2-tuple of (x, y)-coordinates
        for i in range(68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        # return the list of (x, y)-coordinates
        return coords

    def get_landmarks(self,shape, rect):
        xlist = []
        ylist = []
        _, _, w, h = self.rect_to_bb(rect)
        for i in range(68):  # x and y coordinates
            x = 48 * float(float(shape.part(i).x - rect.left()) / w)
            y = 48 * float(float(shape.part(i).y - rect.top()) / h)
            xlist.append(x)
            ylist.append(y)
        xmean = np.mean(xlist)
        ymean = np.mean(ylist)
        xcentral = [(x - xmean) for x in xlist]
        ycentral = [(y - ymean) for y in ylist]
        landmarks_vectorised = []
        for x, y, w, z in zip(xcentral, ycentral, xlist, ylist):
            landmarks_vectorised.append(w)
            landmarks_vectorised.append(z)
            meannp = np.asarray((ymean, xmean))
            coornp = np.asarray((z, w))
            dist = np.linalg.norm(coornp - meannp)
            landmarks_vectorised.append(dist)
            landmarks_vectorised.append((math.atan2(y, x) * 360) / (2 * math.pi))
        return landmarks_vectorised

    def Capture_photo(self,model,cam_id=0):

        cam = cv2.VideoCapture(cam_id)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        while True:
            _, frame = cam.read()
            image = self.clahe.apply(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            rects = self.detector(image, 1)
            # loop over the face detections
            for rect in rects:
                # determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
                shape = self.predictor(image, rect)
                coords = self.shape_to_np(shape)
                landmark_vect = np.expand_dims(np.array(self.get_landmarks(shape, rect)), axis=0)
                emotion_idx = np.argmax(model.predict(landmark_vect))
                # convert dlib's rectangle to a OpenCV-style bounding box [i.e., (x, y, w, h)], then draw the face bounding box
                (x, y, w, h) = self.rect_to_bb(rect)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # show the emotion
                cv2.putText(frame, self.emotions[emotion_idx], (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                            2)
                # loop over the (x, y)-coordinates for the facial landmarks and draw them on the image
                for (x, y) in coords:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                    cv2.imshow("Emotion Detector", frame)
                self.last_emotion = self.emotions[emotion_idx]



                if self.emotions[emotion_idx] != ['fear', 'digust']:
                    cv2.imwrite("captured_photo.png", frame)
                    cv2.imwrite("capture_image.png", frame)

                else:
                    fer_model = load_model('best_fer_model.h5')
                    self.Capture_photo(fer_model)













            if cv2.waitKey(3) & cv2.imwrite("captured_photo.png", frame) & cv2.imwrite("captured_photo.png", frame) :
                break


        cam.release()
        cv2.destroyAllWindows()

        photo = Image.open("captured_photo.png")
        resize1 = photo.resize((200, 200), Image.ANTIALIAS)
        label1 = ImageTk.PhotoImage(resize1)

        dframe = Frame(self.parent, width=300, height=250)
        dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

        self.image_label = tk.Label(dframe, image=label1)
        self.image_label.pack()


        textframe = Frame(self.parent, width=300, height=70, bg="white")
        textframe.place(relx=0.885, rely=0.7, anchor=CENTER)
        self.my_b = tk.Button(textframe, text= self.last_emotion, width=15, height=2, font=("Courier New", 15), fg="white",
                                   bg="#0a4a54")
        self.my_b.pack(pady=5)
        print("Last detected emotion:", self.last_emotion)

        self.predict()


    def predict(self):
        if self.last_emotion == "Angry":
            self.angry()
            photo = Image.open("captured_photo.png")
            resize1 = photo.resize((200, 200), Image.ANTIALIAS)
            label1 = ImageTk.PhotoImage(resize1)

            dframe = Frame(self.parent, width=300, height=250)
            dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

            self.image_label = tk.Label(dframe, image=label1)
            self.image_label.pack()





        elif self.last_emotion == "Happy":
            self.happy()
            photo = Image.open("captured_photo.png")
            resize1 = photo.resize((200, 200), Image.ANTIALIAS)
            label1 = ImageTk.PhotoImage(resize1)

            dframe = Frame(self.parent, width=300, height=250)
            dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

            self.image_label = tk.Label(dframe, image=label1)
            self.image_label.pack()

        elif self.last_emotion == "Neutral":
            self.normal()
            photo = Image.open("captured_photo.png")
            resize1 = photo.resize((200, 200), Image.ANTIALIAS)
            label1 = ImageTk.PhotoImage(resize1)

            dframe = Frame(self.parent, width=300, height=250)
            dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

            self.image_label = tk.Label(dframe, image=label1)
            self.image_label.pack()

        elif self.last_emotion == "Sad":
            self.sad()
            photo = Image.open("captured_photo.png")
            resize1 = photo.resize((200, 200), Image.ANTIALIAS)
            label1 = ImageTk.PhotoImage(resize1)

            dframe = Frame(self.parent, width=300, height=250)
            dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

            self.image_label = tk.Label(dframe, image=label1)
            self.image_label.pack()

        elif self.last_emotion == "Surprise":
            self.surprise()
            photo = Image.open("captured_photo.png")
            resize1 = photo.resize((200, 200), Image.ANTIALIAS)
            label1 = ImageTk.PhotoImage(resize1)

            dframe = Frame(self.parent, width=300, height=250)
            dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

            self.image_label = tk.Label(dframe, image=label1)
            self.image_label.pack()

        else:
            fer_model = load_model('best_fer_model.h5')
            self.Capture_photo(fer_model)



    def youtube(self):

        if self.last_emotion == 'Angry':
            search_query = self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Disgust':
            search_query = self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Fear':
            search_query = self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Happy':
            search_query = self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Neutral':
            search_query = self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Sad':
            search_query = self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Surprise':
            webbrowser.open(f"https://www.youtube.com/")

    def english(self):
        if self.last_emotion == 'Angry':
            search_query = "English+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Disgust':
            search_query = "English+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Fear':
            search_query = "English+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Happy':
            search_query = "English+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Neutral':
            search_query = "English+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Sad':
            search_query = "English+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Surprise':
            search_query = "English+" + self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

    def hindi(self):

        if self.last_emotion == "Angry":
            search_query = "hindi+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Disgust':
            search_query = "hindi+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Fear':
            search_query = "hindi+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Happy':
            search_query = "hindi+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Neutral':
            search_query = "hindi+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Sad':
            search_query = "hindi+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Surprise':
            search_query = "hindi+"+self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

    def nepali(self):

        if self.last_emotion == 'Angry':
            search_query = "nepali+"+ self.last_emotion + " +song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Disgust':
            search_query = "nepali+" + self.last_emotion + " +song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Fear':
            search_query = "nepali+" + self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Happy':
            search_query = "nepali+" +self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Neutral':
            search_query = "nepali+" +self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Sad':
            search_query = "nepali+" +self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        elif self.last_emotion == 'Surprise':
            search_query = "nepali+" + self.last_emotion + " song"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")



def main():
    subprocess.run(["python", "classification.py"])
    root1 = tk.Tk()
    style = ttk.Style()
    root1.title('Emotion Based Music PLayer')
    root1.geometry("1300x600")
    root1.configure(bg="#0b798c")
    music_image = Image.open('music_image.png')
    image_icon = PhotoImage(file="music_image.png")
    root1.iconphoto(False, image_icon)

    # DEFINE FONT AND SIZE
    font_name = "Courier New"
    font_size = 20


    # Set the font and size for the label
    style.configure("Custom.TLabel", font=(font_name, font_size))

    # logo
    image_icon = PhotoImage(file="music_image.png")
    logo = PhotoImage(file="music_image.png")
    logo = logo.subsample(logo.width() // 60, logo.height() // 60)

    # widgets

    # top frame
    top_frame = ttk.Frame(root1)
    label1 = ttk.Label(top_frame, image=logo, background='#0b798c')
    label2 = ttk.Label(top_frame, text='EMOTION BASED MUSIC PLAYER', background='#0b798c', style="Custom.TLabel",
                       foreground='white')
    labelr = ttk.Label(top_frame, text='EMOTION BASED MUSIC PLAYER BASED MUSIC PLAYERrr', background='#0b798c',
                       style="Custom.TLabel",
                       foreground='#0b798c')

    # camera frame

    # BOTTOM FRAME
    bottom_frame = ttk.Frame(root1)
    label6 = ttk.Label(bottom_frame, text='label6', background='white')

    # top layout
    label1.pack(side='left', expand=True, padx=10)
    label2.pack(side='left', expand=True, fill='y')
    labelr.pack(side='left', expand=True, fill='y')
    top_frame.pack(side='top')

    fer_model = load_model('best_fer_model.h5')

    music_app = MusicPlayerApp(root1)
    camera_app = CameraApp(root1, music_app)

    photo = Image.open("captured_photo.png")
    resize1 = photo.resize((200, 200), Image.ANTIALIAS)
    label1 = ImageTk.PhotoImage(resize1)

    dframe = Frame(root1, width=300, height=250)
    dframe.place(relx=0.885, rely=0.45, anchor=CENTER)

    image_label = tk.Label(dframe, image=label1)
    image_label.pack()
    # run
    root1.mainloop()


# window
if __name__ == "__main__":
    main()
