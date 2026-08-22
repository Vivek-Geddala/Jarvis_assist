import random
import threading
import time

from Components.automation import (
    close_app,
    open_app,
    open_website,
    send_whatsapp_message,
    system_control,
    write_note,
)
from Components.speech import listen, speak
from Components.wakeword import is_wake_word
from brain import get_ai_response
from ui.signals import signals

# AI lock prevents overlapping model requests.
ai_lock = threading.Lock()


def run():
    while True:
        try:
            wake_detected = is_wake_word()
        except Exception as e:
            print(f"Wake word error: {e}")
            speak("Wake word is not configured correctly.")
            signals.hide_orb.emit()
            return

        if not wake_detected:
            continue

        signals.show_orb.emit()
        signals.set_listening.emit()

        responses = [
            "Yes?",
            "I'm listening.",
            "Tell me what you need.",
            "How can I help you?",
        ]

        speak(random.choice(responses))

        command = listen()

        if not command:
            speak("I didn't catch that.")
            signals.hide_orb.emit()
            continue

        if command.strip() in ["exit", "quit", "stop"]:
            speak("Goodbye.")
            signals.hide_orb.emit()
            signals.quit_app.emit()
            return

        if "open" in command:
            if any(word in command for word in ["youtube", "linkedin", "google"]):
                open_website(command)
            else:
                open_app(command)
        elif "close" in command:
            close_app(command)
        elif "send" in command and "to" in command:
            send_whatsapp_message(command)
        elif any(word in command for word in ["shutdown", "restart", "sleep"]):
            system_control(command)
        elif "write note" in command:
            write_note(command)
        else:
            if ai_lock.locked():
                speak("Please wait, I am thinking.")
            else:
                with ai_lock:
                    ai_reply = get_ai_response(command)
                speak(ai_reply)

        speak("Done.")
        signals.set_idle.emit()
        signals.hide_orb.emit()
