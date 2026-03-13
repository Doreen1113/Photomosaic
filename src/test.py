import pathlib
import json
import os
import math
import random
import numpy as np
import cv2

# --- 平均顏色計算 ---
def get_average_color(img):
    if img is None or img.size == 0:
        return (0, 0, 0)
    average_color = np.average(np.average(img, axis=0), axis=0)
    average_color = np.around(average_color, decimals=-1)
    return tuple(int(i) for i in average_color)

# --- 找最接近顏色的圖片 ---
def get_closest_color(color, colors):
    cr, cg, cb = color
    min_difference = float("inf")
    closest_color = None
    for c in colors:
        try:
            r, g, b = eval(c)
            difference = math.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
            if difference < min_difference:
                min_difference = difference
                closest_color = (r, g, b)
        except:
            continue
    return closest_color if closest_color else (0, 0, 0)

# --- 快取處理素材圖片的平均顏色 ---
if "cache.json" not in os.listdir():
    imgs_dir = pathlib.Path("art")
    images = list(imgs_dir.glob("*\\*.jpg"))
    print(f"A total of {len(images)} images were read")  

    data = {}
    for img_path in images:
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        average_color = get_average_color(img)
        key = str(average_color)
        data.setdefault(key, []).append(str(img_path))
    with open("cache.json", "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)
    print("✅ Caching done")
else:
    with open("cache.json", "r") as file:
        data = json.load(file)

# --- 讀入主圖 ---
img = cv2.imread("hatt.png")
if img is None:
    raise FileNotFoundError(" not find hatt.png！")

tile_height, tile_width = 10, 10
img_height, img_width, _ = img.shape
num_tiles_h = img_height // tile_height
num_tiles_w = img_width // tile_width
img = img[:tile_height * num_tiles_h, :tile_width * num_tiles_w]

tiles = []
for y in range(0, img.shape[0], tile_height):
    for x in range(0, img.shape[1], tile_width):
        tiles.append((y, y + tile_height, x, x + tile_width))

random.shuffle(tiles)

# --- 生成馬賽克 ---
for tile in tiles:
    y0, y1, x0, x1 = tile
    if y1 > img.shape[0] or x1 > img.shape[1]:
        continue

    average_color = get_average_color(img[y0:y1, x0:x1])
    closest_color = get_closest_color(average_color, data.keys())

    if str(closest_color) not in data:
        continue

    i_path = random.choice(data[str(closest_color)])
    i = cv2.imread(i_path)
    if i is None:
        continue

    i = cv2.resize(i, (tile_width, tile_height), interpolation=cv2.INTER_LANCZOS4)
    img[y0:y1, x0:x1] = i

    try:
        cv2.imshow("Building Mosaic", img)
        cv2.waitKey(1)
    except:
        pass

cv2.imwrite("oart.png", img)
cv2.destroyAllWindows()
print("finish")

# # --- AI 超解析度放大 ---
# print("AI super-resolution upscaling begins in HD...")
# sr = cv2.dnn_superres.DnnSuperResImpl_create()
# sr.readModel("EDSR_x2.pb")
# sr.setModel("edsr", 2)

# img = cv2.imread("out2.png")
# if img is None:
#     raise FileNotFoundError("not find igout.png！")

# result = sr.upsample(img)
# cv2.imwrite("van2_highres.png", result)
# print("✅ HD van_highres.png")
