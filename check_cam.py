import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ 摄像头索引 {i} 可用")
            cv2.imwrite(f"cam_{i}.jpg", frame)
            print(f"   照片已保存为 cam_{i}.jpg")
        else:
            print(f"⚠️ 摄像头索引 {i} 能打开但无法拍照")
        cap.release()
    else:
        print(f"❌ 摄像头索引 {i} 不可用")
