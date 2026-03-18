import cv2

# 强制使用 V4L2 并设置 MJPEG
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# 关键：设置像素格式为 MJPEG
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# 设置分辨率（建议从低开始）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)  # 降低帧率更稳定

if not cap.isOpened():
    print("❌ 无法打开摄像头")
    exit()

print("✅ 摄像头已启动，开始显示画面...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 无法读取帧（可能是供电不足、格式不支持或设备断开）")
        break

    cv2.imshow('Camera Test', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
