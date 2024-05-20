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

def remove_new_song_tag(file_path):
    # Remove the " NEW_SONG" tag from the given file in the playlist
    with open("playlist.txt", 'r') as f:
        songs = [song.strip() for song in f.readlines()]

    with open("playlist.txt", 'w') as f:
        for song in songs:
            if song == file_path + " NEW_SONG":
                f.write(file_path + '\n')
            else:
                f.write(song + '\n')

i = 0
while True:
    with open("playlist.txt", 'r') as f:
        songs = [song.strip() for song in f.readlines()]
    print(songs)

    if len(songs) == 0:
        sleep(5)
    else:
        # Separate new songs and regular songs
        new_songs = [song for song in songs if song.endswith(" NEW_SONG")]
        regular_songs = [song for song in songs if not song.endswith(" NEW_SONG")]
        
        if new_songs:
            # Play the first new song
            file_path = new_songs[0].replace(" NEW_SONG", "")
            play_with_fade_out(file_path)
            # Remove the " NEW_SONG" tag from the file
            remove_new_song_tag(file_path)
        else:
            # Play the next regular song
            file_path = regular_songs[i % len(regular_songs)]
            play_with_fade_out(file_path)
            i += 1