import tkinter as tk
from PIL import Image, ImageTk
import random

# 로그인된 사용자 아이디 (예시)
logged_in_id = "kimire"

# 임의 점수 데이터 (최근 30일치)
# 실제로는 DB에서 불러오도록 수정 가능
scores = [random.randint(0, 100) for _ in range(30)]

# 점수 → 색상 매핑 함수
def score_to_color(score):
    if score == 0:
        return "#ebedf0"  # 회색 (기록 없음)
    elif score < 30:
        return "#c6e48b"  # 연녹
    elif score < 60:
        return "#7bc96f"  # 중간 녹색
    elif score < 90:
        return "#239a3b"  # 진한 녹색
    else:
        return "#196127"  # 아주 진한 녹색

# 창 생성
root = tk.Tk()
root.title("사람이 되자")

# 배경 이미지 불러오기
bg_img = Image.open("./img/records_background.png")
bg_photo = ImageTk.PhotoImage(bg_img)

# 창 크기 이미지에 맞춤
root.geometry(f"{bg_img.width}x{bg_img.height}")
root.resizable(False, False)

# 캔버스 생성
canvas = tk.Canvas(root, width=bg_img.width, height=bg_img.height)
canvas.pack(fill="both", expand=True)

# 배경 이미지 삽입
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# 아이디 표시
canvas.create_text(180, 160, text=logged_in_id, fill="black", 
                   font=("맑은 고딕", 14, "bold"), anchor="w")

# # "오늘 점수" 표시
# today_score = scores[-1]
# canvas.create_text(180, 200, text=f"오늘 점수: {today_score}", fill="black", 
#                    font=("맑은 고딕", 14, "bold"), anchor="w")

# 잔디 그래프 (최근 30일)
start_x, start_y = 150, 250   # 잔디 시작 위치
box_size = 15                 # 네모 크기
padding = 3                   # 네모 간격

for i, score in enumerate(scores):
    x = start_x + (i % 10) * (box_size + padding)   # 열
    y = start_y + (i // 10) * (box_size + padding)  # 행
    color = score_to_color(score)
    canvas.create_rectangle(x, y, x+box_size, y+box_size, fill=color, outline="")

# # 범례 표시
# canvas.create_text(start_x, start_y - 20, text="지난 점수 기록", 
#                    fill="black", font=("맑은 고딕", 12, "bold"), anchor="w")

root.mainloop()
