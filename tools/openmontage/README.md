# Videos mit OpenMontage (HyperFrames)

Seit 25.11.2026 werden alle Reels und Videos für @podologie.moenchengladbach und den YouTube-Kanal mit OpenMontage produziert (Wunsch von Sergej). Gewählt: Render-Engine HyperFrames, maßgeschneiderte Gestaltung (Atelier-Modus), Stimme Piper de_DE-thorsten-high, keine Hintergrundmusik (Pixabay/Musik-APIs aus der Cloud-Umgebung nicht erreichbar).

## Einrichtung (einmal pro Umgebung)

```bash
git clone --depth 1 https://github.com/OpenMontageInc/OpenMontage.git
cd OpenMontage && make setup            # Python-venv, Remotion, Piper, HyperFrames
npx hyperframes doctor                  # Chrome muss gefunden werden
```

Stimme: Piper-Modell `vits-piper-de_DE-thorsten-high` (GitHub-Release von k2-fsa/sherpa-onnx, tts-models), Schriften Bricolage Grotesque und Kalam aus github.com/google/fonts, GSAP lokal per `npm pack gsap@3.14.2`.

## Dateien

- `illustrations.py` – Comic-Zeichnungen (Füße, Zelle, Schlüssel, Glukose …) und Story-Folien-Layout
- `reels_build.py` – Sprechertexte, Szenenfolge, Piper-Sprachausgabe pro Satz
- `om_build.py` – baut je Reel ein HyperFrames-Projekt (`projects/<reel>/hyperframes/index.html`) mit animierten SVG-Elementen und Wort-für-Wort-Untertiteln

## Ablauf

1. `python3 reels_build.py <reel>` erzeugt die Sprachaufnahmen (und Stand-Frames als Vorschau).
2. `python3 om_build.py <reel>` baut das HyperFrames-Projekt.
3. `npx hyperframes lint <projekt>` (0 Fehler), `npx hyperframes snapshot <projekt> --at <Zeiten>` ansehen.
4. `npx hyperframes render <projekt> -o <ausgabe>.mp4`.

Neue Themen: Szene in `reels_build.py` (Texte) und eine Szenen-Funktion `sc_<name>` mit Animationen in `om_build.py` ergänzen.
