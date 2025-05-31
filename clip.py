#!/bin/python3.12
# -*- coding: utf-8 -*-
#Version 1.01
#Original credit to Sergey Kurikalov

#REQUIRES PYPERCLIP, ROFI, AND XCLIP/XSEL

import os
import time
import struct
import subprocess
import pyperclip
import sys
import re


# Settings
CLIP_LIMIT = 200             # number of clipboard history
HISTORY_FILE = os.environ['HOME'] + '/.clipboard-history'
CLIP_FILE = os.environ['HOME'] + '/.clipboard'
STRING_LIMIT = 200
HELP = '''./mclip.py menu|daemon'''
PASTE = '''keydown Control_L
key v
keyup Control_L
'''                         # your paste key
DAEMON_DELAY = 1

def splitQuotes(item):
    returnal = []
    for i in re.split(r"(?<![\\])'", item):
        if i != '':
            returnal.append(i)
    return returnal

class ClipboardManager():
    def __init__(self):
        open(HISTORY_FILE, "a+").close()

    def daemon(self):
        with open(HISTORY_FILE, "w+") as file:
            file.write('')
        with open(HISTORY_FILE, "r") as file:
            clips = splitQuotes(file.read())
            while True:
                clip = pyperclip.paste() #clipboard item
                if clip and (not clips or clip != clips[0]): #check if clipboard item is real and that it's not the first item in storage
                    if clip in clips: #remove old item to move up, if existing
                        clips.remove(clip) 
                    clips.insert(0, clip)
                    self.write(clips[0:CLIP_LIMIT])
                time.sleep(DAEMON_DELAY)

    def menu(self):
        with open(CLIP_FILE, "w+") as file:
            file.write('')
        with open(HISTORY_FILE, "r") as file:
            clips = splitQuotes(file.read())
            for index, clip in enumerate(clips):
                clip = clip.replace('\n', ' ').replace('\\\'','\'')
                print('{}: {}'.format(index, clip))

    def copy(self, select):
        if select:
            with open(HISTORY_FILE, "r") as file:
                clips = splitQuotes(file.read())
            #clips = self.read()
            index = int(select[0:select.index(':')])
            with open(CLIP_FILE, "w+") as file:
                file.write(clips[index].replace('\\\'','\''))

    def paste(self):
        with open(CLIP_FILE, "r") as file:
            copy = file.read()
            sys.stdout.write(copy)
            if copy:
                os.system('xsel --clipboard < ' + CLIP_FILE)
                #p = subprocess.Popen(['xte'], stdin=subprocess.PIPE)
                #p.communicate(input=PASTE)

    def write(self, items):
        with open(HISTORY_FILE, 'w') as file:
            for item in items:
                #file.write("{0}{1}".format(struct.pack('>i', len(item)), item))
                file.write(item.replace("'", "\\'")+"'")


if __name__ == "__main__":
    cm = ClipboardManager()
    argv = sys.argv
    if len(argv) <= 1:
        print(HELP)
        cm.daemon()
    elif argv[1] == 'daemon':
        cm.daemon()
    elif argv[1] == 'menu' and len(argv) == 2:
        cm.menu()
    elif argv[1] == 'menu' and len(argv) > 2:
        cm.copy(argv[2])
    elif argv[1] == 'paste':
        cm.paste()
    else:
        print(HELP)
    exit(0)