import sys
import threading

from PySide6.QtCore import QTimer
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
    orb = IronOrb()
    orb.hide()

    signals.show_orb.connect(queue_orb_action(orb.show_orb))
    signals.hide_orb.connect(queue_orb_action(orb.hide_orb))
    signals.quit_app.connect(app.quit)

    assistant_thread = threading.Thread(target=run_assistant, daemon=True)
    assistant_thread.start()

    try:
        return app.exec()   # ✅ return instead of sys.exit here
    except KeyboardInterrupt:
        print("Exiting program...")
        app.quit()


if __name__ == "__main__":
    sys.exit(main())