import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys

# 인자 받기
if len(sys.argv) > 2:
    logged_in_id = int(sys.argv[1])   # USERS.id (PK)
    logged_in_user = sys.argv[2]      # userid
else:
    logged_in_id = -1
    logged_in_user = "게스트"

root = tk.Tk()
root.title("사람이 되자")
root.geometry("550x450")
root.resizable(False, False)

# === 배경 이미지 ===
bg_img = Image.open("./img/login_Success.png")
bg_photo = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(root, width=bg_img.width, height=bg_img.height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# === 텍스트 표시 ===
canvas.create_text(275, 80, text=f"환영합니다, {logged_in_user}님!",
                   fill="black", font=("맑은 고딕", 14, "bold"))

# === 버튼 함수 ===
def run_test():
    subprocess.Popen(["python", "test.py", str(logged_in_id), logged_in_user])

def go_records():
    subprocess.Popen(["python", "myrecords.py", str(logged_in_id), logged_in_user])

# === 버튼 이미지 ===
btn1_img = ImageTk.PhotoImage(Image.open("./img/start_program_btn.png"))
btn2_img = ImageTk.PhotoImage(Image.open("./img/go_to_record.png"))

# === 버튼 생성 ===
btn1 = tk.Button(root, image=btn1_img, command=run_test,
                 bd=0, highlightthickness=0, relief="flat", cursor="hand2")
btn2 = tk.Button(root, image=btn2_img, command=go_records,
                 bd=0, highlightthickness=0, relief="flat", cursor="hand2")

# === 캔버스 위에 버튼 배치 ===
canvas.create_window(275, 200, window=btn1)
canvas.create_window(275, 270, window=btn2)

# 🔑 PhotoImage 참조 유지
root.bg_photo = bg_photo
root.btn1_img = btn1_img
root.btn2_img = btn2_img

root.mainloop()
