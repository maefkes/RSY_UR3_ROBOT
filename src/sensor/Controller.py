############################################################
#  Controller.py
#  Diese Klasse liest Controllerbefehle aus
#  16-Jul-2025 10:35:00
############################################################
import pygame
import sys


class Controller:
    def __init__(self, deadzone=0.1):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise RuntimeError("❌ Kein Joystick / Gamepad gefunden.")
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.deadzone = deadzone
        
        # Entprellungs-Timeout (in Sekunden)
        self.last_button_press_time = 0
        self.button_debounce_time = 0.3  # 300 ms Entprellungszeit

        print("🎮 Controller initialisiert:")
        print("Anzahl der Achsen:", self.joystick.get_numaxes())
        print("Anzahl der Buttons:", self.joystick.get_numbuttons())

    def get_axes(self):
        """
        Gibt die normalisierten Achsenwerte als Dictionary zurück.
        Keys: 'x', 'y', 'rx', 'ry'
        """
        pygame.event.pump()
        x = self._apply_deadzone(self.joystick.get_axis(0))
        y = self._apply_deadzone(self.joystick.get_axis(1))
        rx = self._apply_deadzone(self.joystick.get_axis(2))
        ry = self._apply_deadzone(self.joystick.get_axis(4))
        return {'x': x, 'y': y, 'rx': rx, 'ry': ry}

    def get_buttons(self):
        """
        Gibt eine Liste der aktuellen Button-Status zurück (True / False).
        """
        pygame.event.pump()
        return [bool(self.joystick.get_button(i)) for i in range(self.joystick.get_numbuttons())]

    def _apply_deadzone(self, value):
        if abs(value) < self.deadzone:
            return 0.0
        return value

    def close(self):
        pygame.quit()

