#all the libraries used in this project
import asyncio
import pygame
import webbrowser
import speech_recognition as sr
from edge_tts import Communicate
from gtts import gTTS
import os
import ssl
import certifi
import datetime
import re
import google.generativeai as genai
import musiclibery  # make sure this file exists(as i creaated on my own)

# Safe SSL context for Edge TTS
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Configure with your API key(pleas use your own api key here)
genai.configure(api_key="")

# Load the correct model (flash 2.5)
model = genai.GenerativeModel("gemini-2.5-flash")

def get(text):
    """Fallback TTS using gTTS (Google)"""
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(15)

    pygame.mixer.quit()
    os.remove("temp.mp3")


async def bol_async(text):
    """Edge TTS async voice (Neural voice)"""
    tts = Communicate(text, "en-US-GuyNeural")
    await tts.save("temp.mp3", ssl=ssl_context)  # SSL fixed

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(15)

    pygame.mixer.quit()
    os.remove("temp.mp3")


def bol(text):
    """Sync wrapper for bol_async"""
    try:
        asyncio.run(bol_async(text))
    except Exception as e:
        print(f"[EdgeTTS Error] {e}\n→ Falling back to gTTS...")
        get(text)  # fallback if SSL fails


def process_command(c):
    """Process spoken commands"""
    c = c.lower()

    # Website commands
    if "open google" in c:
        webbrowser.open("https://google.com")
        bol("Opening Google, sir.")
        return
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        bol("Opening Facebook, sir.")
        return
    elif "open whatsapp" in c:
        webbrowser.open("https://web.whatsapp.com")
        bol("Opening WhatsApp, sir.")
        return
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        bol("Opening YouTube, sir.")
        return
    elif "open spotify" in c:
        webbrowser.open("https://spotify.com")
        bol("Opening Spotify, sir.")
        return

    # Music commands 
    elif c.startswith("play "):
        song = c.split(" ", 1)[1]
        if song in musiclibery.music:
            webbrowser.open(musiclibery.music[song])
            bol(f"Playing {song}, sir.")
        else:
            bol("Sorry sir, I could not find that song.")
        return  #stop here, don’t call Gemini

    # AI Chat fallback 
    else:
        bol("Let me think about that...")
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(c)
            answer = response.text

            if answer:
                clean_answer = re.sub(r"[*#`>_~]", "", answer)
                sentences = clean_answer.split(". ")
                short_answer = ". ".join(sentences[:3])
                bol(short_answer)
                print("Gemini:", clean_answer)
            else:
                bol("Sorry sir, I couldn't find an answer.")
        except Exception as e:
            print("Gemini error:", e)
            bol("Sorry sir, I faced a problem connecting to Gemini.")



if __name__ == "__main__":
 def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        bol("Good morning, sir!")
    elif hour >= 12 and hour < 18:
        bol("Good afternoon, sir!")
    else:
        bol("Good evening, sir!")
    bol("wellcome back sir ?")
    recognizer = sr.Recognizer()

    recognizer = sr.Recognizer()

    while True:
        print("Listening for wake word...")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)

            if word.lower() == "friday":
                bol("tell me sir .")
                with sr.Microphone() as source:
                    print("Jarvis activated...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    process_command(command)

        except Exception as e:
            print("Error:", e)

wishMe()            
#here i completed the code