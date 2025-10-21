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