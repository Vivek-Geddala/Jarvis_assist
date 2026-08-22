from PySide6.QtCore import QObject, Signal


class AssistantSignals(QObject):
    show_orb = Signal()
    hide_orb = Signal()
    set_idle = Signal()
    set_listening = Signal()
    set_speaking = Signal()
    quit_app = Signal()


signals = AssistantSignals()
