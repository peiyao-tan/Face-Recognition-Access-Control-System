from gpiozero import Servo
from time import sleep

# SG90 舵机接在 GPIO18
servo = Servo(18)

try:
    print("▶ 舵机测试（gpiozero）：-1 → 0 → +1")
    servo.min()    # ≈ 0°
    sleep(1)
    servo.mid()    # ≈ 90°
    sleep(1)
    servo.max()    # ≈ 180°
    sleep(1)
    servo.mid()
    print("✅ 测试完成！")

except KeyboardInterrupt:
    print("⚠️ 中断")
finally:
    servo.close()  # 显式释放资源
