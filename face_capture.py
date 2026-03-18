import cv2
import os
import time

# ========== 配置 ==========
face_id = input("输入你的ID: ")
save_path = "dataset"
os.makedirs(save_path, exist_ok=True)

# ========== 摄像头初始化（关键修改！）==========
print("正在初始化摄像头...")
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # 强制使用 V4L2

# 设置 MJPEG 格式（大幅提升 USB 摄像头兼容性）
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)

if not cap.isOpened():
    print("❌ 无法打开摄像头！请检查连接和权限。")
    exit()

# ========== 人脸检测器 ==========
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ========== 采集逻辑 ==========
print("采集人脸数据中，请正对摄像头...")
count = 0

while True:
    start_time = time.time()
    
    ret, frame = cap.read()
    if not ret:
        print("❌ 无法读取摄像头画面，退出...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        count += 1
        face_img = gray[y:y + h, x:x + w]
        filename = f"{save_path}/User.{face_id}.{count}.jpg"
        cv2.imwrite(filename, face_img)
        print(f"✅ 已保存: {filename}")

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f"ID: {face_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # ========== 显示处理（安全模式）==========
    try:
        cv2.imshow("Face Capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or count >= 1000:
            break
    except cv2.error as e:
        # 如果没有图形界面，跳过显示（但继续采集！）
        print("⚠️ 无图形界面，仅后台采集... 按 Ctrl+C 停止")
        # 可选：加个简单退出机制（比如按 Enter）
        pass

    # 控制采集速度（约每秒10张）
    elapsed = time.time() - start_time
    if elapsed < 0.1:
        time.sleep(0.1 - elapsed)

print(f"✅ 采集完成！共保存 {count} 张图片到 '{save_path}'")
cap.release()
try:
    cv2.destroyAllWindows()
except:
    pass