"""Bausteine der Oberfläche: Button und Würfel-Zeichnung."""

import pygame

from gui.einstellungen import (
    WEISS, SCHWARZ, GRAU, TISCH_RAND, BUTTON, BUTTON_HOVER, BUTTON_AUS,
)


class Button:
    """Ein einfacher anklickbarer Button."""

    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.aktiv = True

    def zeichnen(self, flaeche, schrift):
        maus = pygame.mouse.get_pos()
        if not self.aktiv:
            farbe = BUTTON_AUS
        elif self.rect.collidepoint(maus):
            farbe = BUTTON_HOVER
        else:
            farbe = BUTTON
        pygame.draw.rect(flaeche, farbe, self.rect, border_radius=10)
        pygame.draw.rect(flaeche, TISCH_RAND, self.rect, 2, border_radius=10)
        text = schrift.render(self.text, True, WEISS if self.aktiv else GRAU)
        flaeche.blit(text, text.get_rect(center=self.rect.center))

    def geklickt(self, pos):
        return self.aktiv and self.rect.collidepoint(pos)


# Positionen der Augen auf einem Würfel (relativ, 0..1)
AUGEN = {
    1: [(0.5, 0.5)],
    2: [(0.25, 0.25), (0.75, 0.75)],
    3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
    4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
    5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
    6: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.5),
        (0.75, 0.5), (0.25, 0.75), (0.75, 0.75)],
}


def wuerfel_zeichnen(flaeche, rect, augenzahl, rahmen=None, augenfarbe=SCHWARZ):
    """Zeichnet einen Würfel mit der gegebenen Augenzahl in das Rechteck."""
    rect = pygame.Rect(rect)
    pygame.draw.rect(flaeche, WEISS, rect, border_radius=rect.w // 6)
    if rahmen:
        pygame.draw.rect(flaeche, rahmen, rect.inflate(8, 8), 4,
                         border_radius=rect.w // 5)
    radius = max(3, rect.w // 11)
    for fx, fy in AUGEN[augenzahl]:
        x = rect.x + int(fx * rect.w)
        y = rect.y + int(fy * rect.h)
        pygame.draw.circle(flaeche, augenfarbe, (x, y), radius)
