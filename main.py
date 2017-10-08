from flask import Flask
app = Flask(__name__)

import pygame
import mutagen.mp3
import urllib
import io
import os
import requests
import subprocess
import httplib2, re
from analyze_image import analyze_image
from analyze_text import analyze_text
from get_quotes import get_quotes
from get_input import get_input
from play_audio import play_audio

def hello_world():
    speak = "Wow, you look really sad! Try smiling more!"
    play_audio(speak)

    speak = "What is your number 1 goal for today?"
    play_audio(speak)

    userInput = get_input()
    analyzed = analyze_text(userInput)

    quote = get_quotes(analyzed)

    play_audio(quote)

def run_quickstart():
    hello_world()

if __name__ == '__main__':
    run_quickstart()