import subprocess
import os
import openai
import hashlib
import json
import argparse
import sys
from tqdm import tqdm
import argcomplete  # Import argcomplete for autocomplete support

def parse_arguments():
    parser = argparse.ArgumentParser(description="""This script processes audio files to generate transcriptions by segmenting the audio, transcribing the segments, and then concatenating the transcriptions.\n\nTo enable autocomplete in your shell, follow these instructions:\n\n- For bash, add:\n  eval "$(register-python-argcomplete transcript.py)"\n  to your .bashrc.\n\n- For zsh, add:\n  eval "$(register-python-argcomplete transcript.py)"\n  to your .zshrc.\n\n- For PowerShell, add:\n  Import-Module <path to argcomplete module>\n  to your profile.""")
    parser.add_argument('--source_audio_file', type=str, help='Absolute or relative path to the source audio file that you want to transcribe.', required=True)
    parser.add_argument('--audio_segment_dir', type=str, default='segmented_audio', help='Path to the directory where audio segments will be stored.\nDefaults to a folder named "segmented_audio" in the current directory.')
    parser.add_argument('--overlap_duration', type=int, default=30, help='Duration in seconds of how much each audio segment should overlap with the next one.\nHelps in ensuring continuity in transcriptions.\nDefaults to 30 seconds.')
    parser.add_argument('--segment_duration', type=int, default=300, help='Total duration in seconds for each audio segment, including the overlap duration.\nFor example, with a default of 300 seconds and an overlap of 30 seconds, each segment will be 5 minutes long with the last 30 seconds repeated in the next segment.\nDefaults to 300 seconds.')
    parser.add_argument('--remove_silences', action='store_true', default=True, help='Enables the removal of silences from the audio file before processing.\nDefaults to True.')
    parser.add_argument('--remove_silences_threshold', type=int, default=0.5, help='Duration in seconds of the silence threshold for removal.\nSilences longer than this threshold will be reduced to the threshold duration.\nDefaults to 2 seconds.')
    parser.add_argument('--audio_speed', type=float, default=1.0, help='Speed at which the audio will be played back for transcription.\nDefaults to 1x speed.\nBased on initial testing, speeds greater than 2x are not recommended as they may compromise transcription accuracy.')
    parser.add_argument('--test', action='store_true', help='Enables test mode to process a limited number of audio chunks, useful for quick checks.')
    parser.add_argument('--test_chunks', type=int, default=7, help='Specifies the number of audio chunks to process in test mode.\nOnly effective if --test is enabled.\nDefaults to 7 chunks.')
    parser.add_argument('--verbose', action='store_true', help='Enables verbose output, providing detailed logs of the script\'s operations.\nUseful for debugging or understanding the script\'s progress.')
    parser.add_argument('--openai_api_key', type=str, help='Your OpenAI API key required for accessing the transcription service.\nThis is not stored and is only used for the duration of the script execution.')
    parser.add_argument('--output_file', type=str, help='Filename for saving the final transcript.\nIf not provided, the transcript will be printed to the console.', required=False)
    argcomplete.autocomplete(parser)  # Enable autocomplete with argcomplete
    return parser.parse_args()

