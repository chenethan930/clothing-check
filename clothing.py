import openai
import base64
import requests
from PIL import Image
import json
import streamlit as st

with st.form("my_form"):
    uploaded_file = st.file_uploader("Choose a file", type=["jpeg", "png", "jpg"])
    submitted = st.form_submit_button("Upload")

if submitted:
    bytes_data = uploaded_file.getvalue()
    base64_encoded_str3 = base64.b64encode(bytes_data).decode('utf-8')

    file_path1 = "cloth1.png"
    file_path2 = "cloth2.png"
    # file_path3 = "cloth3.png"

    with open(file_path1, 'rb') as image_file1:
        base64_encoded_str1 = base64.b64encode(image_file1.read()).decode('utf-8')

    with open(file_path2, 'rb') as image_file2:
        base64_encoded_str2 = base64.b64encode(image_file2.read()).decode('utf-8')

    # with open(file_path3, 'rb') as image_file3:
    #     base64_encoded_str3 = base64.b64encode(image_file3.read()).decode('utf-8')


    if image_file1 and image_file2:
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets["api_key"]}"
        }

        payload = {
        "model": "gpt-4o-mini",
        "response_format": { "type": "json_object" },
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"""請依照頭、上半身、外搭三個類別，分析圖中人物的穿搭及配色，每個部分都有幾個種類可以選擇如下：

    頭：空、棒球帽、漁夫帽、貝雷帽、粗框眼鏡、細框眼鏡、髮帶
    上半身：空、背心、長袖圓領T恤、長袖V領T恤、長袖高領T恤、短袖圓領T恤、短袖V領T恤、短袖高領T恤、帽T、長袖襯衫、短袖襯衫、洋裝
    外搭：空、細肩背心、西裝外套、拉鍊外套、針織外套、羽絨外套、外搭襯衫

    請根據圖片，在每個類別中都選擇一個種類，若在類別中沒有符合的種類可以選擇，則會被判定為「空」。"""
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpg;base64,{base64_encoded_str1}"
                }
                },
                {
                "type": "text",
                "text": """{“頭”:{“類型”:“漁夫帽”, “顏色”:”藍色”, “色票”:”#C4D1D6”},”上半身":{“類型”:“帽T”, “顏色”:”#白色”, “色票”:”#000000”},”外搭":{“類型”:“空”, “顏色”:”空”, “色票”:”空”}}""",
                },
                {
                "type": "text",
                "text": f"""請依照頭、上半身、外搭三個類別，分析圖中人物的穿搭及配色，每個部分都有幾個種類可以選擇如下：

    頭：空、棒球帽、漁夫帽、貝雷帽、粗框眼鏡、細框眼鏡、髮帶
    上半身：空、背心、長袖圓領T恤、長袖V領T恤、長袖高領T恤、短袖圓領T恤、短袖V領T恤、短袖高領T恤、帽T、長袖襯衫、短袖襯衫、洋裝
    外搭：空、細肩背心、西裝外套、拉鍊外套、針織外套、羽絨外套、外搭襯衫

    請根據圖片，在每個類別中都選擇一個種類，若在類別中沒有符合的種類可以選擇，則會被判定為「空」。在選擇種類時，請不要跨類別進行選擇。"""
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpg;base64,{base64_encoded_str2}"
                }
                },
                            {
                "type": "text",
                "text": """{“頭”:{“類型”:“空”, “顏色”:”空”, “色票”:”空”},”上半身":{“類型”:“短袖圓領T恤”, “顏色”:”白色”, “色票”:”#FFFFFF”},”外搭":{“類型”:“拉鍊外套”, “顏色”:”#黑色”, “色票”:”#000000”}}""",
                },
                {
                "type": "text",
                "text": """請依照頭、上半身、外搭三個類別，分析圖中人物的穿搭及配色，每個部分都有幾個種類可以選擇如下：

    頭：空、棒球帽、漁夫帽、貝雷帽、粗框眼鏡、細框眼鏡、髮帶
    上半身：空、背心、長袖圓領T恤、長袖V領T恤、長袖高領T恤、短袖圓領T恤、短袖V領T恤、短袖高領T恤、帽T、長袖襯衫、短袖襯衫、洋裝
    外搭：空、細肩背心、西裝外套、拉鍊外套、針織外套、羽絨外套、外搭襯衫

    請根據圖片，在每個類別中都選擇一個種類，若在類別中沒有符合的種類可以選擇，則會被判定為「空」。Provide your response as a JSON object with the following schema: {"頭": {"類型": "", "顏色": "", “色票”:””}, "上半身": {"類型": "", "顏色": "", “色票”:””},"外搭": {"類型": "", "顏色": "", “色票”:””}} """,
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpg;base64,{base64_encoded_str3}"
                }
                },
            ]
            }
        ],
        "max_tokens": 300
        }
        while True:

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            message = response.json()
            if "sorry" in message['choices'][0]['message']['content']:
                print("contain sorry")
                continue
            else:
                break

    # print(type(message['choices'][0]['message']['content']))


    answer = json.loads(message['choices'][0]['message']['content'])

    # st.write(answer)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""#### 頭""")
        st.caption("類型")
        st.write(answer["頭"]["類型"])
        st.caption("顏色/樣式")
        st.write(answer["頭"]["顏色"])
        st.caption("色票")
        st.write(answer["頭"]["色票"])
    with col2:
        st.markdown("""#### 上半身""")
        st.caption("類型")
        st.write(answer["上半身"]["類型"])
        st.caption("顏色/樣式")
        st.write(answer["上半身"]["顏色"])
        st.caption("色票")
        st.write(answer["上半身"]["色票"])
    with col3:
        st.markdown("""#### 外搭""")
        st.caption("類型")
        st.write(answer["外搭"]["類型"])
        st.caption("顏色/樣式")
        st.write(answer["外搭"]["顏色"])
        st.caption("色票")
        st.write(answer["外搭"]["色票"])
