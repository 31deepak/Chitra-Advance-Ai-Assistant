import os
import shlex
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
import pyautogui
import eel
import sounddevice as sd
import pyaudio  # Uncommented for hotword detection
import pvporcupine
from playsound import playsound
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words
import pywhatkit as kit
from hugchat import hugchat
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":0"

# Database Connection
conn = sqlite3.connect("chitar.db")
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.mp3"
    try:
        playsound(music_dir)
    except Exception as e:
        print(f"Error playing sound: {e}")

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()

    if query:
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (query,))
            result = cursor.fetchone()

            if result:
                speak(f"Opening {query}")
                os.startfile(result[0])
            else:
                cursor.execute('SELECT url FROM web_command WHERE name = ?', (query,))
                result = cursor.fetchone()
                
                if result:
                    speak(f"Opening {query}")
                    webbrowser.open(result[0])
                else:
                    speak(f"Trying to open {query}")
                    try:
                        os.system(f'start {query}')
                    except Exception as e:
                        speak(f"Could not open {query}. Error: {e}")
        except Exception as e:
            speak(f"An error occurred: {e}")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    audio_stream = None
    paud = None
    try:
        porcupine = pvporcupine.create(keywords=["chitra", "alexa"]) 
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("Hotword detected")

                pyautogui.hotkey("win", "j")
                time.sleep(2)
                
    except Exception as e:
        print(f"Error in hotword detection: {e}")
    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
        result = cursor.fetchone()
        
        if result:
            mobile_number = str(result[0])
            if not mobile_number.startswith('+91'):
                mobile_number = '+91' + mobile_number
            return mobile_number, query
        else:
            speak("Contact not found")
            return None, None
    except Exception as e:
        speak(f"Error fetching contact: {e}")
        return None, None

def whatsApp(mobile_no, message, flag, name):
    target_tab = {'message': 12, 'call': 7, 'video': 6}.get(flag, 6)
    speak_msg = f"{flag}ing {name}" if flag else f"Starting video call with {name}"

    encoded_message = shlex.quote(message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    subprocess.Popen(f'start "" "{whatsapp_url}"', shell=True)
    
    time.sleep(5)
    subprocess.Popen(f'start "" "{whatsapp_url}"', shell=True)

    pyautogui.hotkey('ctrl', 'f')
    for _ in range(1, target_tab):
        pyautogui.press('tab')
    pyautogui.press('enter')

    speak(speak_msg)

def chatBot(query):
    try:
        chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
        conversation_id = chatbot.new_conversation()
        chatbot.change_conversation(conversation_id)
        response = chatbot.chat(query.lower())
        print(response)
        speak(response)
        return response
    except Exception as e:
        print(f"Chatbot error: {e}")
        return "Sorry, I couldn't process that request."

def makeCall(name, mobile_no):
    mobile_no = mobile_no.replace(" ", "")
    speak(f"Calling {name}")
    command = f'adb shell am start -a android.intent.action.DIAL -d tel:{mobile_no}'
    os.system(command)

def sendMessage(message, mobile_no, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput

    message = replace_spaces_with_percent_s(message)
    mobile_no = replace_spaces_with_percent_s(mobile_no)

    speak("Sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    tapEvents(136, 2220)  # Open SMS app
    tapEvents(819, 2192)  # Start chat
    adbInput(mobile_no)
    tapEvents(601, 574)  # Tap on contact
    tapEvents(390, 2270)  # Tap on input field
    adbInput(message)
    tapEvents(957, 1397)  # Send message

    speak(f"Message sent successfully to {name}")
