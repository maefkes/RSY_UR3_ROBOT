# UR-Rubik's Cube: Image Recognition
## Gruppenmitglieder
- Lars Böckenholt
- Marc van Heynsbergen
## Aufgabenbeschreibung
Der Würfel muss so erkannt werden, dass der Roboter ihn greifen und lösen kann. Dafür sind folgende Teilschritte notwendig:
- Lokalisierung des Würfels
- Orientierung des Würfels ermitteln
- Farbgitter des Würfels erkennen
- Matrix für Lösungsalgorithmus erstellen
## ToDo
- [x] Würfellokalisierung
- [x] Würfelorientierung zum Greifen
- [x] Farberkennung
- [ ] Würfelorientierung für die Farben
- [ ] In Matrix umwandeln
## Anwendung
Lade die Bildpfade
```bash
image_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\Nahaufnahme\test2\*.jpg"
print("Loading images")
imgs = glob(image_path)
```

Hole die Orientierung
```bash
model_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\models\best.pt"
detector = CubeColorDetectorLive(model_path, cam_index=1) # initialisiere den Cube Color Detector

# detection aller Bilder
image1 = detector.detect_from_image(imgs[0])
image2 = detector.detect_from_image(imgs[1])
image3 = detector.detect_from_image(imgs[2])
image4 = detector.detect_from_image(imgs[3])
image5 = detector.detect_from_image(imgs[4])
image6 = detector.detect_from_image(imgs[5])

images = [image1, image2, image3, image4, image5, image6]
```

Definiere die Rotationen
```bash
rotation1 = {"axis": "x", "steps": 1}
rotation2 = {"axis": "y", "steps": 2}
rotation3 = {"axis": "x", "steps": 1}
rotation4 = {"axis": "y", "steps": 1}
rotation5 = {"axis": "y", "steps": 2}

rotations = [rotation1, rotation2, rotation3, rotation4, rotation5]
```

Ermittle die Lösungen
```bash
result = CubeOrientation.get_final_color_string(images, rotations)
```