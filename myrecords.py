import tkinter as tk
from PIL import Image, ImageTk
import pymysql
import sys
from tkinter import font as tkFont

# ===== 로그인된 사용자 PK(id) 전달받기 =====
if len(sys.argv) > 1:
    logged_in_id = sys.argv[1]
else:
    logged_in_id = None

# ===== DB 연결 설정 =====
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "passwd": "Mysql4344!",  # 비밀번호 확인
    "database": "bePerson",
    "charset": "utf8mb4"
}

# ===== DB에서 userid 불러오기 =====
def fetch_userid(user_pk):
    if not user_pk:
        return "게스트"
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT userid FROM USERS WHERE id = %s", (user_pk,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "게스트"
    except Exception as e:
        print("DB 오류 (userid 조회):", e)
        return "게스트"

logged_in_user = fetch_userid(logged_in_id)

# ===== 최근 30일 점수 불러오기 =====
def fetch_scores(userid):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

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

        # 튜플 → 리스트 변환 (최신순이니까 reverse)
        scores = [row[0] for row in result][::-1]
        return scores if scores else [0] * 30
    except Exception as e:
        print("DB 오류 (점수 조회):", e)
        return [0] * 30

scores = fetch_scores(logged_in_user)

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

root.geometry(f"{bg_img.width}x{bg_img.height}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=bg_img.width, height=bg_img.height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# ===== 폰트 통일 =====
custom_font = tkFont.Font(family="DungGeunMo", size=14)

# 유저 아이디 표시
canvas.create_text(180, 160, text=f"{logged_in_user}", fill="black",
                   font=custom_font, anchor="w")

# ===== 잔디 그래프 (최근 30일) =====
start_x, start_y = 150, 250
box_size = 15
padding = 3

for i, score in enumerate(scores):
    x = start_x + (i % 10) * (box_size + padding)
    y = start_y + (i // 10) * (box_size + padding)
    color = score_to_color(score)
    canvas.create_rectangle(x, y, x + box_size, y + box_size, fill=color, outline="")

# 🔑 이미지 참조 유지
root.bg_photo = bg_photo

root.mainloop()
