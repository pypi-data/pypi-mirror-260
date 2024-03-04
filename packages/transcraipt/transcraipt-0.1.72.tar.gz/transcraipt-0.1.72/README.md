# Audio Transcript

Audio Transcript is an advanced tool that transcribes audio files using OpenAI's API. It not only segments the audio for manageable processing but also offers features like silence removal and speed adjustment to minimies the cost of transcribing. After processing, it seamlessly concatenates the transcriptions to deliver a complete and coherent transcript of the entire audio file. Designed for high efficiency, it facilitates the rapid transcription of extensive audio files by optimizing the transcription process. It utilizes the OpenAI API for precise transcription and accommodates a wide range of audio formats.
## Installation

To get Audio Transcript up and running, you've got two straightforward options: pip install or direct setup. Pick the one that suits you best.

### Option 1: Pip Install

Fire up your terminal and run:

```
pip install audio_transcript
```

This command fetches Audio Transcript from PyPI and installs it along with all its dependencies. Easy peasy.

### Option 2: Direct Setup

Prefer to do things manually? No problem. Here's how:

First, clone the repository to your local machine:

```
git clone https://github.com/gsusI/audio_transcript.git
```

Next, dive into the cloned directory:

```
cd audio_transcript
```

And kick off the setup script:

```
python setup.py install
```

This installs all the necessary dependencies and gets the tool ready for action.

## Post-Installation Goodies

Once you've got Audio Transcript installed, you can supercharge your command-line experience with autocomplete. Just follow the on-screen instructions post-installation. They'll walk you through setting up autocomplete for bash, zsh, or PowerShell. It's a game-changer, trust me.

## Usage

To use Audio Transcript, you need to provide the source audio file and optionally specify parameters such as the directory for audio segments, segment duration, overlap duration, and the output file for the transcript. The tool comes with a command-line interface that is fully documented. To see all available options, run:

```
transcribe-audio --help
```

A typical command might look like this:

```
transcribe-audio --source_audio_file path/to/your/audio/file.mp3 --audio_segment_dir path/to/segment/dir --segment_duration 300 --overlap_duration 30 --remove_silences --remove_silences_threshold 0.5 --audio_speed 1.0 --output_file path/to/output/transcript.txt
```

To ensure the best balance between transcription speed and accuracy, it's crucial to find the optimal audio playback speed. While increasing the speed can reduce transcription time and potentially minimize costs, setting the speed too high may lead to inaccurate transcriptions or even nonsensical results. To determine the most effective speed for your audio files, follow these steps:

1. Use the `--test` and `--test_chunks` options set to `1` to transcribe only the first chunk of your audio at various speeds. This approach allows you to compare the accuracy of transcriptions at different speeds without processing the entire file.

2. Set the `--segment_duration` to a short duration, such as `30` seconds, for these tests. This ensures that the test runs quickly and focuses on a manageable portion of the audio.

3. Start by running the transcription at the default speed (`1.0x`). Use the following command as a template, adjusting the `--source_audio_file` and `--output_file` paths as necessary.

4. Once the transcription is complete, review the results and assess the accuracy of the transcription. If the results are satisfactory, you can proceed with the full transcription at the same speed. If not, you can adjust the speed and repeat the process until you find the optimal speed for your audio file.