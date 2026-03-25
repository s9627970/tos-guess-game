import re
import os

# 設定路徑
input_file = r'F:\auto_summary\test\monsterData.tsx'
output_file = r'F:\auto_summary\test\monster_list.txt'

def extract_monster_data():
    if not os.path.exists(input_file):
        print(f"錯誤：找不到檔案 {input_file}")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 正規表示法：匹配 id, name, attribute, race, star, monsterTag
        # 使用 re.DOTALL 處理跨行，並精確定位欄位
        pattern = re.compile(
            r"\{\s*'id':\s*(\d+),\s*"
            r"'name':\s*'(.*?)',\s*"
            r"'attribute':\s*'(.*?)',\s*"
            r"'race':\s*'(.*?)',\s*"
            r"'star':\s*(\d+),\s*"
            r"'monsterTag':\s*\[(.*?)\]",
            re.DOTALL
        )

        matches = pattern.findall(content)
        results = []

        for match in matches:
            m_id = int(match[0])
            name = match[1].strip()
            
            # 條件：ID >= 10819 且 名字不能為空
            if m_id >= 10819 and name:
                attribute = match[2].strip()
                race = match[3].strip()
                star = match[4].strip()
                
                # 處理標籤：移除單引號與空格，取第一個
                raw_tags = match[5].replace("'", "").replace('"', "").strip()
                tag_list = [t.strip() for t in raw_tags.split(',') if t.strip()]
                first_tag = tag_list[0] if tag_list else ""
                
                # 格式化輸出：60006 疾風形態 ‧ ORB 水 神 6 光之巨人
                line = f"id:{m_id} name:{name} attribute:{attribute} race:{race} star:{star} first_tag:{first_tag}"
                results.append(line)

        # 儲存結果
        with open(output_file, 'w', encoding='utf-8') as f_out:
            if results:
                f_out.write("\n".join(results))
                print(f"成功！已提取 {len(results)} 筆資料，儲存至：{output_file}")
            else:
                print("未找到符合條件（ID >= 10819 且有內容）的資料。")

    except Exception as e:
        print(f"執行時發生錯誤: {e}")

if __name__ == "__main__":
    extract_monster_data()