import tkinter as tk
from PIL import Image, ImageTk
import pymysql

# ===== 로그인된 사용자 아이디 전달받기 (예: sys.argv[1]) =====
import sys
if len(sys.argv) > 1:
    logged_in_id = sys.argv[1]
else:
    logged_in_id = "guest"

# ===== DB에서 점수 불러오기 =====
def fetch_scores(userid):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            passwd="Mysql4344!",   # DB 비밀번호 맞게 수정
            database="bePerson",
            charset="utf8mb4"
        )
        cursor = conn.cursor()

        # 최근 30일 점수 불러오기 (예시 테이블: user_scores)
        sql = """
            SELECT score 
            FROM user_scores
            WHERE userid = %s
            ORDER BY created_at DESC
            LIMIT 30
        """
        cursor.execute(sql, (userid,))
        result = cursor.fetchall()

        conn.close()

        # 튜플 → 리스트 변환, 최신순이니까 reverse()
        scores = [row[0] for row in result][::-1]
        return scores if scores else [0]*30  # 기록 없으면 0으로 채움

    except Exception as e:
        print("DB 오류:", e)
        return [0]*30  # DB 오류 시 기본값

scores = fetch_scores(logged_in_id)

# ===== 점수 → 색상 매핑 =====
def score_to_color(score):
    if score == 0:
        return "#ebedf0"  # 회색 (기록 없음)
    elif score < 30:
        return "#c6e48b"
    elif score < 60:
        return "#7bc96f"
    elif score < 90:
        return "#239a3b"
    else:
        return "#196127"

# ===== Tkinter 창 생성 =====
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

# 유저 아이디 표시
canvas.create_text(180, 160, text=logged_in_id, fill="black", 
                   font=("맑은 고딕", 14, "bold"), anchor="w")

# 잔디 그래프 (최근 30일)
start_x, start_y = 150, 250
box_size = 15
padding = 3

for i, score in enumerate(scores):
    x = start_x + (i % 10) * (box_size + padding)
    y = start_y + (i // 10) * (box_size + padding)
    color = score_to_color(score)
    canvas.create_rectangle(x, y, x+box_size, y+box_size, fill=color, outline="")

root.mainloop()
