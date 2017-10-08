def play_audio(speak):
    import pygame
    import mutagen.mp3
    import urllib
    import io
    import os
    import subprocess
    if len(speak) > 200:
        speak = "That's a good goal!"
    if len(speak) == 0:
        speak = "That's a good goal!"
    print(speak)
    speak = urllib.quote_plus(speak)
    print(speak)
    music_file = "google_tts.mp3"
    bash_com = "curl 'https://translate.google.com/translate_tts?ie=UTF-8&q=" + speak + "&tl=en&tk=995126.592330&client=tw-ob' -H 'user-agent: stagefright/1.2 (Linux;Android 5.0)' -H 'referer: https://translate.google.com/' > " + music_file
    print(bash_com)
    p = subprocess.Popen(bash_com, shell=True)
    (output, err) = p.communicate()

    #This makes the wait possible
    p_status = p.wait()
    if output is None:
        print("MP3 Saved")
        # pick a MP3 music file you have in the working folder
        # otherwise give the full file path
        # (try other sound file formats too)
        mp3 = mutagen.mp3.MP3(music_file)
        pygame.mixer.init(frequency=mp3.info.sample_rate)
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(10)

def run_quickstart():
    play_audio("testing testing testing")

if __name__ == '__main__':
    run_quickstart()