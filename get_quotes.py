def get_quotes(text):
    import pygame
    import mutagen.mp3
    import urllib
    import io
    import os
    import subprocess
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

def run_quickstart():
    print(get_quotes("happy"))

if __name__ == '__main__':
    run_quickstart()