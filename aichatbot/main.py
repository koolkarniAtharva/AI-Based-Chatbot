import time
import openai
import speech_recognition as sr
import os
import webbrowser
import pyttsx3
import datetime
import random
from config import apikey

engine = pyttsx3.init()

chatStr = ""


def say(text):
    engine.say(text)
    engine.runAndWait()


def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "

    retry_count = 3
    for _ in range(retry_count):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis, an AI assistant."},
                    {"role": "user", "content": query},
                ],
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            ai_response = response['choices'][0]['message']['content']
            say(ai_response)
            chatStr += f"{ai_response}\n"
            return ai_response
        except openai.error.RateLimitError:
            time.sleep(10)
    print("Rate limit exceeded. Please try again later.")
    return "I'm currently unable to process your request due to high demand. Please try again later."


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    retry_count = 3
    for _ in range(retry_count):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis, an AI assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            ai_response = response['choices'][0]['message']['content']
            text += ai_response
            if not os.path.exists("Openai"):
                os.mkdir("Openai")
            with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
                f.write(text)
            return ai_response
        except openai.error.RateLimitError:
            time.sleep(10)
    print("Rate limit exceeded. Please try again later.")
    return "I'm currently unable to process your request due to high demand. Please try again later."


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


if __name__ == '__main__':
    say("Jarvis A.I")

    while True:
        query = takeCommand()

        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "open music" in query:
            musicPath = "path_to_your_music_file.mp3"
            os.system(f"start {musicPath}")

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes.")

        elif "open facetime".lower() in query.lower():
            os.system(f"start Facetime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"start Passky.app")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            chat(query)