def generate_file_hash(file_path):
    """Generate MD5 hash of a file's contents."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def remove_silences_from_audio(source_file, threshold):
    """Optimize audio by reducing background noise and enhancing speech clarity."""
    print(f"Optimizing audio with threshold {threshold} seconds for speech clarity")
    temp_file = f"{source_file}.optimized.mp3"
    
    # Use ffmpeg to reduce background noise and enhance speech
    noise_reduction_cmd = f"ffmpeg -y -i \"{source_file}\" -af \"highpass=f=200,lowpass=f=3000\" \"{temp_file}\" -hide_banner -loglevel error"
    subprocess.call(noise_reduction_cmd, shell=True)


    print(f"Removing silences from audio with threshold {threshold} seconds")
    # Adjust the command to remove silences greater than the specified threshold completely
    silence_remove_cmd = f"ffmpeg -y -i \"{temp_file}\" -af silenceremove=stop_periods=-1:stop_duration={threshold}:stop_threshold=-30dB -ar 44100 \"{temp_file}.nosilence.mp3\" -hide_banner -loglevel error"
    subprocess.call(silence_remove_cmd, shell=True)
    # Check if the target file exists and remove it before renaming
    if os.path.exists(temp_file):
        os.remove(temp_file)
    # Replace the original file with the processed one
    os.rename(f"{temp_file}.nosilence.mp3", temp_file)
    return temp_file

def adjust_audio_speed(source_file, speed):
    """Adjust the playback speed of the audio file with reduced verbosity."""
    print(f"Adjusting audio speed to {speed}x")
    if speed == 1.0:  # No need to adjust if speed is 1x
        return source_file
    adjusted_file = f"{source_file}.adjusted.mp3"
    # Adjust audio speed with overwrite without prompt and reduced verbosity
    adjust_cmd = f"ffmpeg -y -i \"{source_file}\" -filter:a \"atempo={speed}\" -vn \"{adjusted_file}\" -hide_banner -loglevel error"
    subprocess.call(adjust_cmd, shell=True)
    return adjusted_file

def segment_audio_with_overlap(source_file, segment_dir, segment_duration, overlap_duration, remove_silences, remove_silences_threshold, audio_speed, verbose=False):
    if remove_silences:
        source_file = remove_silences_from_audio(source_file, remove_silences_threshold)
    source_file = adjust_audio_speed(source_file, audio_speed)
    if not os.path.exists(segment_dir):
        os.makedirs(segment_dir)
    segment_cmd = f"ffmpeg -i \"{source_file}\" -f segment -segment_time {segment_duration - overlap_duration} -c copy -reset_timestamps 1 -map 0 \"{segment_dir}/segment_%03d.mp3\""
    if verbose:
        print(f"Segmenting audio with command: {segment_cmd}")
    subprocess.call(segment_cmd, shell=True)
    # if remove_silences:
    #     os.remove(source_file)  # Clean up temporary file

def transcribe_audio(file_path, openai_api_key, verbose=False):
    file_hash = generate_file_hash(file_path)
    transcript_cache_file = f"{file_path}.{file_hash}.cache"
    if os.path.exists(transcript_cache_file):
        with open(transcript_cache_file, 'r') as cache_file:
            return cache_file.read()
    else:
        client = openai.OpenAI(api_key=openai_api_key)
        with open(file_path, 'rb') as audio_file:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        transcript = transcript_response.text
        with open(transcript_cache_file, 'w') as cache_file:
            cache_file.write(transcript)
        if verbose:
            print(f"Transcribed: {file_path}")
        return transcript

def match_and_concatenate(transcripts, overlap_duration):
    full_transcript = transcripts[0]
    for i in range(1, len(transcripts)):
        previous_text = transcripts[i-1].split()
        current_text = transcripts[i].split()
        
        overlap = set(previous_text[-(overlap_duration*10):]) & set(current_text[:overlap_duration*10])
        if len(overlap) > overlap_duration * 3:
            overlap_index = next((j for j, word in enumerate(current_text) if word in overlap), 0)
            full_transcript += ' ' + ' '.join(current_text[overlap_index:])
        else:
            full_transcript += ' ' + ' '.join(current_text)
    return full_transcript

def main():
    args = parse_arguments()
    openai_api_key = args.openai_api_key if args.openai_api_key else os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        sys.exit('Error: OPENAI_API_KEY environment variable not set or not passed as an argument.')
    
    segment_audio_with_overlap(source_file=args.source_audio_file, segment_dir=args.audio_segment_dir, segment_duration=args.segment_duration, overlap_duration=args.overlap_duration, remove_silences=args.remove_silences, remove_silences_threshold=args.remove_silences_threshold, audio_speed=args.audio_speed, verbose=args.verbose)
    transcripts = []
    segment_files = sorted([file for file in os.listdir(args.audio_segment_dir) if file.endswith('.mp3')])
    if args.test:
        segment_files = segment_files[:args.test_chunks]
    for segment_file in tqdm(segment_files, desc="Transcribing segments"):
        transcript = transcribe_audio(os.path.join(args.audio_segment_dir, segment_file), openai_api_key, args.verbose)
        transcripts.append(transcript)
    full_transcript = match_and_concatenate(transcripts, args.overlap_duration)
    
    output_file_name = args.output_file if args.output_file else args.source_audio_file.rsplit('.', 1)[0] + '.txt'
    if args.verbose:
        print(full_transcript)
    else:
        with open(output_file_name, 'w') as f:
            f.write(full_transcript)

if __name__ == "__main__":
    main()