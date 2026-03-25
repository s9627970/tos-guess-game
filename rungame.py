import http.server
import socketserver
import webbrowser
import os

# 1. 自動切換到這個 Python 檔案所在的目錄
# 這樣可以確保伺服器抓得到同資料夾的 index.html 與 card_name.txt
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir:
    os.chdir(script_dir)

Handler = http.server.SimpleHTTPRequestHandler

# 2. 使用 port 0，讓系統自動分配一個「目前沒人使用的連接埠」
# 這樣就不用擔心 Port 8000 或 8080 剛好被其他程式佔用而報錯
try:
    with socketserver.TCPServer(("", 0), Handler) as httpd:
        # 取得系統分配的埠號
        port = httpd.server_address[1]
        url = f"http://localhost:{port}"
        
        print(f"🚀 神魔之塔猜卡片 - 本地伺服器已啟動！")
        print(f"🌐 網址：{url}")
        print("💡 正在自動開啟瀏覽器... 若沒有彈出視窗，請手動複製上方網址到瀏覽器貼上。")
        print("🛑 若要關閉伺服器結束遊戲，請在這裡按下 [Ctrl + C]")
        
        # 3. 自動在預設瀏覽器中開啟該網址
        webbrowser.open(url)
        
        # 4. 讓伺服器持續運作，直到你手動關閉
        httpd.serve_forever()

except KeyboardInterrupt:
    print("\n👋 伺服器已關閉，感謝遊玩！")
except Exception as e:
    print(f"\n❌ 發生錯誤：{e}")
    input("按 Enter 鍵結束...")