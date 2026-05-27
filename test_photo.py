import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if ret:
    cv2.imwrite("my_photo.jpg", frame)
    print("✅ 照片已保存为 my_photo.jpg")
    print("请打开这张图片，看看照片里有没有你的人脸")
else:
    print("❌ 拍照失败")
