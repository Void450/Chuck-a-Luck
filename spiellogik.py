"""Spiellogik von Chuck-a-luck – wird von Konsole und GUI gemeinsam genutzt."""

import random


START_GUTHABEN = 100.0  # Startguthaben in €
ANZAHL_WUERFEL = 3


def wuerfeln(anzahl=ANZAHL_WUERFEL):
    """Wirft 'anzahl' Würfel und gibt die Augenzahlen als Liste zurück."""
    return [random.randint(1, 6) for _ in range(anzahl)]


def treffer_zaehlen(wuerfel, tipp):
    """Zählt, wie viele Würfel die getippte Zahl zeigen."""
    treffer = 0
    for augenzahl in wuerfel:
        if augenzahl == tipp:
            treffer = treffer + 1
    return treffer


def auszahlung_berechnen(einsatz, treffer):
    """Berechnet die Auszahlung nach den Chuck-a-luck-Regeln."""
    if treffer == 0:
        return 0.0
    return einsatz * (1 + treffer)
