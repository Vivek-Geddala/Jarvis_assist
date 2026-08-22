import sys
import threading

# PyAudio currently ships Windows wheels only for CPython 3.13 and earlier.
# Check this before importing modules that require it so startup errors are actionable.
if sys.version_info >= (3, 14):
    raise RuntimeError(
        "MyJarvis requires Python 3.12 or 3.13 because PyAudio is not yet "
        "available for Python 3.14 on Windows. Create the virtual environment "
        "with: py -3.12 -m venv .venv"
    )

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from Components.assistant import run as run_assistant
from ui.orb import IronOrb
from ui.signals import signals

def queue_orb_action(action):
    def wrapped():
        QTimer.singleShot(0, action)
    return wrapped


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon/myjarvisicon.ico"))
    orb = IronOrb()
    orb.hide()

    # 🔥 UI signal connections
    signals.show_orb.connect(queue_orb_action(orb.show_orb))
    signals.hide_orb.connect(queue_orb_action(orb.hide_orb))
    signals.set_idle.connect(queue_orb_action(orb.set_idle))
    signals.set_listening.connect(queue_orb_action(orb.set_listening))
    signals.set_speaking.connect(queue_orb_action(orb.set_speaking))
    signals.quit_app.connect(app.quit)

    # 🔥 Run assistant in background thread
    assistant_thread = threading.Thread(target=run_assistant, daemon=True)
    assistant_thread.start()

    try:
        return app.exec()
    except KeyboardInterrupt:
        print("Exiting program...")
        app.quit()


if __name__ == "__main__":
    sys.exit(main())
