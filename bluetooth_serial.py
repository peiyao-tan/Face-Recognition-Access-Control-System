import serial
import threading
import time

class BluetoothSerial:
    def __init__(self, port='/dev/serial0', baudrate=9600, timeout=1):
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_running = False
        self.command_callback = None  # 指令回调函数（触发舵机）

    # 初始化串口连接
    def init_serial(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout
            )
            if self.ser.isOpen():
                print(f"蓝牙串口已打开：{self.port}")
                self.is_running = True
                return True
            return False
        except Exception as e:
            print(f"串口初始化失败：{e}")
            return False

    # 监听串口数据（独立线程）
    def listen_thread(self):
        while self.is_running:
            try:
                if self.ser.in_waiting > 0:
                    # 读取手机发送的指令（按换行符分割，去除空格）
                    command = self.ser.readline().decode('utf-8').strip()
                    print(f"收到蓝牙指令：{command}")
                    # 调用回调函数处理指令（如开门）
                    if self.command_callback:
                        self.command_callback(command)
                time.sleep(0.1)
            except Exception as e:
                print(f"串口监听异常：{e}")

    # 启动监听线程
    def start_listen(self, callback):
        self.command_callback = callback
        if self.init_serial():
            listen_thread = threading.Thread(target=self.listen_thread, daemon=True)
            listen_thread.start()
            print("蓝牙指令监听线程已启动")

    # 停止监听，关闭串口
    def stop_listen(self):
        self.is_running = False
        if self.ser and self.ser.isOpen():
            self.ser.close()
            print("蓝牙串口已关闭")