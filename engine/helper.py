import os
import re
import time


def extract_yt_term(command):
    pattern = r'play\s+(.+?)\s*on\s+youtube'

    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

def remove_words(input_string, words_to_remove):
    
    words = input_string.split()

    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    result_string = ' '.join(filtered_words)

    return result_string

def keyEvent(key_code):
    command =  f'adb shell input keyevent {key_code}'
    os.system(command)
    time.sleep(1)

def tapEvents(x, y):
    command =  f'adb shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

def adbInput(message):
    command =  f'adb shell input text "{message}"'
    os.system(command)
    time.sleep(1)

def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

def replace_spaces_with_percent_s(input_string):
    return input_string.replace(' ', '%s')