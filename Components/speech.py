import threading

import pyttsx3
import speech_recognition as sr

from ui.signals import signals


tts_lock = threading.Lock()
engine = None


def _init_engine():
    global engine

    if engine is not None:
        return engine

    try:
        engine = pyttsx3.init("sapi5")
        engine.setProperty("rate", 185)
        engine.setProperty("volume", 1)

        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)

        return engine
    except Exception as e:
        print("TTS Init Error:", e)
        engine = None
        return None


def speak(text):
    with tts_lock:
        try:
            message = str(text).strip()
            if not message:
                print("TTS Warning: empty text received")
                return

            speaker = _init_engine()
            if speaker is None:
                print("TTS Error: speech engine is unavailable")
                return

            signals.set_speaking.emit()
            print(f"Jarvis: {message}")
            speaker.say(message)
            speaker.runAndWait()
        except Exception as e:
            print("TTS Error:", e)
        finally:
            signals.set_idle.emit()


def listen():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.2
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    try:
        signals.set_listening.emit()
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
    finally:
        signals.set_idle.emit()
