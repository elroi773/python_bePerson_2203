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

# 아이디 입력창 (투명 느낌)
id_entry = tk.Entry(root, textvariable=id_var,
                    font=("Arial", 14),
                    fg="black", bg="#dff",   # 배경 이미지 색상과 비슷하게
                    bd=0, highlightthickness=0,
                    justify="center", insertbackground="black")
id_entry.place(x=230, y=150, width=140, height=25)

# 비밀번호 입력창
pw_entry = tk.Entry(root, textvariable=pw_var,
                    font=("Arial", 14),
                    show="*",
                    fg="black", bg="#dff",
                    bd=0, highlightthickness=0,
                    justify="center", insertbackground="black")
pw_entry.place(x=230, y=195, width=140, height=25)

# 버튼 이미지
submit_img = PhotoImage(file="./img/join_submit.png")   # 제출 버튼 이미지

# 버튼 동작
def submit_action():
    print("아이디:", id_var.get())
    print("비밀번호:", pw_var.get())

# 제출 버튼
submit_btn = tk.Button(root, image=submit_img, command=submit_action,
                       bd=0, highlightthickness=0, relief="flat", cursor="hand2")
submit_btn.place(x=230, y=240)

root.mainloop()
