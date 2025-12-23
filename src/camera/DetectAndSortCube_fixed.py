# file: cube_color_detector_live.py
import os
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Tuple, Optional, Dict

# BGR-Farben
COLOR_MAP = {
    'r': (0, 0, 255),
    'g': (0, 255, 0),
    'b': (255, 0, 0),
    'y': (0, 255, 255),
    'o': (0, 165, 255),
    'w': (255, 255, 255)
}

Det = Tuple[float, float, float, float, str]  # (x_c, y_c, w, h, label)


class CubeColorDetectorLive:
    """Minimal: keine Clustering-Logik. Bestimmt Reihen anhand y-centers + x-sorting.
       Speichert die letzte erfolgreiche Detection als ./last_detection/img.png (max width 1000px)."""

    def __init__(self, model_path: str, conf_threshold: float = 0.6, cam_index: int = 0):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.cam_index = cam_index
        os.makedirs("./last_detection", exist_ok=True)

    @staticmethod
    def _sort_into_rows_by_y_then_x(detections: List[Det]) -> Optional[List[List[Det]]]:
        """Aus 9 Detections: bestimme top/mid/bottom anhand y-center, dann sortiere innerhalb jeder Zeile nach x."""
        if len(detections) != 9:
            return None

        # sortiere nach y (klein -> groß). y kleiner = oberer Bildschirmbereich
        by_y = sorted(detections, key=lambda d: d[1])
        top3 = sorted(by_y[0:3], key=lambda d: d[0])
        mid3 = sorted(by_y[3:6], key=lambda d: d[0])
        bot3 = sorted(by_y[6:9], key=lambda d: d[0])

        # Reihenfolge gemäß Wunsch:
        # top3 -> 1,2,3 ; mid3 -> 4,5,6 ; bot3 -> 7,8,9
        return [top3, mid3, bot3]

    @staticmethod
    def _draw_boxes_and_grid(frame: np.ndarray, detections: List[Det], grid: List[List[Det]],
                             cell_size: int = 60, grid_pos: Tuple[int, int] = (20, 20)) -> np.ndarray:
        """Zeichnet YOLO-Boxen+Labels (BGR-Color anhand label) und das 3x3 Farb-Grid."""
        out = frame.copy()
        FONT = cv2.FONT_HERSHEY_SIMPLEX

        # YOLO boxes (colored by label)
        for (x_c, y_c, w, h, label) in detections:
            x1 = int(x_c - w / 2)
            y1 = int(y_c - h / 2)
            x2 = int(x_c + w / 2)
            y2 = int(y_c + h / 2)
            color = COLOR_MAP.get(label, (0, 255, 0))
            cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
            cv2.putText(out, label, (x1, max(y1 - 6, 12)), FONT, 0.6, color, 2)

        # Draw color grid (filled squares) at given pos
        x0, y0 = grid_pos
        border = 4
        for r in range(3):
            for c in range(3):
                lbl = grid[r][c]
                col = COLOR_MAP.get(lbl, (128, 128, 128))
                gx = x0 + c * (cell_size + border)
                gy = y0 + r * (cell_size + border)
                cv2.rectangle(out, (gx, gy), (gx + cell_size, gy + cell_size), col, -1)
                cv2.rectangle(out, (gx, gy), (gx + cell_size, gy + cell_size), (0, 0, 0), 1)
                # optional label inside square (small)
                cv2.putText(out, lbl, (gx + 6, gy + cell_size - 8), FONT, 0.6, (0, 0, 0), 2)

        return out

    @staticmethod
    def _scale_to_max_width(img: np.ndarray, max_width: int = 1000) -> np.ndarray:
        h, w = img.shape[:2]
        if w <= max_width:
            return img
        scale = max_width / w
        return cv2.resize(img, (int(w * scale), int(h * scale)))

    def _detections_from_result(self, result) -> List[Det]:
        detections: List[Det] = []
        for box in result[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            cls = int(box.cls[0])
            label = self.model.names[cls]
            w = (x2 - x1).item()
            h = (y2 - y1).item()
            x_c = (x1 + x2).item() / 2.0
            y_c = (y1 + y2).item() / 2.0
            detections.append((x_c, y_c, w, h, label))
        return detections

    def detect_from_image(self, source: str) -> Optional[Dict[str, str]]:
        img = cv2.imread(source)
        if img is None:
            print("❌ Kein gültiges Bild geladen.")
            return None

        res = self.model.predict(img, conf=self.conf_threshold, verbose=False)
        detections = self._detections_from_result(res)

        rows = self._sort_into_rows_by_y_then_x(detections)
        if rows is None:
            print("⚠️ Nicht genau 9 Detections.")
            return None

        grid_labels = [[cell[4] for cell in row] for row in rows]
        # Save visualization
        out = self._draw_boxes_and_grid(img, detections, grid_labels)
        out_scaled = self._scale_to_max_width(out, 1000)
        save_path = "./last_detection/img.png"
        cv2.imwrite(save_path, out_scaled)
        matrix = "".join("".join(r) for r in grid_labels)
        parentcolor = grid_labels[1][1]
        result = {"parentcolor": parentcolor, "matrix": matrix}
        print("💾 Detection saved:", save_path)
        print("✅ Result:", result)
        return result

    def detect_from_camera(self) -> Optional[Dict[str, str]]:
        """Versucht eine Farberkennung vom Kamerabild aus zu ermitteln."""
        cap = cv2.VideoCapture(self.cam_index)
        if not cap.isOpened():
            print("❌ Keine Kamera gefunden.")
            return None
        print("🎥 Kamera läuft (kein GUI). Warte auf 9 Detections ...")

        result: Optional[Dict[str, str]] = None
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Kein Frame empfangen.")
                break

            res = self.model.predict(source=frame, conf=self.conf_threshold, verbose=False)
            detections = self._detections_from_result(res)
            rows = self._sort_into_rows_by_y_then_x(detections)
            if rows is not None:
                grid_labels = [[cell[4] for cell in row] for row in rows]
                out = self._draw_boxes_and_grid(frame, detections, grid_labels)
                out_scaled = self._scale_to_max_width(out, 1000)
                save_path = "./last_detection/img.png"
                cv2.imwrite(save_path, out_scaled)
                matrix = "".join("".join(r) for r in grid_labels)
                parentcolor = grid_labels[1][1]
                result = {"parentcolor": parentcolor, "matrix": matrix}
                print("💾 Detection saved:", save_path)
                print("✅ Result:", result)
                break

        cap.release()
        return result


if __name__ == "__main__":
    model_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\models\best.pt"
    detector = CubeColorDetectorLive(model_path, conf_threshold=0.6, cam_index=0)
    # Beispiel mit Bild
    image_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\Nahaufnahme\test1\image1.jpg"
    result = detector.detect_from_image(image_path)
    print("📦 Endergebnis:", result)
