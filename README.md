# Chuck-a-Luck

Das klassische Würfelspiel **Chuck-a-Luck** als Python-Spiel mit grafischer Oberfläche (pygame).

Du startest mit 100 € Guthaben, setzt einen Betrag auf eine Zahl von 1 bis 6, und drei Würfel werden geworfen. Je öfter deine Zahl fällt, desto mehr gewinnst du. Ist das Guthaben aufgebraucht, ist das Spiel vorbei.

## Regeln

| Treffer (Würfel mit deiner Zahl) | Auszahlung        | Reingewinn     |
|----------------------------------|-------------------|----------------|
| 0                                | 0 €               | − Einsatz      |
| 1                                | 2 × Einsatz       | + 1 × Einsatz  |
| 2                                | 3 × Einsatz       | + 2 × Einsatz  |
| 3                                | 4 × Einsatz       | + 3 × Einsatz  |

Die Auszahlung enthält den Einsatz bereits. Das Spiel sieht fair aus, ist es aber nicht: Auf lange Sicht verliert man im Schnitt etwa **7,9 %** des Einsatzes pro Runde (Erwartungswert −17/216).

## Voraussetzungen

- Python 3 (entwickelt mit Python 3.14)
- [pygame](https://www.pygame.org/)

```bash
pip install pygame
```

## Starten

```bash
python chuck_a_luck_gui.py
```

## Bedienung

**Maus**

- **−10 / −1 / +1 / +10**: Einsatz ändern
- **Alles**: das gesamte Guthaben setzen
- **Würfel 1–6**: Tipp auswählen (der gewählte Würfel bekommt einen goldenen Rahmen)
- **Würfeln!**: Runde starten
- **Neues Spiel**: nach Spielende neu beginnen

**Tastatur**

| Taste                     | Aktion                                  |
|---------------------------|-----------------------------------------|
| Ziffern, `,` oder `.`     | Einsatz direkt eintippen                |
| Rücktaste                 | letzte Ziffer des Einsatzes löschen     |
| ← / →                     | Tipp wechseln                           |
| Leertaste / Enter         | Würfeln                                 |
| `R` / Enter (Spielende)   | Neues Spiel                             |

Rechts im Fenster zeigt der **Verlauf** die letzten 10 Runden im Format `#Runde T<Tipp>: <Wurf>  <Gewinn>`, z. B. `#3 T4: 145  +10`.

## Projektstruktur

```
Chuck-a-Luck/
├── chuck_a_luck_gui.py   # Startpunkt: öffnet das Spielfenster
├── spiellogik.py         # Spielregeln: würfeln, Treffer zählen, Auszahlung berechnen
└── gui/
    ├── __init__.py
    ├── einstellungen.py  # Fenstergröße, FPS, Animationsdauer, Farben
    ├── elemente.py       # Bausteine: Button-Klasse und Würfel-Zeichnung
    └── spiel.py          # ChuckALuckGUI: Spielzustand, Eingaben, Zeichnen, Hauptschleife
```

Die Regeln liegen getrennt von der Oberfläche in `spiellogik.py`. So lässt sich die Logik auch ohne pygame verwenden oder testen.

## Anpassen

In `spiellogik.py`:

- `START_GUTHABEN`: Startguthaben (Standard: 100 €)
- `ANZAHL_WUERFEL`: Anzahl der Würfel (Standard: 3)

In `gui/einstellungen.py`:

- `BREITE`, `HOEHE`: Fenstergröße
- `FPS`: Bildwiederholrate
- `ROLL_DAUER`: Dauer der Würfel-Animation in Millisekunden
- Farben als RGB-Werte

> Hinweis: Die GUI ist auf 3 Würfel ausgelegt. Wer `ANZAHL_WUERFEL` ändert, muss auch die Würfelanzeige in `gui/spiel.py` anpassen.
