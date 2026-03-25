import random
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


def run():
    while True:
        is_wake_word()
        signals.show_orb.emit()

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
            ai_reply = get_ai_response(command)
            time.sleep(1)
            speak(ai_reply)

        speak("Done.")
        signals.hide_orb.emit()
