# file: cube_color_detector_live.py
import cv2
import numpy as np
from ultralytics import YOLO
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from collections import Counter

COLOR_MAP = {
    'r': (0, 0, 255),
    'g': (0, 255, 0),
    'b': (255, 0, 0),
    'y': (0, 255, 255),
    'o': (0, 165, 255),
    'w': (255, 255, 255)
}


class CubeColorDetectorLive:
    """Erkennt Würfelseite über Live-Kamera und gibt sie als Dictionary zurück."""

    def __init__(self, model_path: str, conf_threshold: float = 0.6, cam_index: int = 2):
        # print("Initialize model")
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.cam_index = cam_index

    def _filter_detections(self, detections, size_tolerance=0.3, eps=30, min_samples=4):
        if len(detections) < 4:
            return detections
        sizes = np.array([w * h for (_, _, w, h, _) in detections])
        median_size = np.median(sizes)
        valid = [d for d in detections if abs((d[2] * d[3]) - median_size) / median_size < size_tolerance]
        centers = np.array([(x, y) for (x, y, _, _, _) in valid])
        if len(centers) < 4:
            return valid
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(centers)
        labels = clustering.labels_
        if len(set(labels)) <= 1:
            return valid
        main_cluster = Counter(labels).most_common(1)[0][0]
        return [d for d, lbl in zip(valid, labels) if lbl == main_cluster]

    def _normalize_orientation(self, detections):
        points = np.array([(x, y) for (x, y, _, _, _) in detections])
        pca = PCA(n_components=2)
        pca.fit(points)
        angle = np.arctan2(pca.components_[0, 1], pca.components_[0, 0])
        center = np.mean(points, axis=0)
        rot = np.array([[np.cos(-angle), -np.sin(-angle)],
                        [np.sin(-angle), np.cos(-angle)]])
        rotated_pts = (points - center) @ rot.T + center
        return [(p[0], p[1], d[2], d[3], d[4]) for d, p in zip(detections, rotated_pts)]

    def _build_color_grid(self, detections_rotated):
        pts = np.array([(x, y) for (x, y, _, _, _) in detections_rotated])
        xs, ys = pts[:, 0], pts[:, 1]
        x_min, x_max = xs.min(), xs.max()
        y_min, y_max = ys.min(), ys.max()
        if (x_max - x_min) < 1 or (y_max - y_min) < 1:
            return None

        x_bins = np.linspace(x_min, x_max, 4)
        y_bins = np.linspace(y_min, y_max, 4)
        col_idxs = np.clip(np.digitize(xs, x_bins) - 1, 0, 2)
        row_idxs = np.clip(np.digitize(ys, y_bins) - 1, 0, 2)

        grid = [[None for _ in range(3)] for __ in range(3)]
        for (r, c, w, h, label), row_i, col_i in zip(detections_rotated, row_idxs, col_idxs):
            if grid[row_i][col_i] is None:
                grid[row_i][col_i] = label

        for r in range(3):
            for c in range(3):
                if grid[r][c] is None:
                    return None
        return grid

    def _process_cube_side(self, detections):
        dets = self._filter_detections(detections)
        if len(dets) != 9:
            return None
        dets_rot = self._normalize_orientation(dets)
        grid = self._build_color_grid(dets_rot)
        return grid

    def detect_from_image(self, source:str)->dict:
        """Wertet ein statisches Bild aus"""
        
        result_dict = None
        # print("get prediction from model")
        result = self.model.predict(source)

        # print("postprocessing prediction...")
        detections = []
        for box in result[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            cls = int(box.cls[0])
            label = self.model.names[cls]
            w, h = (x2 - x1).item(), (y2 - y1).item()
            x_c, y_c = (x1 + w / 2).item(), (y1 + h / 2).item()
            detections.append((x_c, y_c, w, h, label))
        
        # print("calculationg result dictionary...")
        grid = self._process_cube_side(detections)
        if grid:
            matrix = "".join("".join(row) for row in grid)
            parentcolor = grid[1][1]
            result_dict = {"parentcolor": parentcolor, "matrix": matrix}
            # print("✅ Würfelseite erkannt:", result_dict)

        return result_dict

    def detect_from_camera(self) -> dict | None:
        """Startet Kamera (index=2), zeigt YOLO-Detections live und gibt Ergebnis zurück, wenn 9 Felder erkannt."""
        cap = cv2.VideoCapture(self.cam_index)
        if not cap.isOpened():
            # print("❌ Keine Kamera gefunden.")
            return None

        # print("🎥 Kamera gestartet – halte eine Würfelseite ins Bild.")
        # print("Warte auf genau 9 erkannte Flächen ... (Taste [q] beendet)")

        result_dict = None
        FONT = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            ret, frame = cap.read()
            if not ret:
                # print("❌ Kein Frame empfangen.")
                break

            results = self.model.predict(source=frame, conf=self.conf_threshold, verbose=False)
            detections = []
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                cls = int(box.cls[0])
                label = self.model.names[cls]
                w, h = (x2 - x1).item(), (y2 - y1).item()
                x_c, y_c = (x1 + w / 2).item(), (y1 + h / 2).item()
                detections.append((x_c, y_c, w, h, label))
                # === YOLO-Visualisierung ===
                color = COLOR_MAP.get(label, (0, 255, 0))
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 5), FONT, 0.6, color, 2)

            grid = self._process_cube_side(detections)
            if grid:
                matrix = "".join("".join(row) for row in grid)
                parentcolor = grid[1][1]
                result_dict = {"parentcolor": parentcolor, "matrix": matrix}
                # print("✅ Würfelseite erkannt:", result_dict)
                break

            cv2.imshow("🧩 Cube Live Feed (YOLO)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Abbruch durch Benutzer.")
                break

        cap.release()
        cv2.destroyAllWindows()
        return result_dict


# === Testlauf ===
if __name__ == "__main__":
    model_path = r"C:\Users\heyni\Desktop\Studium\Master\Module\2025_26_WS\RSY\Project\RSY_UR3_ROBOT\data\models\best.pt"
    detector = CubeColorDetectorLive(model_path, cam_index=1)
    result = detector.detect_from_camera()
    # print("📦 Endergebnis:", result)
