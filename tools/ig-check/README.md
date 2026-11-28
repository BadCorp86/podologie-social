# ig-check – Prüfwerkzeuge für Captions und Reel-Skripte

Ausgewählt und angepasst aus dem Skill-Paket https://github.com/Jakeschincariol/instagram-agent-skill (MIT-Lizenz, siehe LICENSE), geprüft am 28.11.2026. Beide Skripte laufen offline, ohne Netzwerk und ohne Abhängigkeiten.

## Benutzen

```bash
# Caption: zeigt, was im Feed vor „... mehr“ sichtbar ist, prüft Hashtags, Emojis, Links, Suchbegriffe
python3 tools/ig-check/caption.py caption.txt --keywords "Podologe Mönchengladbach"

# Reel-Skript (ein Satz bzw. eine Einblendung pro Zeile): geschätzte Dauer und Zeitplan vor dem Rendern
python3 tools/ig-check/beats.py skript.txt --target 20
```

beats.py trifft bei der Piper-Stimme thorsten-high die echte Länge gut (Insulin-Reel: Schätzung 60,7 s, tatsächlich 59,3 s). Deshalb jedes neue Reel-Skript vor dem Rendern damit timen. Ziel laut Lernprotokoll: unter 20 s, erste Zeile unter 3 s.

## Was zählt, was man ignoriert

- caption.py: Feed-Vorschau, Hashtag-Zahl (max. 5), Emoji (muss 0 sein), Link-Warnung und Suchbegriffe gelten. Die Prüfung „ONE ASK“ erkennt nur englische Formulierungen, ihre Warnung bei deutschen Captions ignorieren.
- beats.py: Dauer, Hook über 3 s und Abschnitte über 4 s gelten. Die Hinweise zum „Loop“ (letzter Satz wiederholt ein Wort aus dem ersten) sind optional.
- Anpassungen gegenüber dem Original: Hashtags mit Umlauten werden erkannt, .de-Adressen gelten als Link.

## Bewusst NICHT übernommen
- **hookscore.py / hooks.json:** bewertet englische Hooks nach Reiz-Formeln. Im Test bekam „Nagelpilz in 3 Tagen weg“ (verbotenes Heilversprechen, HWG) die beste Note. Passt nicht zu Brand-Profil und HWG.
- **humanize.py / detect.py:** auf Englisch ausgelegt. Würde deutsche Anführungszeichen „…“ und Gedankenstriche zerstören und bewertet die fehlende Ich-Form bzw. fehlende Kurzformen in der Sie-Ansprache als „KI“.
- **Die übrigen Skills** (Stories, DMs, Kommentare, Planung): englisch und auf Creator-Wachstum zugeschnitten. Das Brand-Profil und die Säulen decken das bereits ab.
