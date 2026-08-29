import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
import subprocess
import sys
import requests
import time
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import json

recognizer = sr.Recognizer()
engine = pyttsx3.init()

MICROPHONE_INDEX = 1
load_dotenv()

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

with open("config.json", "r") as file:
    config = json.load(file)

custom_commands = config.get("custom_commands", {})




def speak(text):
    print("Assistant:", text)

    speech_code = """
import pyttsx3
import sys

engine = pyttsx3.init("sapi5")
engine.say(sys.argv[1])
engine.runAndWait()
engine.stop()
"""

    subprocess.run(
        [sys.executable, "-c", speech_code, text],
        check=False
    )


# Calibrate once
print("Calibrating microphone...")

with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("Microphone ready!")


def listen():
    with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
        print("\nListening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=5
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:
        command = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("You:", command)
        return command.lower()

    except sr.UnknownValueError:
        print("I couldn't understand that.")
        return ""

    except sr.RequestError as error:
        print("Speech recognition error:", error)
        return ""


def get_weather(city):
    try:
        url = "https://wttr.in/" + city.replace(" ", "+") + "?format=j1"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "Sorry, I could not get the weather right now."

        data = response.json()
        current = data["current_condition"][0]

        temperature = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        description = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]

        return (
            f"The weather in {city} is {description}. "
            f"The temperature is {temperature} degrees Celsius, "
            f"and it feels like {feels_like} degrees. "
            f"The humidity is {humidity} percent."
        )

    except Exception:
        return "Sorry, I could not get the weather right now."
def send_email(recipient, subject, body):
    try:
        message = EmailMessage()
        message["From"] = SMTP_USERNAME
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP("smtp.ethereal.email", 587) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)

        return True

    except Exception as error:
        print("Email error:", error)
        return False

def get_intent(command):
    if any(word in command for word in ["hello", "hi", "hey"]):
        return "greeting"

    elif "how are you" in command:
        return "how_are_you"

    elif "what is your name" in command or "what's your name" in command:
        return "name"

    elif "what time is it" in command or "tell me the time" in command:
        return "time"

    elif "what is today's date" in command or "what is the date" in command:
        return "date"

    elif "what day is it" in command or "what day is today" in command:
        return "day"

    elif "weather in" in command:
        return "weather"

    elif "send an email" in command or "send email" in command:
        return "email"

    elif "open youtube" in command:
        return "youtube"

    elif "open google" in command:
        return "google"

    elif "open notepad" in command:
        return "notepad"

    elif "open calculator" in command:
        return "calculator"

    elif "open file explorer" in command:
        return "file_explorer"

    elif "open paint" in command:
        return "paint"

    elif "open vs code" in command or "open visual studio code" in command:
        return "vs_code"

    elif "search for" in command:
        return "search"

    elif "remind me in" in command:
        return "reminder"

    elif command in ["goodbye", "exit", "stop"]:
        return "exit"
    
    elif command.startswith(("what is", "who is", "what are", "who created")):
        return "question"

    return "unknown"
def answer_question(command):
    knowledge = {
        "what is python": "Python is a high-level programming language known for being simple and easy to read.",
        "who created python": "Python was created by Guido van Rossum.",
        "what is artificial intelligence": "Artificial intelligence is the ability of computers to perform tasks that normally require human intelligence.",
        "what is machine learning": "Machine learning is a branch of artificial intelligence where computers learn patterns from data.",
        "what is html": "HTML stands for HyperText Markup Language and is used to structure web pages.",
        "what is css": "CSS stands for Cascading Style Sheets and is used to style web pages."
    }

    for question, answer in knowledge.items():
        if question in command:
            return answer

    return "Sorry, I don't know the answer to that question."



speak("Hello! I am your voice assistant. How can I help you?")


while True:

    command = listen()

    if not command:
        continue
    intent = get_intent(command)
    if intent == "greeting":
        speak("Hello! Nice to hear from you.")

    elif intent == "how_are_you":
        speak("I am doing great. Thanks for asking!")

    elif intent == "name":
        speak("My name is your voice assistant.")

    elif intent == "time":
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif intent == "date":
        current_date = datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}.")

    elif intent == "day":
        current_day = datetime.now().strftime("%A")
        speak(f"Today is {current_day}.")

    elif intent == "youtube":
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif intent == "google":
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif intent == "notepad":
        speak("Opening Notepad.")
        subprocess.Popen("notepad.exe")

    elif intent == "calculator":
        speak("Opening Calculator.")
        subprocess.Popen("calc.exe")

    elif intent == "file_explorer":
        speak("Opening File Explorer.")
        subprocess.Popen("explorer.exe")

    elif intent == "paint":
        speak("Opening Paint.")
        subprocess.Popen("mspaint.exe")

    elif intent == "vs_code":
        speak("Opening Visual Studio Code.")
        subprocess.Popen(
            r"C:\Users\Administrator\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        )

    elif intent == "weather":
        city = command.replace("weather in", "").strip()

        if city:
            speak(get_weather(city))
        else:
            speak("Please tell me the city.")

    elif intent == "reminder":
        reminder_text = command.replace("remind me in", "").strip()

        if "seconds" in reminder_text:
            number = reminder_text.replace("seconds", "").strip()

            try:
                seconds = int(number)
                speak(f"Okay. I will remind you in {seconds} seconds.")
                time.sleep(seconds)
                speak("Reminder! Your requested time is up.")
            except ValueError:
                speak("Sorry, I could not understand the number of seconds.")
        else:
            speak("Please tell me the number of seconds.")

    elif intent == "email":
        recipient = "destin.boehm@ethereal.email"

        speak("I will send the test email to the configured test account.")

        # Get subject
        while True:
            speak("What should the subject be?")
            subject = listen()

            if subject:
                break

            speak("I couldn't understand the subject. Please try again.")

        # Get message
        while True:
            speak("What should the message say?")
            body = listen()

            if body:
                break

            speak("I couldn't understand the message. Please try again.")

        # Send email
        speak("Sending the email.")

        if send_email(recipient, subject, body):
            speak("Email sent successfully.")
        else:
            speak("Sorry, I could not send the email.")


    elif intent == "search":
        search_query = command.replace("search for", "").strip()

        if search_query:
            speak(f"Searching for {search_query}.")
            webbrowser.open(
                "https://www.google.com/search?q="
                + search_query.replace(" ", "+")
            )
        else:
            speak("What would you like me to search for?")

    elif intent == "exit":
        speak("Goodbye! Have a great day.")
        break
    elif intent == "question":
        speak(answer_question(command))

    else:
        if command in custom_commands:
            target = custom_commands[command]
            speak(f"Opening {command}.")
            webbrowser.open(target)
        else:
            speak("I heard you say " + command)
