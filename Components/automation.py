import pyautogui
import time
import psutil
import webbrowser
import subprocess
import os

from Components.speech import speak,listen
whatsapp_command = "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"


def open_app(command):
    # Extract app name
    app_name = command.replace("open", "").strip()

    if not app_name:
        speak("Please tell me which app to open.")
        return

    speak(f"Opening {app_name}")

    time.sleep(0.5)

    # Open Windows search
    pyautogui.press("win")
    time.sleep(0.5)

    # Type app name
    pyautogui.write(app_name, interval=0.05)
    time.sleep(0.7)

    # Press Enter to open
    pyautogui.press("enter")


def close_app(command):
    keyword = command.replace("close", "").strip().lower()
    app_map = {
        "youtube": "chrome",
        "chrome": "chrome",
        "notepad": "notepad",
        "whatsapp": "whatsapp",
        "hianime": "chrome"
    }
    app_name = app_map.get(keyword, keyword)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if app_name in proc.info['name'].lower():
                proc.kill()
                speak(f"{keyword} closed.")
                return
        except:
            pass
    speak(f"{keyword} is not running.")

def open_website(command):
    sites = {
        "youtube": "https://www.youtube.com",
        "linkedin": "https://www.linkedin.com",
        "google": "https://www.google.com",
        "hianime": "https://www.hianime.tv"
    }
    for key in sites:
        if key in command:
            webbrowser.open(sites[key])
            speak(f"Opening {key}.")
            return
    speak("Website not found.")

def send_whatsapp_message(command):
    try:
        # Improved parsing: "send message hello there to mom"
        parts = command.split(" to ")
        recipient_name = parts[-1].strip()
        message = parts[0].replace(
            "send message", "").replace("send", "").strip()

        speak(f"Preparing to send a message to {recipient_name}")
        # Use the specific command to open WhatsApp UWP
        subprocess.run(["explorer.exe", whatsapp_command])
        time.sleep(10)  # Give WhatsApp more time to load fully
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.write(recipient_name)
        time.sleep(2)  # Wait for search results
        pyautogui.press("down")  # Select the first result
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write(message)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "w")  # Close WhatsApp window

        speak(f"Message sent to {recipient_name}.")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        speak("Failed to send the message. Something went wrong.")


def system_control(command):
    if "shutdown" in command:
        speak("Shutting down.")
        time.sleep(1)
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting system.")
        time.sleep(1)
        os.system("shutdown /r /t 1")
    elif "sleep" in command:
        speak("Sleeping now.")
        time.sleep(1)   
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def write_note(command):
    note_content = command.replace("write note", "").strip()
    if not note_content:
        speak("Please tell me what to write in the note.")
        return
    with open("note.txt", "w") as file:
        file.write(note_content)
    speak("Note written to note.txt")
