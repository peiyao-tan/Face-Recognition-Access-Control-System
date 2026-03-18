import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class VideoStreamApp(QWidget):
    def __init__(self, stream_url):
        super().__init__()

        self.stream_url = stream_url
        self.cap = cv2.VideoCapture(self.stream_url)  # 从网络流读取视频
        self.init_ui()

        # 定时器定期更新画面
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 每 30ms 更新一次画面

    def init_ui(self):
        self.video_label = QLabel(self)  # 显示视频流
        self.quit_button = QPushButton("退出")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

        # 绑定退出按钮
        self.quit_button.clicked.connect(self.close_app)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def close_app(self):
        self.cap.release()
        self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # 替换为树莓派的 IP 地址
    stream_url = "http://10.20.10.73:5000/video_feed"
    window = VideoStreamApp(stream_url)
    window.setWindowTitle("树莓派摄像头视频流")
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())
