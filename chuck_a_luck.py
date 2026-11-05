import random
import pygame


START_GUTHABEN = 100.0  # Startguthaben in €
ANZAHL_WUERFEL = 3


# ---------------------------------------------------------------
# Eingabe-Funktionen (mit Prüfung der Eingaben)
# ---------------------------------------------------------------

def einsatz_eingeben(guthaben):
    """Fragt den Einsatz ab, bis ein gültiger Betrag eingegeben wurde.
    Gültig: Zahl > 0 und nicht größer als das aktuelle Guthaben."""
    while True:
        eingabe = input(f"Dein Einsatz in € (Guthaben: {guthaben:.2f} €): ")
        try:
            # Komma als Dezimaltrennzeichen erlauben (z. B. "2,50")
            einsatz = float(eingabe.replace(",", "."))
        except ValueError:
            print("  Ungültige Eingabe – bitte eine Zahl eingeben.")
            continue

        if einsatz <= 0:
            print("  Der Einsatz muss größer als 0 sein.")
        elif einsatz > guthaben:
            print("  So viel Guthaben hast du nicht.")
        else:
            return einsatz


def tipp_eingeben():
    """Fragt den Tipp ab, bis eine ganze Zahl von 1 bis 6 eingegeben wurde."""
    while True:
        eingabe = input("Dein Tipp (1 bis 6): ")
        try:
            tipp = int(eingabe)
        except ValueError:
            print("  Ungültige Eingabe – bitte eine ganze Zahl eingeben.")
            continue

        if 1 <= tipp <= 6:
            return tipp
        print("  Der Tipp muss zwischen 1 und 6 liegen.")


def weiterspielen():
    """Fragt, ob noch eine Runde gespielt werden soll (j/n)."""
    while True:
        antwort = input("Noch eine Runde? (j/n): ").strip().lower()
        if antwort in ("j", "ja"):
            return True
        if antwort in ("n", "nein"):
            return False
        print("  Bitte 'j' oder 'n' eingeben.")


# ---------------------------------------------------------------
# Spiellogik
# ---------------------------------------------------------------

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


# ---------------------------------------------------------------
# Ablauf einer Runde und des ganzen Spiels
# ---------------------------------------------------------------

def runde_spielen(guthaben):
    """Spielt eine Runde und gibt das neue Guthaben zurück."""
    einsatz = einsatz_eingeben(guthaben)
    tipp = tipp_eingeben()

    wuerfel = wuerfeln()
    treffer = treffer_zaehlen(wuerfel, tipp)
    auszahlung = auszahlung_berechnen(einsatz, treffer)
    gewinn = auszahlung - einsatz  # positiv = Gewinn, negativ = Verlust

    # Ergebnis ausgeben
    print()
    print(f"  Gewürfelt:  {', '.join(str(w) for w in wuerfel)}")
    print(f"  Treffer:    {treffer}")
    print(f"  Auszahlung: {auszahlung:.2f} €")
    if gewinn >= 0:
        print(f"  Gewinn:     +{gewinn:.2f} €")
    else:
        print(f"  Verlust:    {gewinn:.2f} €")

    # Einsatz wird abgezogen, Auszahlung gutgeschrieben
    guthaben = guthaben - einsatz + auszahlung
    print(f"  Neues Guthaben: {guthaben:.2f} €")
    print()
    return guthaben


def main():
    print("=" * 40)
    print("        Willkommen bei Chuck-a-luck!")
    print("=" * 40)
    print(f"Du startest mit {START_GUTHABEN:.2f} € Guthaben.\n")

    guthaben = START_GUTHABEN
    runden = 0

    while True:
        runden = runden + 1
        print(f"--- Runde {runden} ---")
        guthaben = runde_spielen(guthaben)

        if guthaben <= 0:
            print("Dein Guthaben ist aufgebraucht. Spielende!")
            break
        if not weiterspielen():
            break
        print()

    # Bilanz am Ende
    bilanz = guthaben - START_GUTHABEN
    print(f"\nGespielte Runden: {runden}")
    print(f"Endguthaben:      {guthaben:.2f} €")
    print(f"Bilanz:           {bilanz:+.2f} €")
    print("Danke fürs Spielen!")


# Programm nur starten, wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    main()
