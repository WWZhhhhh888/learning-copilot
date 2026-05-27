import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("摄像头打不开")
else:
    ret, frame = cap.read()
    if ret:
        print("✅ 拍照成功！")
        cv2.imwrite("test_photo.jpg", frame)
        print("照片已保存为 test_photo.jpg")
    else:
        print("❌ 拍照失败")
    cap.release()
