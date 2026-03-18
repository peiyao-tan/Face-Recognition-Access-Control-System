import cv2
import numpy as np
import os

# 数据集路径：从 train 目录指向 ../capture/dataset
dataset_path = os.path.join("..", "capture", "dataset")

# 检查路径是否存在
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"数据集路径不存在: {dataset_path}")

# 初始化识别器
recognizer = cv2.face.LBPHFaceRecognizer_create()

# 加载数据
faces = []
ids = []

# 自动分配递增 ID
id_map = {}  # 类别名（如用户编号）到 ID 的映射
current_id = 1  # 从 1 开始

# 遍历 dataset 文件夹中的所有 jpg 图片
for file in os.listdir(dataset_path):
    if file.endswith(".jpg"):
        path = os.path.join(dataset_path, file)
        face_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        if face_img is not None:
            faces.append(face_img)

            # 提取文件名前缀作为类别（例如 User.1.1.jpg → "1"）
            prefix = file.split(".")[1]  # 获取第一个点后的部分（即用户编号）

            # 如果这个类别没有分配过 ID，则分配一个新的 ID
            if prefix not in id_map:
                id_map[prefix] = current_id
                current_id += 1

            ids.append(id_map[prefix])
        else:
            print(f"跳过无效图像: {file}")

# 检查是否有有效数据
print(f"有效人脸数: {len(faces)}")
print(f"有效 ID 数: {len(ids)}")

# 打印类别与 ID 对应关系
print("类别与 ID 对应关系：")
for prefix, assigned_id in id_map.items():
    print(f"类别: {prefix}, ID: {assigned_id}")

# 训练模型
if len(faces) > 0 and len(ids) > 0:
    print("训练模型中...")
    recognizer.train(faces, np.array(ids))
    model_path = os.path.join("..", "recognize", "face_model.yml")  # 保存到 recognize 文件夹
    recognizer.write(model_path)
    print(f"模型训练完成并已保存为: {model_path}")
else:
    print("没有有效的训练数据，无法训练模型。")