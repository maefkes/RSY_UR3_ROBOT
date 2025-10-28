import pyrealsense2 as rs
import numpy as np
import cv2

# 1) Pipeline erstellen
pipeline = rs.pipeline()

# 2) Konfiguration: Stream aktivieren (Farbbild + Tiefenbild)
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 3) Stream starten
pipeline.start(config)

try:
    while True:
        # 4) Frames auslesen
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # 5) In NumPy konvertieren
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # 6) Tiefenbild einfärben
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03), 
            cv2.COLORMAP_JET
        )

        # 7) Anzeigen
        images = np.hstack((color_image, depth_colormap))
        cv2.imshow('RealSense', images)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 8) Stoppen und Fenster schließen
    pipeline.stop()
    cv2.destroyAllWindows()