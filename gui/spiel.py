"""Das Chuck-a-luck-Fenster: Spielzustand, Eingaben und Zeichnen."""

import random

import pygame

from spiellogik import (
    START_GUTHABEN,
    wuerfeln,
    treffer_zaehlen,
    auszahlung_berechnen,
)
from gui.einstellungen import (
    BREITE, HOEHE, FPS, ROLL_DAUER,
    HINTERGRUND, TISCH_RAND, WEISS, SCHWARZ, GOLD, ROT, GRUEN_HELL, GRAU,
)
from gui.elemente import Button, wuerfel_zeichnen


class ChuckALuckGUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chuck-a-luck")
        self.fenster = pygame.display.set_mode((BREITE, HOEHE))
        self.uhr = pygame.time.Clock()

        self.schrift_gross = pygame.font.SysFont("dejavusans", 40, bold=True)
        self.schrift = pygame.font.SysFont("dejavusans", 24)
        self.schrift_klein = pygame.font.SysFont("dejavusans", 18)

        # Buttons für den Einsatz
        self.btn_minus10 = Button((60, 200, 70, 44), "-10")
        self.btn_minus1 = Button((140, 200, 60, 44), "-1")
        self.btn_plus1 = Button((360, 200, 60, 44), "+1")
        self.btn_plus10 = Button((430, 200, 70, 44), "+10")
        self.btn_allin = Button((510, 200, 110, 44), "Alles")
        self.einsatz_buttons = [
            (self.btn_minus10, -10), (self.btn_minus1, -1),
            (self.btn_plus1, 1), (self.btn_plus10, 10),
        ]

        # Die sechs Tipp-Würfel
        self.tipp_rects = [pygame.Rect(60 + i * 95, 300, 70, 70) for i in range(6)]

        self.btn_wuerfeln = Button((60, 400, 250, 60), "Würfeln!")
        self.btn_neu = Button((BREITE // 2 - 125, 470, 250, 60), "Neues Spiel")

        self.neues_spiel()

    # ---------------- Spielzustand ----------------

    def neues_spiel(self):
        self.guthaben = START_GUTHABEN
        self.einsatz_text = "10"
        self.tipp = None
        self.runden = 0
        self.wuerfel = [1, 1, 1]
        self.letztes_ergebnis = None   # Text + Farbe der letzten Runde
        self.verlauf = []              # letzte Runden (für die Liste rechts)
        self.rollt = False
        self.roll_start = 0
        self.spielende = False
        self.meldung = ""

    def einsatz(self):
        """Wandelt den eingegebenen Text in eine Zahl um (oder None)."""
        try:
            return float(self.einsatz_text.replace(",", "."))
        except ValueError:
            return None

    def einsatz_setzen(self, wert):
        wert = max(0, min(wert, self.guthaben))
        # Ganze Zahlen ohne Nachkommastellen anzeigen
        if wert == int(wert):
            self.einsatz_text = str(int(wert))
        else:
            self.einsatz_text = f"{wert:.2f}".replace(".", ",")

    def eingabe_pruefen(self):
        """Prüft Einsatz und Tipp, gibt eine Fehlermeldung oder '' zurück."""
        einsatz = self.einsatz()
        if einsatz is None:
            return "Ungültiger Einsatz – bitte eine Zahl eingeben."
        if einsatz <= 0:
            return "Der Einsatz muss größer als 0 sein."
        if einsatz > self.guthaben + 1e-9:
            return "So viel Guthaben hast du nicht."
        if self.tipp is None:
            return "Bitte wähle einen Tipp (1 bis 6)."
        return ""

    def wurf_starten(self):
        if self.rollt or self.spielende:
            return
        self.meldung = self.eingabe_pruefen()
        if self.meldung:
            return
        self.rollt = True
        self.roll_start = pygame.time.get_ticks()
        self.letztes_ergebnis = None

    def wurf_auswerten(self):
        """Wird nach der Animation aufgerufen – nutzt die Logik aus spiellogik.py."""
        einsatz = self.einsatz()
        self.wuerfel = wuerfeln()
        treffer = treffer_zaehlen(self.wuerfel, self.tipp)
        auszahlung = auszahlung_berechnen(einsatz, treffer)
        gewinn = auszahlung - einsatz

        self.guthaben = self.guthaben - einsatz + auszahlung
        self.runden += 1

        if treffer == 0:
            text = f"Kein Treffer – {einsatz:.2f} € verloren."
            farbe = ROT
        else:
            text = (f"{treffer} Treffer! Auszahlung {auszahlung:.2f} € "
                    f"(+{gewinn:.2f} €)")
            farbe = GRUEN_HELL
        self.letztes_ergebnis = (text, farbe)

        self.verlauf.insert(0, (self.runden, list(self.wuerfel), self.tipp, gewinn))
        self.verlauf = self.verlauf[:10]

        # Einsatz anpassen, falls er jetzt zu hoch ist
        if einsatz > self.guthaben:
            self.einsatz_setzen(self.guthaben)

        if self.guthaben <= 0:
            self.spielende = True

    # ---------------- Eingaben ----------------

    def ereignis(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.klick(e.pos)
        elif e.type == pygame.KEYDOWN:
            self.taste(e)

    def klick(self, pos):
        if self.spielende:
            if self.btn_neu.geklickt(pos):
                self.neues_spiel()
            return
        if self.rollt:
            return

        for btn, delta in self.einsatz_buttons:
            if btn.geklickt(pos):
                self.einsatz_setzen((self.einsatz() or 0) + delta)
                self.meldung = ""
        if self.btn_allin.geklickt(pos):
            self.einsatz_setzen(self.guthaben)
        for i, rect in enumerate(self.tipp_rects):
            if rect.collidepoint(pos):
                self.tipp = i + 1
                self.meldung = ""
        if self.btn_wuerfeln.geklickt(pos):
            self.wurf_starten()

    def taste(self, e):
        if self.spielende:
            if e.key in (pygame.K_r, pygame.K_RETURN):
                self.neues_spiel()
            return
        if self.rollt:
            return

        if e.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
            self.wurf_starten()
        elif e.key == pygame.K_BACKSPACE:
            self.einsatz_text = self.einsatz_text[:-1]
        elif e.key in (pygame.K_LEFT, pygame.K_RIGHT):
            # Pfeiltasten wechseln den Tipp
            start = self.tipp or (0 if e.key == pygame.K_RIGHT else 7)
            schritt = 1 if e.key == pygame.K_RIGHT else -1
            self.tipp = min(6, max(1, start + schritt))
        elif e.unicode and (e.unicode.isdigit() or e.unicode in ",."):
            if len(self.einsatz_text) < 8:
                self.einsatz_text += e.unicode
            self.meldung = ""

    # ---------------- Zeichnen ----------------

    def text(self, inhalt, pos, schrift=None, farbe=WEISS, mitte=False):
        schrift = schrift or self.schrift
        bild = schrift.render(inhalt, True, farbe)
        rect = bild.get_rect(center=pos) if mitte else bild.get_rect(topleft=pos)
        self.fenster.blit(bild, rect)

    def zeichnen(self):
        f = self.fenster
        f.fill(TISCH_RAND)
        pygame.draw.rect(f, HINTERGRUND, (15, 15, BREITE - 30, HOEHE - 30),
                         border_radius=25)

        # Titel und Guthaben
        self.text("Chuck-a-luck", (60, 35), self.schrift_gross, GOLD)
        self.text(f"Guthaben: {self.guthaben:.2f} €", (60, 95))
        self.text(f"Runde: {self.runden}", (400, 95), farbe=GRAU)
        bilanz = self.guthaben - START_GUTHABEN
        self.text(f"Bilanz: {bilanz:+.2f} €", (60, 125), self.schrift_klein,
                  GRUEN_HELL if bilanz >= 0 else ROT)

        # Einsatz
        self.text("Einsatz:", (60, 168), self.schrift_klein, GRAU)
        feld = pygame.Rect(210, 200, 140, 44)
        pygame.draw.rect(f, WEISS, feld, border_radius=8)
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 and not self.rollt else ""
        self.text(self.einsatz_text + cursor + " €", feld.center,
                  self.schrift, SCHWARZ, mitte=True)
        for btn, _ in self.einsatz_buttons:
            btn.aktiv = not self.rollt and not self.spielende
            btn.zeichnen(f, self.schrift)
        self.btn_allin.aktiv = not self.rollt and not self.spielende
        self.btn_allin.zeichnen(f, self.schrift)

        # Tipp-Auswahl
        self.text("Dein Tipp:", (60, 268), self.schrift_klein, GRAU)
        for i, rect in enumerate(self.tipp_rects):
            gewaehlt = self.tipp == i + 1
            wuerfel_zeichnen(f, rect, i + 1, rahmen=GOLD if gewaehlt else None)

        # Würfeln-Button und Meldung
        self.btn_wuerfeln.aktiv = not self.rollt and not self.spielende
        self.btn_wuerfeln.zeichnen(f, self.schrift)
        if self.meldung:
            self.text(self.meldung, (330, 420), self.schrift_klein, ROT)

        # Die drei geworfenen Würfel
        if self.rollt:
            vergangen = pygame.time.get_ticks() - self.roll_start
            anzeige = [random.randint(1, 6) for _ in range(3)]
            wackeln = [random.randint(-6, 6) for _ in range(3)]
            if vergangen >= ROLL_DAUER:
                self.rollt = False
                self.wurf_auswerten()
                anzeige, wackeln = self.wuerfel, [0, 0, 0]
        else:
            anzeige, wackeln = self.wuerfel, [0, 0, 0]

        for i, augen in enumerate(anzeige):
            rect = pygame.Rect(60 + i * 115, 490 + wackeln[i], 90, 90)
            treffer = (not self.rollt and self.letztes_ergebnis
                       and augen == self.tipp)
            wuerfel_zeichnen(f, rect, augen, rahmen=GOLD if treffer else None,
                             augenfarbe=ROT if treffer else SCHWARZ)

        if self.letztes_ergebnis and not self.rollt:
            text, farbe = self.letztes_ergebnis
            self.text(text, (60, 465), self.schrift_klein, farbe)

        # Verlauf rechts
        x = 650
        self.text("Verlauf", (x, 35), self.schrift, GOLD)
        for zeile, (nr, wurf, tipp, gewinn) in enumerate(self.verlauf):
            y = 75 + zeile * 26
            farbe = GRUEN_HELL if gewinn > 0 else ROT
            self.text(f"#{nr} T{tipp}: {''.join(map(str, wurf))}  {gewinn:+.0f}",
                      (x, y), self.schrift_klein, farbe)

        # Spielende
        if self.spielende:
            dunkel = pygame.Surface((BREITE, HOEHE), pygame.SRCALPHA)
            dunkel.fill((0, 0, 0, 180))
            f.blit(dunkel, (0, 0))
            self.text("Spielende!", (BREITE // 2, 220), self.schrift_gross, GOLD, True)
            self.text("Dein Guthaben ist aufgebraucht.", (BREITE // 2, 290),
                      mitte=True)
            self.text(f"Gespielte Runden: {self.runden}", (BREITE // 2, 340),
                      mitte=True)
            self.text(f"Bilanz: {self.guthaben - START_GUTHABEN:+.2f} €",
                      (BREITE // 2, 380), farbe=ROT, mitte=True)
            self.btn_neu.zeichnen(f, self.schrift)

        pygame.display.flip()

    # ---------------- Hauptschleife ----------------

    def starten(self):
        laeuft = True
        while laeuft:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    laeuft = False
                else:
                    self.ereignis(e)
            self.zeichnen()
            self.uhr.tick(FPS)
        pygame.quit()
