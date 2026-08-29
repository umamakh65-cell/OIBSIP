Task 1 — Voice Assistant

Overview

This project is a Python-based voice assistant developed as part of the internship Task 1. The assistant listens to spoken commands, converts speech into text, identifies the user's intent, and performs useful actions using Python libraries and external services.

Technologies Used

- Python
- "SpeechRecognition" — captures and recognizes spoken commands
- "PyAudio" — provides microphone input
- "pyttsx3" — converts responses into speech
- "datetime" — provides the current date, time, and day
- "webbrowser" — opens websites and performs web searches
- "subprocess" — opens Windows applications
- "requests" — retrieves weather information
- "smtplib" — sends test emails through SMTP
- "python-dotenv" — loads SMTP credentials from the ".env" file
- "json" — loads custom commands from "config.json"

Features

Beginner Tier

- Captures voice input through the microphone.
- Responds to greetings such as "Hello".
- Provides the current time, date, and day.
- Performs Google searches from spoken commands.
- Handles speech that cannot be understood without crashing.
- Provides text-to-speech feedback for assistant responses.

Advanced Tier

- Uses an intent-based natural language processing layer to classify spoken commands.
- Sends test emails through SMTP using "smtplib".
- Sets timed reminders and provides an audible alert when the duration ends.
- Retrieves live weather information using a weather API.
- Answers selected general knowledge questions using a local knowledge base.
- Supports custom commands through "config.json".
- Uses a test SMTP account rather than a personal email account.

Privacy Considerations

The assistant processes several types of data while it is running:

Voice Data

The microphone captures the user's spoken command. The "SpeechRecognition" library sends the recorded speech to Google's speech recognition service for transcription when "recognize_google()" is used.

Commands

The resulting text command is processed locally by the Python program to determine the requested action. Commands are not intentionally stored as a permanent conversation history by this application.

Weather Data

When a user requests weather information, the requested city is sent to the weather service used by the application to retrieve current weather data.

Email Data

When the email feature is used, the recipient, subject, and message are transmitted through the configured SMTP test server.

Credentials

SMTP credentials are stored in a ".env" file instead of being hard-coded directly into the Python source code. The ".env" file should remain private and should not be uploaded to a public repository.

Custom Commands

Custom commands are stored locally in "config.json". The file contains the command names and their configured actions or URLs.

Security Notes

- Do not share the ".env" file publicly.
- Do not commit SMTP passwords or other credentials to GitHub.
- A test/dummy SMTP account is used for email testing.
- API credentials should be stored securely rather than directly in source code.

Example Voice Commands

Hello
What time is it?
What is today's date?
What day is it?
Open YouTube
Open Google
Open Notepad
Open Calculator
Open File Explorer
Open Paint
Open VS Code
Search for Python tutorials
Weather in Karachi
Remind me in 10 seconds
Send an email
What is Python?
Who created Python?
Open GitHub
Goodbye

Project Structure

Task01_voice_assistant/
│
├── assistant.py
├── config.json
├── .env
├── README.md
└── venv/

Conclusion

This project implements the Beginner and Advanced requirements for the internship Voice Assistant task, including voice recognition, text-to-speech, intent handling, web search, application launching, weather information, reminders, test email sending, general knowledge responses, configurable custom commands, and privacy documentation.