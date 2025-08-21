import tkinter as tk
from tkinter import PhotoImage

root = tk.Tk()
root.title("로그인 화면")

# 배경 이미지 로드
bg_img = PhotoImage(file="./img/join_page.png")
canvas = tk.Canvas(root, width=bg_img.width(), height=bg_img.height(), highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=bg_img)

# 입력값 저장 변수
id_var = tk.StringVar()
pw_var = tk.StringVar()

# 아이디 입력창 (배경 색과 맞추기)
id_entry = tk.Entry(root, textvariable=id_var,
                    font=("Arial", 14),
                    fg="black", bg="#bdefff",  # 배경 버튼 색상 직접 맞추기
                    bd=0, highlightthickness=0,
                    justify="center", insertbackground="black")
id_entry.place(x=180, y=200, width=200, height=30)

# 비밀번호 입력창
pw_entry = tk.Entry(root, textvariable=pw_var,
                    font=("Arial", 14),
                    show="*",
                    fg="black", bg="#bdefff",
                    bd=0, highlightthickness=0,
                    justify="center", insertbackground="black")
pw_entry.place(x=180, y=160, width=200, height=30)

# 제출 버튼 이미지
submit_img = PhotoImage(file="./img/join_submit.png")

def submit_action():
    print("아이디:", id_var.get())
    print("비밀번호:", pw_var.get())

submit_btn = tk.Button(root, image=submit_img, command=submit_action,
                       bd=0, highlightthickness=0, relief="flat", cursor="hand2")
submit_btn.place(x=180, y=240)

root.mainloop()
