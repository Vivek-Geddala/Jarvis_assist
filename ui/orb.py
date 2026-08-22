import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QConicalGradient, QPainter, QRadialGradient
from PySide6.QtWidgets import QApplication, QWidget


class IronOrb(QWidget):
    def __init__(self):
        super().__init__()
        self.gradient_angle = 0
        self.flow_phase = 0
        self.glow = 0
        self.direction = 1
        self.rotation = 0
        self.wave_phase = 0
        self.state = "IDLE"

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(160, 160)

        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            screen.height() - self.height() - 80,
        )

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.glow += self.direction * 2
        if self.glow > 80 or self.glow < 10:
            self.direction *= -1

        if self.state in ("LISTENING", "SPEAKING"):
            self.rotation = (self.rotation + 2) % 360
            self.wave_phase += 0.2

        self.gradient_angle = (self.gradient_angle + 0.5) % 360
        self.flow_phase += 0.02
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        center = rect.center()

        scale = 1.0 + math.sin(self.flow_phase) * 0.03
        painter.translate(center)
        painter.scale(scale, scale)
        painter.translate(-center)

        if self.state == "IDLE":
            base_color = QColor(0, 180, 255)
        elif self.state == "LISTENING":
            base_color = QColor(0, 255, 180)
        else:
            base_color = QColor(170, 0, 255)

        gradient = QConicalGradient(center, self.gradient_angle)
        gradient.setColorAt(0.0, base_color)
        gradient.setColorAt(0.4, QColor(80, 120, 255))
        gradient.setColorAt(0.7, QColor(0, 220, 255))
        gradient.setColorAt(1.0, base_color)

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, 55, 55)

        core = QRadialGradient(center, 25)
        core.setColorAt(0.0, QColor(255, 255, 255, 220))
        core.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setBrush(core)
        painter.drawEllipse(center, 25, 25)

        glow = QRadialGradient(center, 80)
        glow.setColorAt(
            0.0,
            QColor(base_color.red(), base_color.green(), base_color.blue(), 120),
        )
        glow.setColorAt(
            1.0,
            QColor(base_color.red(), base_color.green(), base_color.blue(), 0),
        )
        painter.setBrush(glow)
        painter.drawEllipse(center, 80, 80)

        painter.save()
        painter.translate(center)
        painter.rotate(self.rotation)
        painter.translate(-center)
        painter.setPen(QColor(0, 255, 255, 150))
        painter.drawEllipse(center, 65, 65)
        painter.restore()

    def set_idle(self):
        self.state = "IDLE"
        self.rotation = 0

    def set_listening(self):
        self.state = "LISTENING"

    def set_speaking(self):
        self.state = "SPEAKING"

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            QApplication.quit()

    def show_orb(self):
        self.show()

    def hide_orb(self):
        self.hide()
