import os
import requests
from concurrent.futures import ThreadPoolExecutor

# --- 設定區域 ---
BASE_URL = "https://d1h5mn9kk900cf.cloudfront.net/toswebsites/gallery/cards/{}.jpg"
SAVE_PATH = r"C:\Users\user\Desktop\tos\webpage_tos_guess_image_mini_game\source_image"
START_ID = 1
END_ID = 15000
MAX_WORKERS = 10  # 同時下載的數量，建議設定 5~20 之間

# 確保資料夾存在
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
    print(f"已建立資料夾：{SAVE_PATH}")

def download_image(card_id):
    # 格式化編號為 4 位數，例如 0001
    str_id = str(card_id).zfill(4)
    url = BASE_URL.format(str_id)
    file_name = f"{str_id}.jpg"
    full_save_path = os.path.join(SAVE_PATH, file_name)

    # 如果檔案已經存在，就跳過（方便中斷後續傳）
    if os.path.exists(full_save_path):
        return f"跳過 {file_name} (已存在)"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(full_save_path, "wb") as f:
                f.write(response.content)
            return f"成功下載 {file_name}"
        elif response.status_code == 404:
            return f"跳過 {file_name} (伺服器無此檔案)"
        else:
            return f"失敗 {file_name} (HTTP {response.status_code})"
    except Exception as e:
        return f"錯誤 {file_name}: {e}"

def main():
    print(f"開始下載任務，目標範圍：{START_ID} 到 {END_ID}...")
    
    # 使用 ThreadPoolExecutor 進行多執行緒下載
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 建立任務清單
        results = executor.map(download_image, range(START_ID, END_ID + 1))
        
        # 顯示進度
        for count, result in enumerate(results, 1):
            if count % 100 == 0: # 每 100 張回報一次進度
                print(f"已處理 {count}/{END_ID} 檔案...")
            # 如果想看每一條詳細結果，可以取消下面這行的註解
            # print(result)

    print("--- 任務完成 ---")

if __name__ == "__main__":
    main()