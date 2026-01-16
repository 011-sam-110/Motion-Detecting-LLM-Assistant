import cv2
import time

def take_photo(filename="src/photo.jpg", camera_index=1):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # CAP_DSHOW = faster on Windows

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")

    # Warm up camera very briefly (improves exposure)
    time.sleep(0.1)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("Failed to capture image")

    cv2.imwrite(filename, frame)
    return filename

print(take_photo())