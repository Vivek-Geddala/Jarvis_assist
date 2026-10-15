"""Windows global hotkey used as an alternate Jarvis activation method."""

import ctypes
import threading
from ctypes import wintypes


activation_requested = threading.Event()

MOD_CONTROL = 0x0002
VK_I = 0x49
WM_HOTKEY = 0x0312
HOTKEY_ID = 1


def listen_for_hotkey():
    """Wait for Ctrl+I and signal the assistant when it is pressed."""
    if not hasattr(ctypes, "windll"):
        print("Global Ctrl+I activation is only available on Windows.")
        return

    user32 = ctypes.windll.user32
    if not user32.RegisterHotKey(None, HOTKEY_ID, MOD_CONTROL, VK_I):
        print("Could not register Ctrl+I. Another application may already use it.")
        return

    print("Press Ctrl+I to activate Jarvis.")
    message = wintypes.MSG()
    try:
        while user32.GetMessageW(ctypes.byref(message), None, 0, 0) > 0:
            if message.message == WM_HOTKEY and message.wParam == HOTKEY_ID:
                activation_requested.set()
    finally:
        user32.UnregisterHotKey(None, HOTKEY_ID)
