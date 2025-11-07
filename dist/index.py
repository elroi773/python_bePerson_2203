import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os, sys

# ✅ exe 환경에서도 안전하게 경로를 불러오는 함수
def resource_path(relative_path):
    """PyInstaller 환경에서도 리소스 경로를 올바르게 찾기"""
    try:
        base_path = sys._MEIPASS  # PyInstaller 임시 폴더
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 창 생성
root = tk.Tk()
root.title("사람이 되자")
root.geometry("550x450")
root.resizable(False, False)

# ✅ 배경 이미지 불러오기 (resource_path 적용)
bg_img = Image.open(resource_path("img/index_background.png"))
bg_photo = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(root, width=bg_img.width, height=bg_img.height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# ✅ 버튼 클릭 시 다른 exe 실행하도록 수정
def open_login():
    subprocess.Popen([sys.executable, resource_path("login.py")])  # Python 실행기 기준으로 실행
    root.destroy()

def open_join():
    subprocess.Popen([sys.executable, resource_path("join.py")])
    root.destroy()

# ✅ 버튼 이미지들도 resource_path 적용
btn_login_img = ImageTk.PhotoImage(Image.open(resource_path("img/login.png")))
btn_join_img = ImageTk.PhotoImage(Image.open(resource_path("img/join.png")))
btn_title_img = ImageTk.PhotoImage(Image.open(resource_path("img/title.png")))

# 버튼 배치
canvas.create_image(270, 200, image=btn_title_img, anchor="center")

login_btn = tk.Button(root, image=btn_login_img, command=open_login, borderwidth=0, highlightthickness=0)
join_btn = tk.Button(root, image=btn_join_img, command=open_join, borderwidth=0, highlightthickness=0)

canvas.create_window(200, 300, anchor="center", window=login_btn)
canvas.create_window(340, 300, anchor="center", window=join_btn)

root.mainloop()
