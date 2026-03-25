import cv2
import numpy as np
import os
from tqdm import tqdm

def create_silhouette_by_pixel(input_folder, output_folder, threshold=240):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_extensions)]

    for filename in tqdm(files, desc="處理像素中"):
        try:
            path = os.path.join(input_folder, filename)
            # 1. 讀取圖片
            img = cv2.imread(path)
            if img is None: continue
            
            h, w = img.shape[:2]

            # 2. 轉為灰階並二值化，找出「白色」區域
            # threshold 越高，代表越接近純白才算白色
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, white_mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

            # 3. Flood Fill (從左上角 0,0 開始填色)
            # 建立一個比原圖大兩像素的 mask (OpenCV 規定)
            ff_mask = np.zeros((h + 2, w + 2), np.uint8)
            
            # 我們要把與邊緣相連的白色「標記」出來
            # 先複製一份 white_mask，然後從角落開始填充
            flood_filled = white_mask.copy()
            cv2.floodFill(flood_filled, ff_mask, (0, 0), 255)
            
            # 4. 取得「非」外圍連通區域 (這包含主體，也包含主體內未連通的白斑)
            # flood_filled 的白色 (255) 是外圍，其餘 (0) 是主體和內部白斑
            main_body = cv2.bitwise_not(flood_filled) # 反轉：外圍黑，主體+內斑白

            # 5. 使用形態學膨脹 (Dilation) 來「吞噬」內部的微小黑色斑點
            # 建立一個圓形或方形的結構元素 (Kernel)，這裡用 3x3
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            
            # 進行膨脹：白色區域會向外擴張，填滿內部的黑色小洞
            dilated_body = cv2.dilate(main_body, kernel, iterations=1)

            # 6. 最後反轉回來：讓膨脹後的主體變黑，外圍保留白色
            final_silhouette = cv2.bitwise_not(dilated_body)

            # 7. 儲存結果
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
            cv2.imwrite(output_path, final_silhouette)

        except Exception as e:
            print(f"處理 {filename} 失敗: {e}")

if __name__ == "__main__":
    input_dir = r'C:\Users\user\Desktop\tos\webpage_tos_guess_image_mini_game\source_image'    # 原始圖片放這裡
    output_dir = r'C:\Users\user\Desktop\tos\webpage_tos_guess_image_mini_game\done_image' # 剪影圖片會存在這裡
    
    # threshold 建議設在 240-250 之間，視你的白色背景有多乾淨而定
    create_silhouette_by_pixel(input_dir, output_dir, threshold=245)
    print("\n處理完成！已保留外圍白色並將主體塗黑。")

