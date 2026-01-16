import cv2

def list_available_cameras(max_index=10):
    available = []

    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # CAP_DSHOW helps on Windows
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                available.append(i)
                print(f"✅ Camera index {i} is available")
            cap.release()
        else:
            cap.release()

    if not available:
        print("❌ No cameras found")
    return available


list_available_cameras()
