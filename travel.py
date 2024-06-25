import tkinter as tk
import tkinter.simpledialog as sd
import os
import openai
import requests
from tkinter import *
import urllib.request
import json
import re
from PIL import Image, ImageTk

# GPT-3 API 키
openai.api_key = "secret"


def recommend_places(region, detail):
    messages = []
    messages.append({"role": "user", "content": f"{region} {detail} 5곳 추천해줘"})
    while True:
        user_content = input("user: ")
        messages.append({"role": "user", "content": f"{user_content}"})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        assistant_content = completion.choices[0].message["content"].strip()
        messages.append({"role": "assistant", "content": f"{assistant_content}"})
        print(f"GPT: {assistant_content}")


# 지도 이미지 파일 경로
map_image_path = r"C://Users//김문기\Desktop//지도.png"

# 지역 정보 사전
region_details = {
    "서울특별시": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/서울1.gif",
        "details": ["강남구", "강서구", "송파구", "마포구"],
    },
    "경기도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/경기도1.gif",
        "details": [
            "김포",
            "고양",
            "파주",
            "연천",
            "동두천",
            "포천",
            "의정부",
            "양주",
            "가평",
            "남양주",
            "구리",
            "하남",
            "인천",
            "양평",
            "부천",
            "시흥",
            "광명",
            "안양",
            "안산",
            "과천",
            "군포",
            "의왕",
            "성남",
            "광주",
            "여주",
            "수원",
            "용인",
            "이천",
            "화성",
            "오산",
            "평택",
            "안성",
        ],
    },
    "강원도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/강원도1.gif",
        "details": [
            "철원",
            "화천",
            "양구",
            "고성",
            "인제",
            "속초",
            "춘천",
            "양양",
            "홍천",
            "횡성",
            "평창",
            "강릉",
            "원주",
            "정선",
            "동해",
            "영월",
            "태백",
            "삼척",
        ],
    },
    "충청북도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/충청북도1.gif",
        "details": [
            "음성",
            "충주",
            "제천",
            "단양",
            "진천",
            "증평",
            "괴산",
            "청주",
            "보은",
            "옥천",
            "영동",
            "세종",
        ],
    },
    "충청남도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/충청남도1.gif",
        "details": [
            "태안",
            "서산",
            "당진",
            "아산",
            "천안",
            "예산",
            "홍성",
            "청양",
            "공주",
            "보령",
            "부여",
            "서천",
            "논산",
            "계룡",
            "금산",
            "대전",
        ],
    },
    "전라북도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/전라북도1.gif",
        "details": [
            "군산",
            "익산",
            "완주",
            "김제",
            "전주",
            "진안",
            "무주",
            "부안",
            "정읍",
            "임실",
            "장수",
            "고창",
            "순창",
            "남원",
        ],
    },
    "전라남도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/전라남도1.gif",
        "details": [
            "영광",
            "장성",
            "담양",
            "곡성",
            "구례",
            "함평",
            "광주",
            "신안",
            "목포",
            "무안",
            "나주",
            "화순",
            "순천",
            "광양",
            "영암",
            "장흥",
            "보성",
            "여수",
            "진도",
            "해남",
            "강진",
            "완도",
            "고흥",
        ],
    },
    "경상북도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/경상북도1.gif",
        "details": [
            "문경",
            "예천",
            "영주",
            "봉화",
            "울진",
            "안동",
            "염암",
            "상주",
            "의성",
            "청송",
            "영덕",
            "김천",
            "구미",
            "군위",
            "영천",
            "포항",
            "성주",
            "칠곡",
            "대구",
            "경산",
            "경주",
            "고령",
            "청도",
            "울릉도",
            "독도",
            "부산",
            "울산",
        ],
    },
    "경상남도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/경상남도1.gif",
        "details": [
            "거창",
            "함양",
            "합천",
            "창녕",
            "밀양",
            "양산",
            "산청",
            "의령",
            "진주",
            "함안",
            "창원",
            "김해",
            "하동",
            "사천",
            "고성",
            "남해",
            "통영",
            "거제",
        ],
    },
    "제주특별자치도": {
        "image_path": r"C:/Users/김문기/Desktop/gif/450/제주도1.gif",
        "details": ["제주시", "서귀포시"],
    },
}


