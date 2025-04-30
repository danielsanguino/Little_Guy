import cv2
import torch
from ultralytics import YOLO
import serial
import time

# --- CONFIG ---
MODEL_PATH = "best.pt"
SERIAL_PORT = "/dev/ttyUSB0"
CONF_THRESHOLD = 0.5
DEAD_ZONE = 0.7  # How close to center is considered "centered"
FRAME_WIDTH = 224
FRAME_HEIGHT = 224

# --- SETUP ---
model = YOLO(MODEL_PATH)

arduino = serial.Serial(SERIAL_PORT, 115200, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

print("Tracking started. Press Ctrl+C to quit.")


# ---Track---
try:
    fish_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break

        results = model(frame)[0]

        if len(results.boxes) > 0:
            fish_detected = True
            img_w = frame.shape[1]
            img_h = frame.shape[0]
            centers = [(b.xywh[0][0].item(), b.xywh[0][1].item(), b.xywh[0][2].item(), b.xywh[0][3].item(), b.conf.item()) for b in results.boxes]
            most_central = min(centers, key=lambda x: abs((x[0] / img_w) - 0.5))
            x_center, y_center, width, height, confidence = most_central
            x_center_norm = x_center / img_w

            if confidence > CONF_THRESHOLD:
                offset = x_center_norm - 0.5

                if offset < -DEAD_ZONE:
                    arduino.write(b'L\n')
                    print("Command: LEFT")
                elif offset > DEAD_ZONE:
                    arduino.write(b'R\n')
                    print("Command: RIGHT")
                else:
                    arduino.write(b'F\n')
                    print("Command: FORWARD")

                # Draw bounding box
                x1 = int(x_center - width / 2)
                y1 = int(y_center - height / 2)
                x2 = int(x_center + width / 2)
                y2 = int(y_center + height / 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Conf: {confidence:.2f}", (x1, max(y1 - 10, 0)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            else:
                arduino.write(b'S\n')
                print("Command: STOP (low confidence)")
        else:
            fish_detected = False
            arduino.write(b'S\n')
            print("Command: STOP (no fish)")

        time.sleep(0.1)

# ---Interrupt---
except KeyboardInterrupt:
    print("Stopped by user")

finally:
    arduino.write(b'S\n')
    arduino.close()
    cap.release()
    # cv2.destroyAllWindows()
    print("Tracking stopped.")
