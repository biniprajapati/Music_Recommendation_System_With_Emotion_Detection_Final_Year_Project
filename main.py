import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import tensorflow as tf
from keras.models import load_model
from keras.utils import img_to_array
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
class MusicPlayerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.playing = False

        # middle frame

        label3 = ttk.Label(root, background='#0a4a54')

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
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/audio", "")
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

        label4 = ttk.Label(root, background='#0f6c7a')
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
    # Initialize pygame mixer
        pygame.mixer.init()
    def playlist(self):
        self.song_box.delete(0, tk.END)
        song1 = "C:/Users/binee/PycharmProjects/final_year_project/audio"
        song_files = os.listdir(song1)
        for song in song_files:
            song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/audio", "")
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
        song = f'C:/Users/binee/PycharmProjects/final_year_project/audio/{song}.mp3'

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
        song = f'C:/Users/binee/PycharmProjects/final_year_project/audio/{song}.mp3'
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
        song = f'C:/Users/binee/PycharmProjects/final_year_project/audio/{song}.mp3'
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

    # load weights into new model
    # emotion_model.load_weights("model/fer.h5")
    # print("Loaded model from disk")

    def __init__(self,parent,music_player_app_instance,video_source=0):
        self.parent = parent

        self.video_source = video_source
        self.music_player_app_instance = music_player_app_instance
        self.vid = cv2.VideoCapture(self.video_source)
        label3 = ttk.Label(root, background='#0a4a54')
        self.playing = False


        label3 = ttk.Label(root, background='#0a4a54')

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

        label4 = ttk.Label(root, background='#0f6c7a')
        label4.place(relx=0.475, rely=0.13, relwidth=0.3, relheight=0.7)

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
                                   length=450)
        self.my_slider.config(style='Horizontal.TScale')
        self.my_slider.place(relx=0.05, rely=0.8, relwidth=0.9)

        self.youtube_frame = tk.Frame(root, bg="white")
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


        self.last_emotion = None
        label5 = ttk.Label(root, background='#0a4a54')
        label5.place(relx=0.785, rely=0.13, relwidth=0.2, relheight=0.7)

        self.my_button2 = tk.Button(label5, text="Capture Photo", width=15, height=2, font=("Courier New", 10),
                                    fg="white",
                                    bg="#0a4a54", command=self.refresh_program)
        self.my_button2.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.1)

        #emotion buttons

        label6 = ttk.Label(root, background='#0f6c7a')
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

        # self.slider_label = Label(label4, text = "0")
        # self.slider_label.pack(pady=10)

        self.Capture_photo()
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

        python = sys.executable
        os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Set the working directory to the script's location
        subprocess.Popen([python,"main.py"])






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
        song = f'C:/Users/binee/PycharmProjects/final_year_project/audio/{song}.mp3'
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
        song = f'C:/Users/binee/PycharmProjects/final_year_project/audio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.song_box.selection_clear(0, END)
        self.song_box.activate(next_one)

        self.song_box.selection_set(next_one, last=None)
    def play_time(self):
        # grab current song elapsed time
        current_time = pygame.mixer.music.get_pos() /1000

        #throw up temp label to get data
        # self.slider_label.config(text=f'Slider: {int(self.my_slider.get())} and Song Pos: {int(current_time)}')

        converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))

        # next_one = self.song_box.curselection()

        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/audio/{song}.mp3'
        song_mut = MP3(song)
        global song_length

        song_length = song_mut.info.length

        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

        current_time +=1
        if int(self.my_slider.get()) == int(song_length):
            self.status_bar.config(text=f'Time Elapsed:{converted_song_length} ')






        elif int(self.my_slider.get()) == int(current_time):
            slider_position = int(song_length)

            self.my_slider.config(to=slider_position, value=int(current_time))

        else:
            slider_position = int(song_length)

            self.my_slider.config(to=slider_position, value=int(self.my_slider.get()))
            converted_current_time = time.strftime('%M:%S', time.gmtime(int(self.my_slider.get())))
            self.status_bar.config(text=f'Time Elapsed:{converted_current_time} of {converted_song_length} ')

            next_time = int(self.my_slider.get()) + 1

            self.my_slider.config(value=next_time)
        # self.status_bar.config(text=f'Time Elapsed:{converted_current_time} of {converted_song_length} ')
        # self.my_slider.config(value=int(current_time))

        # update slider to position



        # self.my_slider.config(to=slider_position, value = int(current_time))
        # update time
        self.status_bar.after(1000, self.play_time)

    def playlist(self):
        self.song_box.delete(0, tk.END)
        song1 = "C:/Users/binee/PycharmProjects/final_year_project/audio"
        song_files = os.listdir(song1)
        for song in song_files:

            song_name = os.path.splitext(song)[0]
            self.song_box.insert(tk.END, song_name)


        if not self.playing and self.song_files:
            first_song = song_files[0]
            self.song_path = os.path.join(song1, first_song)
            self.play_music_auto(self.song_path)

    def play_selected_song(self, event):
        selected_song_index = self.song_box.curselection()
        if selected_song_index:


            self.current_track = selected_song_index[0]
            self.play_music()
    def play_music(self):

        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/audio/{song}.mp3'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)


        self.update_play_button()
        # self.play_time()

    def play_music_auto(self,song_path):

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0)


        self.update_play_button()



        #call the play_time() function
        self.play_time()

        #update slider to position

        # slider_position = int(song_length)
        # self.my_slider.config(to=slider_position, value = 0)
    def slide(self,x):




        song = self.song_box.get(ACTIVE)
        song = f'C:/Users/binee/PycharmProjects/final_year_project/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0, start=int(self.my_slider.get()))





        # load json and create modelS




    def Capture_photo(self):


        face_classifier = cv2.CascadeClassifier(
            r"C:\Users\binee\PycharmProjects\embp\haarcascade_frontalface_default1.xml")
        classifier = load_model(r'C:\Users\binee\PycharmProjects\embp\model.h5')

        emotions_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

        cap = cv2.VideoCapture(0)

        while True:
            _, frame = cap.read()
            labels = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_LINEAR)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    prediction = classifier.predict(roi)[0]
                    label = emotions_labels[prediction.argmax()]
                    label_position = (x, y - 10)
                    self.last_emotion = label
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, 'NO FACES', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Emotion Detector", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imwrite("captured_photo.png", frame)
            cv2.imwrite("captured_photo.png", frame)

        # After the loop release the cap object
        self.vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

        textframe = Frame(root, width=300, height=70, bg="white")
        textframe.place(relx=0.885, rely=0.7, anchor=CENTER)
        self.my_b = tk.Button(textframe, text= self.last_emotion, width=15, height=2, font=("Courier New", 15), fg="white",
                                   bg="#0a4a54")
        self.my_b.pack(pady=5)
        print("Last detected emotion:", self.last_emotion)

        self.predict()


    def predict(self):
        if self.last_emotion == "Angry":
            self.angry()



        elif self.last_emotion =='Disgust':
            song1 = "C:/Users/binee/PycharmProjects/final_year_project/predictn/disgust"
            song_files = os.listdir(song1)
            for song in song_files:
                song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/predictn/disgust", "")
                song = song.replace(".mp3", "")
                self.song_box.insert(END, song)

        elif self.last_emotion == "Fear":
            song1 = "C:/Users/binee/PycharmProjects/final_year_project/predictn/fear"
            song_files = os.listdir(song1)
            for song in song_files:
                song = song.replace("C:/Users/binee/PycharmProjects/final_year_project/predictn/fear", "")
                song = song.replace(".mp3", "")
                self.song_box.insert(END, song)

        elif self.last_emotion == "Happy":
            self.happy()

        elif self.last_emotion == "Neutral":
            self.normal()

        elif self.last_emotion == "Sad":
            self.sad()

        elif self.last_emotion == "Surprise":
            self.surprise()

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