current_region = None


def on_region_click(region):
    global current_region

    # 기존에 표시되고 있는 이미지 삭제
    map_label.configure(image="")
    current_region = region

    # 해당 지역의 이미지 표시
    image_path = region_details.get(region, {}).get("image_path")
    if image_path:
        region_image = tk.PhotoImage(file=image_path)
        map_label.configure(image=region_image)
        map_label.image = region_image

    # 해당 지역의 세부지역 버튼 생성
    details = region_details.get(region, {}).get("details", [])
    update_detail_buttons(details)


def update_detail_buttons(details):
    # 기존에 있는 세부지역 버튼 삭제
    for button in detail_buttons:
        button.destroy()

    detail_buttons.clear()

    # 새로운 세부지역 버튼 생성
    for detail in details:
        button = tk.Button(
            detail_frame,
            text=detail,
            width=button_width,
            command=lambda d=detail: on_detail_click(d),
        )
        detail_buttons.append(button)
        button.pack(side=tk.LEFT)


def on_detail_click(detail):
    region_info = region_details.get(current_region)
    if region_info:
        region_details = region_info.get("details", [])
        detail_info = f"{current_region} {detail}"
        print(detail_info)


# GUI 생성
root = tk.Tk()
root.title("대한민국 지도")

# 창의 크기 설정
window_width = 565
window_height = 720

