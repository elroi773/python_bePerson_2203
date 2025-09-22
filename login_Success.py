import tkinter as tk
from PIL import Image, ImageTk
import subprocess

# 창 생성
root = tk.Tk()
root.title("사람이 되자")
root.geometry("550x450")  # 배경 이미지 크기에 맞게 수정
root.resizable(False, False)

# ===== 배경 이미지 불러오기 =====
bg_img = Image.open("./img/login_Success.png")  # 배경 이미지 경로
bg_photo = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(root, width=bg_img.width, height=bg_img.height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# ===== 버튼 이미지 불러오기 =====
start_btn_img = Image.open("./img/start_program_btn.png")
start_btn_photo = ImageTk.PhotoImage(start_btn_img)

record_btn_img = Image.open("./img/go_to_record.png")
record_btn_photo = ImageTk.PhotoImage(record_btn_img)

# ===== 버튼 동작 함수 =====
def start_program():
    root.destroy()  # 현재 창 닫기
    subprocess.Popen(["python", "test.py"])

def go_to_record():
    root.destroy()  # 현재 창 닫기
    subprocess.Popen(["python", "myrecords.py"])

# ===== 버튼 배치 =====
start_btn = tk.Button(root, image=start_btn_photo, command=start_program,
                      bd=0, highlightthickness=0, relief="flat", cursor="hand2")
start_btn_window = canvas.create_window(150, 350, anchor="nw", window=start_btn)  # 위치 조정 가능

record_btn = tk.Button(root, image=record_btn_photo, command=go_to_record,
                       bd=0, highlightthickness=0, relief="flat", cursor="hand2")
record_btn_window = canvas.create_window(320, 350, anchor="nw", window=record_btn)  # 위치 조정 가능

root.mainloop()