# window
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()

    root.title('Emotion Based Music PLayer')
    root.geometry("1300x600")
    root.configure(bg="#0b798c")
    music_image = Image.open('music_image.png')
    image_icon = PhotoImage(file="music_image.png")
    root.iconphoto(False, image_icon)

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
    top_frame = ttk.Frame(root)
    label1 = ttk.Label(top_frame, image=logo, background='#0b798c')
    label2 = ttk.Label(top_frame, text='EMOTION BASED MUSIC PLAYER', background='#0b798c', style="Custom.TLabel",
                   foreground='white')
    labelr = ttk.Label(top_frame, text='EMOTION BASED MUSIC PLAYER BASED MUSIC PLAYERrr', background='#0b798c',
                   style="Custom.TLabel",
                   foreground='#0b798c')

# camera frame


# BOTTOM FRAME
    bottom_frame = ttk.Frame(root)
    label6 = ttk.Label(bottom_frame, text='label6', background='white')

# top layout
    label1.pack(side='left', expand=True, padx=10)
    label2.pack(side='left', expand=True, fill='y')
    labelr.pack(side='left', expand=True, fill='y')
    top_frame.pack(side='top')




    music_app = MusicPlayerApp(root)
    camera_app = CameraApp(root,music_app)
    photo = Image.open("captured_photo.png")
    resize1 = photo.resize((200, 200), Image.ANTIALIAS)
    label1 = ImageTk.PhotoImage(resize1)

    dframe = Frame(root, width=300, height=250)
    dframe.place(relx=0.885, rely=0.45, anchor=CENTER)


    image_label = Label(dframe, image=label1)
    image_label.pack()

# run
    root.mainloop()
