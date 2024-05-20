from time import sleep

import simpleaudio as sa
from pydub import AudioSegment

def play_with_fade_out(file_path, fade_out_duration=3000):

    song_name = file_path.split("/")[-1].split(".")[0]
    print(f"Playing {song_name}")

    # Load the audio file
    song = AudioSegment.from_file(file_path)

    # Apply fade out effect
    fade_out_duration_ms = fade_out_duration  # fade out duration in milliseconds
    faded_song = song.fade_out(fade_out_duration_ms)

    # Export the faded song to a temporary file
    temp_path = "temp_faded_song.wav"
    faded_song.export(temp_path, format="wav")

    # Play the audio
    wave_obj = sa.WaveObject.from_wave_file(temp_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


i = 0
while True:
    with open("playlist.txt", 'r') as f:
        songs = [song.strip() for song in f.readlines()]
    print(songs)
    if len(songs) == 0:
        sleep(5)
    else:

        file_path = songs[i % len(songs)]
        # Play the song with fade out
        play_with_fade_out(file_path)

        i += 1
