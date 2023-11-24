import os
import shutil
import json
import numpy as np
import keras as keras
import librosa
import math
import subprocess


subprocess.run(["python", "sample.py"])
# Path to the trained model
MODEL_PATH = "Music_Genre_11_CNN.h5"

# Path to the folder containing the music files
MUSIC_FOLDER = "classify"

# Path to the destination folder for each genre
DESTINATION_FOLDER = "predictn"


# Load the trained model
model = keras.models.load_model(MODEL_PATH)

# Audio files pre-processing
def process_input(audio_file, track_duration):
    SAMPLE_RATE = 22050
    NUM_MFCC = 13
    N_FTT = 2048
    HOP_LENGTH = 512
    TRACK_DURATION = track_duration  # measured in seconds
    SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION
    NUM_SEGMENTS = 10

    samples_per_segment = int(SAMPLES_PER_TRACK / NUM_SEGMENTS)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / HOP_LENGTH)

    signal, sample_rate = librosa.load(audio_file, sr=SAMPLE_RATE)

    mfcc = []
    for d in range(NUM_SEGMENTS):
        # calculate start and finish sample for current segment
        start = samples_per_segment * d
        finish = start + samples_per_segment

        # extract mfcc
        mfcc_segment = librosa.feature.mfcc(
            y=signal[start:finish], sr=sample_rate, n_mfcc=NUM_MFCC, n_fft=N_FTT, hop_length=HOP_LENGTH
        )
        mfcc_segment = mfcc_segment.T

        mfcc.append(mfcc_segment)

    return np.array(mfcc)

# Genre dictionary
genre_dict = {
    0: "neutral",
    1: "angry",
    2: "fear",
    3: "disgust",
    4: "surprise",
    5: "happy",
    6: "sad",
}

# Create the destination folders if they don't exist
for genre_folder in genre_dict.values():
    folder_path = os.path.join(DESTINATION_FOLDER, genre_folder)
    os.makedirs(folder_path, exist_ok=True)



# Iterate through the music files in the folder
for filename in os.listdir(MUSIC_FOLDER):
    file_path = os.path.join(MUSIC_FOLDER, filename)

    # Process the input audio file
    input_mfcc = process_input(file_path, 30)
    input_mfcc = input_mfcc[..., np.newaxis]

    # Perform prediction
    prediction = model.predict(input_mfcc)
    predicted_index = np.argmax(prediction, axis=1)[0]  # Extract scalar value

    if predicted_index == 0:
        predicted_genre = ("angry", "happy")
    elif predicted_index == 1:
        predicted_genre = ("happy", "sad")
    elif predicted_index == 2:
        predicted_genre = ("surprise",)
    elif predicted_index == 3:
        predicted_genre = ("neutral",)
    elif predicted_index == 4:
        predicted_genre = ("angry", "fear")
    elif predicted_index == 5:
        predicted_genre = ("happy", "surprise")
    elif predicted_index == 6:
        predicted_genre = ("angry", "disgust")
    elif predicted_index == 7:
        predicted_genre = ("sad", "neutral")
    elif predicted_index == 8:
        predicted_genre = ("happy",)
    elif predicted_index == 9:
        predicted_genre = ("happy",)
    else:
        predicted_genre = (genre_dict[predicted_index],)  # Use scalar value as index


    for genre in predicted_genre:
        # Create the genre folder if it doesn't exist
        genre_folder_path = os.path.join(DESTINATION_FOLDER, genre)
        os.makedirs(genre_folder_path, exist_ok=True)

        # Move the file to the predicted genre folder
        destination_path = os.path.join(genre_folder_path, filename)
        shutil.copy(file_path, destination_path)
    os.remove(file_path)


    print(f"Moved '{filename}' to '{predicted_genre}' folders.")
