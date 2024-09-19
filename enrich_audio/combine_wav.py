import wave
import os
import random  # Import random module for shuffling

def merge_wav_files(input_folder, output_file):
    # Function to recursively get all WAV files in a folder and its subfolders
    def get_wav_files_recursive(folder):
        wav_files = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.wav'):
                    wav_files.append(os.path.join(root, file))
        return wav_files
    
    # Get a list of all WAV files in the input folder and its subfolders
    wav_files = get_wav_files_recursive(input_folder)
    
    # Check if there are any WAV files in the folder
    if not wav_files:
        print("No WAV files found in the input folder.")
        return
    
    # Randomize the order of wav_files
    random.shuffle(wav_files)
    
    # Open the first WAV file to get parameters
    first_wav = wave.open(wav_files[0], 'rb')
    params = first_wav.getparams()
    first_wav.close()
    
    # Create the output WAV file
    output_wav = wave.open(output_file, 'wb')
    output_wav.setparams(params)
    
    # Iterate over each WAV file in the randomized order, read its content, and write to the output file
    for wav_file in wav_files:
        with wave.open(wav_file, 'rb') as f:
            output_wav.writeframes(f.readframes(f.getnframes()))
    
    output_wav.close()
    print("Merged WAV file saved as", output_file)

# Example usage:
input_folder = 'output_segments/all_speakers'
output_file = 'output_segments/all_in_one/merged3.wav'
merge_wav_files(input_folder, output_file)
