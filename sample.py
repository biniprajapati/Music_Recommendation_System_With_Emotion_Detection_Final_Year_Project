import os
import librosa
import soundfile as sf

def convert_sample_rate(input_folder, output_folder, target_sr=22050):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".wav") or filename.endswith(".mp3"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Load audio using librosa
            audio, sr = librosa.load(input_path, sr=None)

            # Resample audio to the target sample rate
            audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)

            # Save the resampled audio using soundfile library
            sf.write(output_path, audio_resampled, target_sr)
            print(f"Converted: {filename}")



def convert_sample_rate2(input_folder, output_folder2, target_sr=22050):
    os.makedirs(output_folder2, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".wav") or filename.endswith(".mp3"):
            input_path = os.path.join(input_folder, filename)
            output_path2 = os.path.join(output_folder2, filename)

            # Load audio using librosa
            audio, sr = librosa.load(input_path, sr=None)

            # Resample audio to the target sample rate
            audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)

            # Save the resampled audio using soundfile library
            sf.write(output_path2, audio_resampled, target_sr)
            print(f"Converted: {filename}")

            os.remove(input_path)
            print(f"Deleted: {input_path}")



if __name__ == "__main__":
    input_folder = "audio"
    output_folder = "resampled"
    output_folder2 = "classify"
    target_sample_rate = 22050
    convert_sample_rate(input_folder, output_folder, target_sample_rate)
    convert_sample_rate2(input_folder, output_folder2, target_sample_rate)
