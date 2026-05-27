import cv2

def detect_focus():
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        return "no_camera"
    
    # 拍照
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return "no_frame"
    
    # 加载人脸检测模型
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # 转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) > 0:
        return "focused"
    else:
        return "no_face"

def detect_with_desc():
    state = detect_focus()
    desc = {
        "focused": "专注中 🎯",
        "no_face": "未检测到人脸 😶",
        "no_camera": "摄像头未找到 📷",
        "no_frame": "摄像头无画面 ❌"
    }
    return desc.get(state, "未知状态")

if __name__ == "__main__":
    result = detect_with_desc()
    print(f"状态: {result}")
