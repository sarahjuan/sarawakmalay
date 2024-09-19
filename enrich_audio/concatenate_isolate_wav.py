from pydub import AudioSegment
import csv
import os

def parse_rttm(rttm_file):
    speaker_turns = []
    with open(rttm_file, 'r') as file:
        rttm_reader = csv.reader(file, delimiter=' ')
        for row in rttm_reader:
            if len(row) >= 7:
                file_id = row[1]
                speaker_id = row[7]
                start_time = float(row[3])
                end_time = start_time + float(row[4])
                speaker_turns.append((file_id, start_time, end_time, speaker_id))
    return speaker_turns

def split_audio_by_speaker(audio_file, rttm_file, output_folder):
    audio = AudioSegment.from_wav(audio_file)
    speaker_turns = parse_rttm(rttm_file)
    for i, (file_id, start, end, speaker_id) in enumerate(speaker_turns):
        if not os.path.exists(f"{output_folder}/isolated/{file_id}"):
            os.makedirs(f"{output_folder}/isolated/{file_id}")
        segment = audio[int(start * 1000):int(end * 1000)]  # Convert to milliseconds
        output_file = f"{output_folder}/isolated/{file_id}/{speaker_id}_segment_{i}.wav"
        segment.export(output_file, format="wav")
        
def process_folder(audio_folder, rttm_folder, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each pair of audio and RTTM files
    for audio_file in os.listdir(audio_folder):
        if audio_file.endswith(".wav"):
            audio_file_path = os.path.join(audio_folder, audio_file)
            rttm_file = f"{os.path.splitext(audio_file_path)[0]}.rttm"
            rttm_file = rttm_file.replace('wav\\', 'rttm\\')
            print(rttm_file)
            if os.path.exists(rttm_file):
                split_audio_by_speaker(audio_file_path, rttm_file, output_dir)

# Example usage:
audio_folder = "wav"
rttm_folder = "rttm"
output_dir = "output_segments"
# split_audio_by_speaker(audio_file, rttm_file, output_folder)

process_folder(audio_folder, rttm_folder, output_dir)
