import tkinter as tk
from PIL import Image, ImageTk
import subprocess

# 창 생성
root = tk.Tk()
root.title("사람이 되자")
root.geometry("550x450")  # 배경 이미지 크기에 맞게 수정하세요
root.resizable(False, False)

# 배경 이미지 불러오기
bg_img = Image.open("./img/index_background.png")  # 배경 이미지 경로
bg_photo = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(root, width=bg_img.width, height=bg_img.height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# 버튼 클릭 시 실행 함수
def open_login():
    subprocess.Popen(["python", "login.py"])

def open_join():
    subprocess.Popen(["python", "join.py"])

# 버튼 이미지 불러오기
btn_login_img = ImageTk.PhotoImage(Image.open("./img/login.png"))   # 로그인 버튼 이미지
btn_join_img = ImageTk.PhotoImage(Image.open("./img/join.png"))     # 회원가입 버튼 이미지
btn_title_img = ImageTk.PhotoImage(Image.open("./img/title.png"))   # 사람이 되자 버튼 이미지

# 버튼 배치 (좌표는 이미지 위치에 맞게 수정)
canvas.create_image(270, 200, image=btn_title_img, anchor="center")

# 버튼 먼저 생성
login_btn = tk.Button(root, image=btn_login_img, command=open_login, borderwidth=0, highlightthickness=0)
join_btn = tk.Button(root, image=btn_join_img, command=open_join, borderwidth=0, highlightthickness=0)

# 버튼을 캔버스 위에 배치
login_window = canvas.create_window(200, 300, anchor="center", window=login_btn)   # 로그인 버튼 (왼쪽)
join_window = canvas.create_window(340, 300, anchor="center", window=join_btn)    # 회원가입 버튼 (오른쪽)


root.mainloop()
