# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
        
import io
import os
import subprocess

def run_quickstart():
    # [START vision_quickstart]
    
    # Imports the Google Cloud client library
    # [START migration_import]
    from google.cloud import vision
    from google.cloud.vision import types
    # [END migration_import]

    # Instantiates a client
    # [START migration_client]
    client = vision.ImageAnnotatorClient()
    # [END migration_client]

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'Sad.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))

    

    speak = "Wow, you look really sad! Try smiling more!"
    play_audio(speak)

    speak = "What is your number 1 goal for today?"
    play_audio(speak)

    userInput = get_user_input()
    analyzed = analyze_text(userInput)
    print(analyzed)

    quote = brainy_quotes(analyzed)

    play_audio(quote)


def brainy_quotes(text):
    import httplib2, re
    character_limit = 200
    old_text = text
    text = text.replace(" ", "+")
    html_file = "quotes.html"
    bash_com = "curl 'https://www.brainyquote.com/search_results.html?q=" + text + "&tl=en&tk=995126.592330&client=tw-ob' -H 'user-agent: stagefright/1.2 (Linux;Android 5.0)' -H 'referer: https://translate.google.com/' > " + html_file
    p = subprocess.Popen(bash_com, shell=True)
    (output, err) = p.communicate()
    #This makes the wait possible
    p_status = p.wait()
    # print(p_status)

    from bs4 import BeautifulSoup
    from random import randint
    import requests
    soup = BeautifulSoup(open(html_file), "html.parser")
    mydivs = soup.find_all("a", class_="b-qt")
    for index, div in enumerate(mydivs):
        if len(div.string) > character_limit:
            mydivs.pop(index)
    length = len(mydivs) - 1
    if length == -1:
        return "Your goal of " + old_text + " is a pretty good one!"
    print("Got quotes! We have: " + str(length) + " total quotes.")
    return mydivs[randint(0, length)].string

def play_audio(speak):
    import pygame
    import mutagen.mp3
    import urllib
    import io
    import os
    import subprocess
    if len(speak) > 200:
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

def get_user_input():
    import speech_recognition as sr
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("You said: " + r.recognize_google(audio))
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def analyze_text(text):
    # Imports the Google Cloud client library
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types
    import six
    import argparse

    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    fullEntity = ""
    if len(entities) >= 1:
        fullEntity = entities[0].name
    if len(entities) < 1:
        fullEntity = "happy"

    for index, entity in enumerate(entities):
        if index != 0:
            fullEntity = fullEntity + " " + entity.name
    
    return fullEntity


if __name__ == '__main__':
    run_quickstart()