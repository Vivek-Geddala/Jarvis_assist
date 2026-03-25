from PySide6.QtCore import QObject, Signal


class AssistantSignals(QObject):
    show_orb = Signal()
    hide_orb = Signal()
    quit_app = Signal()


signals = AssistantSignals()
