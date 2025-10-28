# RSY - Rubik's Cube with 2 UR3e
## Gruppenmitglieder
- Marvin Schermutzki
- Felix Barking
- Jannick Haneder
- Lars Böckenholt
- Jesse Weintritt
- Golo Tillmann
- Marc van Heynsbergen
## Aufgabenbeschreibung
Mithilfe einer Kamera und zwei UR3e soll ein Rubik's Cube gelöst werden. Der Würfel wird an eine beliebige Stelle unter die Kamera gelegt, sodass dieser zunächst lokalisiert werden kann. Anschließend müssen die Würfelseiten eindeutig bestimmt werden. Ein Lösungsalgorithmus bestimmt die zu tätigenden Züge, welche Koordiniert und von den beiden UR3e ausgeführt werden müssen.
## Teilaufgaben (Branches)
- image_recognition (LB & MvH)
- motion_control (JW)
- robot_communication (MS & FB)
- sequence_of_operations (JH)
- solution_algorithm (GT)
## Meilensteine
- [ ] **KW 45**: Erste Zwischenbesprechung zum aktuellen Stand der Branches
    - Welche Branches können schon zusammengeführt werden?
    - Wo besteht weiterer Zeitbedarf?
    - Sind neue Problemstellungen aufgetaucht?
- [ ] **KW 5**: Prüfung / Präsentation

## Aktueller Stand
- **Würfelerkennung** funktioniert in erster Version 
    - Würfel wird zuerst nur erkannt (inkl. Orientierung), um dann gegriffen werden zu können
    - Seitenerkennung erfolgt in Roboterhand → Roboter fährt unter konstante Position unterhalb der Kamera
- **Würfelorientierung** funktioniert in erster Version, **Dazu muss von der Steuerungsgruppe die Rotation mitübergeben werden!**
    - z.B. ```rotation = {"axis":"x", "steps": 1}```
    - String kann korrekt an Algorithmus übergeben werden
- **Lösungsalgorithmus**: ist fertig
    - gibt max 45 Züge zurück
    - gibt einen String mit Drehbefehlen zurück, z.B. ```"U' R L R2 B F L2"```

## Ein paar nützliche Git-Befehle ...
```bash
git status      # überprüft den aktuellen Status (Welche Dateien wurden geändert?)
git pull        # lädt den aktuellen Stand vom Remote-Repository herunter
git add .       # fügt alle geänderten Dateien zum nächsten Commit hinzu
git commit -m "Nachricht"   # erstellt einen Commit mit einer Nachricht (optional ergänzen)
git push        # überträgt deine Commits ins Remote-Repository
git branch      # zeigt alle lokalen Branches an und markiert den aktuellen
git branch -a   # zeigt alle lokalen und Remote-Branches an
git switch <branch-name>    # wechselt in anderen branch
```
Denkt am besten dran eine .gitignore Datei in euren lokalen Ordner zu legen, um das remote-repo nicht unnötig voll zu packen. Es gibt dafür gute Vorlagen online.
## Virtual Environment anlegen
Es ist sinnvoll mit **python virtual environments** zu arbeiten, da man so lokal Pakete installieren kann, ohne die Gefahr von Versionskonflikten mit anderen Python Projekten zu haben. Hier ein paar nützliche Befehle zur Erstellung:

```pip -m venv .venv``` erstellt ein virtual environment mit dem Namen .venv im aktuellen Ordner.

```.venv/Scripts/activate``` aktiviert das venv. Ab jetzt guckt der Python interpreter nur noch auf die in diesem venv installierten Pakete. Alles, was jetzt mit pip install installiert wird, landet lokal in dem venv.

```deactivate``` deaktiviert das venv wieder.
