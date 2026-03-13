import cv2
import numpy as np
import os
from sklearn.cluster import KMeans
from PIL import Image

# --- 參數設定 ---
input_image_path = "hatt.png"  # ← 替換成你的圖檔路徑
num_colors = 7
tile_size = (128, 128)
output_dir = "pixel_7"

# --- 建立輸出資料夾 ---
os.makedirs(output_dir, exist_ok=True)

# --- 讀取圖片並轉成 RGB ---
img = cv2.imread(input_image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_data = img.reshape((-1, 3))  # 壓平成 Nx3 的矩陣

# --- 使用 KMeans 尋找主色 ---
kmeans = KMeans(n_clusters=num_colors, random_state=42).fit(img_data)
dominant_colors = kmeans.cluster_centers_.astype(int)

# --- 儲存每個主色為色塊圖片 ---
for i, color in enumerate(dominant_colors):
    rgb_tuple = tuple(color)
    block = np.full((tile_size[1], tile_size[0], 3), rgb_tuple, dtype=np.uint8)
    img_pil = Image.fromarray(block)
    filename = f"color_{i+1}_.png"
    img_pil.save(os.path.join(output_dir, filename))

print(f"✅ 成功產出 {num_colors} 張色塊圖片於「{output_dir}/」")
