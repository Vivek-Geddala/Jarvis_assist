import threading

import pyttsx3
import speech_recognition as sr


tts_lock = threading.Lock()
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 185)
engine.setProperty("volume", 1)


def speak(text):
    with tts_lock:
        try:
            print(f"Jarvis: {text}")
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("TTS Error:", e)


def listen():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.2
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(
                source,
                timeout=7,
                phrase_time_limit=8,
            )

        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.WaitTimeoutError:
        print("Listening timed out")
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except Exception as e:
        print("Listen error:", e)
        return ""