# 창을 컴퓨터 중앙 위로 위치시키기
window_x = (root.winfo_screenwidth() // 2) - (window_width // 2)
# 화면의 x축 중앙에서 시작됨  - (window_width // 2) 이 코드를 통해 창의 중앙 부분이 화면 가운데로 오게 함
window_y = (root.winfo_screenheight() // 4) - (window_height // 2) + 200
# 화면의 y축 중앙에서 시작됨 + 200 이 없을 경우 노트북 화면상 윗 부분이 잘려서 200만큼 내려 줌
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
# 크기에 맞게 설정한 위치를 통해 중앙에 나오게 해줌

# 지도 이미지 표시
map_image = tk.PhotoImage(file=map_image_path)
map_label = tk.Label(root, image=map_image)
map_label.pack()

# 지역 버튼 생성
button_frame = tk.Frame(root)
button_frame.pack()

# 버튼을 가로로 나열하기 위한 설정
button_width = 12  # 버튼의 가로 크기
num_buttons_per_row = 3  # 한 줄에 배치할 버튼의 개수

button_count = 0
button_row = None

for region in region_details.keys():
    if button_count % num_buttons_per_row == 0:
        # 한 줄에 버튼의 개수에 도달하면 새로운 줄 생성
        button_row = tk.Frame(button_frame)
        button_row.pack()

    region_button = tk.Button(
        button_row,
        text=region,
        width=button_width,
        command=lambda r=region: on_region_click(r),
    )
    region_button.pack(side=tk.LEFT)

    button_count += 1
# 대화 메시지를 저장하는 리스트
messages = []

# 세부지역 버튼 생성
detail_frame = tk.Frame(root)
detail_frame.pack()

detail_buttons = []


def update_detail_buttons():
    global current_region

    # 기존에 있는 세부지역 버튼 삭제
    for button in detail_buttons:
        button.destroy()

    detail_buttons.clear()

    region_info = region_details.get(current_region)
    if region_info:
        details = region_info.get("details", [])
        num_buttons_per_row = 6  # 한 줄에 배치할 버튼의 개수

        for i, detail in enumerate(details):
            button = tk.Button(
                detail_frame,
                text=detail,
                width=button_width,
                command=lambda d=detail: on_detail_click(d),
            )
            detail_buttons.append(button)
            button.grid(row=i // num_buttons_per_row, column=i % num_buttons_per_row)


def on_region_click(region):
    global current_region

    # 기존에 표시되고 있는 이미지 삭제
    map_label.configure(image="")
    current_region = region

    # 해당 지역의 이미지 표시
    image_path = region_details.get(region, {}).get("image_path")
    if image_path:
        region_image = tk.PhotoImage(file=image_path)
        map_label.configure(image=region_image)
        map_label.image = region_image

    # 해당 지역의 세부지역 버튼 생성
    update_detail_buttons()


# 버튼에 이미지 같이 표현하는 부분, 경로명 수정 필요
img_accomodation = Image.open("C://Users//김문기//Desktop//resaurant.gif")
img_cafe = Image.open("C://Users//김문기//Desktop//cafe.gif")
img_restaurant = Image.open("C://Users//김문기//Desktop//accomodation.gif")
img_travel = Image.open("C://Users//김문기//Desktop//travel.gif")

img_accomodation = img_accomodation.resize((100, 100))
img_cafe = img_cafe.resize((100, 100))
img_restaurant = img_restaurant.resize((100, 100))
img_travel = img_travel.resize((100, 100))

img_acc_tk = ImageTk.PhotoImage(img_accomodation)
img_cafe_tk = ImageTk.PhotoImage(img_cafe)
img_rest_tk = ImageTk.PhotoImage(img_restaurant)
img_travel_tk = ImageTk.PhotoImage(img_travel)


def on_detail_click(detail):
    region_info = region_details.get(current_region)

    image_refs = [img_acc_tk, img_cafe_tk, img_rest_tk, img_travel_tk]

    if region_info:
        detail_info = f"{current_region} {detail}"
        print(detail_info)

        # 새 창 생성
        detail_window = tk.Toplevel(root)
        detail_window.title("여행지 추천")
        detail_window_width = 900
        detail_window_height = 720

        # 창을 컴퓨터 중앙 위로 위치시키기
        detail_window_x = (root.winfo_screenwidth() // 2) - (detail_window_width // 2)
        # 화면의 x축 중앙에서 시작됨  - (window_width // 2) 이 코드를 통해 창의 중앙 부분이 화면 가운데로 오게 함
        detail_window_y = (
            (root.winfo_screenheight() // 4) - (detail_window_height // 2) + 200
        )
        # 화면의 y축 중앙에서 시작됨 + 200 이 없을 경우 노트북 화면상 윗 부분이 잘려서 200만큼 내려 줌
        detail_window.geometry(
            f"{detail_window_width}x{detail_window_height}+{detail_window_x}+{detail_window_y}"
        )
        # 세부지역 정보 표시
        detail_label = tk.Label(detail_window, text=detail_info)
        detail_label.pack()

        # 버튼 추가
        # button1 = tk.Button(detail_window, text="여행지", command=lambda: ask_question(detail_info + " 여행지 5곳 추천해줘"))
        button1 = tk.Button(
            detail_window,
            text="여행지",
            image=img_travel_tk,
            compound="top",
            command=lambda: handle_button_click(detail_info),
        )
        button1.place(x=100, y=480)

        button2 = tk.Button(
            detail_window,
            text="숙소",
            image=img_acc_tk,
            compound="top",
            command=lambda: handle_button_click_resaurant(detail_info),
        )
        button2.place(x=300, y=480)

        button3 = tk.Button(
            detail_window,
            text="맛집",
            image=img_rest_tk,
            compound="top",
            command=lambda: handle_button_click_accomodation(detail_info),
        )
        button3.place(x=500, y=480)

        button4 = tk.Button(
            detail_window,
            text="카페",
            image=img_cafe_tk,
            compound="top",
            command=lambda: handle_button_click_cafe(detail_info),
        )
        button4.place(x=700, y=480)

        response_label = tk.Label(detail_window, textvariable=assistant_response)
        response_label.pack()

        response_label_cafe = tk.Label(
            detail_window, textvariable=assistant_response_cafe
        )
        response_label_cafe.pack()


assistant_response = tk.StringVar()
assistant_response_cafe = tk.StringVar()
assistant_response_acoomodation = tk.StringVar()
assistant_response_resaurant = tk.StringVar()


def handle_button_click(detail_info):
    assistant_response_cafe.set("")
    assistant_response.set(ask_question(detail_info + "여행지 5곳 추천해줘"))


def handle_button_click_cafe(detail_info):
    assistant_response.set("")
    cafe_search(detail_info + " 카페")
    # assistant_response_cafe.set(cafe_search(detail_info + " 카페"))


def handle_button_click_accomodation(detail_info):
    assistant_response.set("")
    accomodation_search(detail_info + " 맛집")
    # assistant_response_cafe.set(cafe_search(detail_info + " 카페"))


def handle_button_click_resaurant(detail_info):
    assistant_response.set("")
    resaurant_search(detail_info + " 숙소")


def ask_question(question):
    user_message = {"role": "user", "content": question}
    messages.append(user_message)

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    assistant_response = completion.choices[0].message["content"]
    print("Assistant:", assistant_response)
    messages.append({"role": "assistant", "content": assistant_response})
    return assistant_response


################################################################


def searchbook(title):
    # 애플리케이션 클라이언트 id 및 secret
    client_id = "E2JOucqB2tPfVTcrrnb_"
    client_secret = "nf8i1ck2CZ"

    # 도서검색 url
    url = "https://openapi.naver.com/v1/search/local.json"
    option = "&display=5&sort=count"
    query = "?query=" + urllib.parse.quote(title)
    url_query = url + query + option

    # Open API 검색 요청 개체 설정
    request = urllib.request.Request(url_query)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    # 검색 요청 및 처리
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        return response.read().decode("utf-8")
    else:
        return None


def showitem(item):
    name = re.sub(r"<[^>]+>", "", item["title"])
    address = re.sub(r"<[^>]+>", "", item["address"])
    return name, address


def cafe_search(detail_info):
    result_list = tk.Listbox()
    res = searchbook(detail_info + " 카페")
    if res == None:
        print("검색 실패!!!")
        return
    jres = json.loads(res)
    if jres == None:
        print("json.loads 실패!!!")
        return

    res_list = []

    for item in jres["items"]:
        title = "이름: " + item["title"]
        road_address = "주소: " + item["roadAddress"]
        res_list.append(f"{title}\n{road_address}")

    assistant_response_cafe.set("\n\n".join(res_list))

    print(jres)

    return jres


def accomodation_search(detail_info):
    result_list = tk.Listbox()
    res = searchbook(detail_info + " 맛집")
    if res == None:
        print("검색 실패!!!")
        return
    jres = json.loads(res)
    if jres == None:
        print("json.loads 실패!!!")
        return

    res_list = []

    for item in jres["items"]:
        title = "이름: " + item["title"]
        road_address = "주소: " + item["roadAddress"]
        res_list.append(f"{title}\n{road_address}")

    assistant_response_cafe.set("\n\n".join(res_list))

    print(jres)

    return jres


def resaurant_search(detail_info):
    result_list = tk.Listbox()
    res = searchbook(detail_info + " 숙소")
    if res == None:
        print("검색 실패!!!")
        return
    jres = json.loads(res)
    if jres == None:
        print("json.loads 실패!!!")
        return

    res_list = []

    for item in jres["items"]:
        title = "이름: " + item["title"]
        road_address = "주소: " + item["roadAddress"]
        res_list.append(f"{title}\n{road_address}")

    assistant_response_cafe.set("\n\n".join(res_list))

    print(jres)

    return jres


def on_item_select(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        item_text = event.widget.get(index)
        name = re.search(r"이름: (.+)", item_text).group(1)
        address = re.search(r"주소: (.+)", item_text).group(1)
        print(f"선택된 항목:\n이름: {name}\n주소: {address}\n")


root.mainloop()
