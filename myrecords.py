import tkinter as tk
from PIL import Image, ImageTk
import pymysql
import sys
from tkinter import font as tkFont, messagebox

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
def fetch_scores(user_pk):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = """
            SELECT score 
            FROM RECORDS
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 30
        """
        cursor.execute(sql, (user_pk,))
        result = cursor.fetchall()
        conn.close()

        scores = [row[0] for row in result][::-1]
        return scores if scores else [0] * 30
    except Exception as e:
        print("DB 오류 (점수 조회):", e)
        return [0] * 30

scores = fetch_scores(logged_in_id)

# ===== 점수 → 색상 매핑 =====
def score_to_color(score):
    if score == 0:
        return "#ebedf0"
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

# 툴팁(Label)
tooltip = tk.Label(root, text="", bg="#333", fg="white",
                   font=("DungGeunMo", 11), bd=0, padx=5, pady=2)
tooltip.place_forget()

def show_tooltip(event, score):
    tooltip.config(text=f"점수: {score}")
    tooltip.place(x=event.x_root - root.winfo_rootx() + 15,
                  y=event.y_root - root.winfo_rooty() - 10)

def hide_tooltip(event):
    tooltip.place_forget()

for i, score in enumerate(scores):
    x = start_x + (i % 10) * (box_size + padding)
    y = start_y + (i // 10) * (box_size + padding)
    color = score_to_color(score)
    rect = canvas.create_rectangle(x, y, x + box_size, y + box_size,
                                   fill=color, outline="")
    canvas.tag_bind(rect, "<Enter>", lambda e, s=score: show_tooltip(e, s))
    canvas.tag_bind(rect, "<Leave>", hide_tooltip)

# =========================================================
# ✅ [추가] REASONS 테이블에서 사유 불러오기
# =========================================================
def fetch_reasons(user_pk):
    if not user_pk:
        return ["게스트는 사유 기록이 없습니다."]
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """
            SELECT reason_text, created_at
            FROM REASONS
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (user_pk,))
        results = cursor.fetchall()
        conn.close()
        if not results:
            return ["등록된 사유가 없습니다."]
        return [f"{created_at.strftime('%Y-%m-%d %H:%M')} — {reason_text}"
                for reason_text, created_at in results]
    except Exception as e:
        print("DB 오류 (사유 조회):", e)
        return ["사유를 불러올 수 없습니다."]

# =========================================================
# ✅ [추가] 사유 보기 버튼 + 팝업창
# =========================================================
def show_reasons():
    reasons = fetch_reasons(logged_in_id)
    popup = tk.Toplevel(root)
    popup.title("나의 사유 기록")
    popup.geometry("400x400")
    popup.resizable(False, False)

    tk.Label(popup, text="📝 나의 사유 기록", font=("DungGeunMo", 14, "bold")).pack(pady=10)

    frame = tk.Frame(popup)
    frame.pack(fill="both", expand=True, padx=15, pady=10)

    text_box = tk.Text(frame, wrap="word", font=("DungGeunMo", 12))
    text_box.pack(fill="both", expand=True)
    text_box.insert("1.0", "\n\n".join(reasons))
    text_box.config(state="disabled")  # 읽기 전용

    tk.Button(popup, text="닫기", command=popup.destroy,
              font=("DungGeunMo", 12)).pack(pady=10)

# ===== 버튼 추가 =====
reason_button = tk.Button(root, text="사유 보기", command=show_reasons,
                          font=("DungGeunMo", 13),
                          bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5)
reason_button_window = canvas.create_window(550, 160, anchor="w", window=reason_button)

# 🔑 이미지 참조 유지
root.bg_photo = bg_photo

root.mainloop()
