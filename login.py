import tkinter as tk
from tkinter import PhotoImage
from tkinter import font as tkFont

root = tk.Tk()
root.title("로그인 화면")

# 배경 이미지 로드
bg_img = PhotoImage(file="./img/login_page.png")
canvas = tk.Canvas(root, width=bg_img.width(), height=bg_img.height(), highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=bg_img)

# ==== 설치된 폰트 불러오기 ====
custom_font = tkFont.Font(family="./DungGeunMo.ttf", size=14)

# 입력값 저장 변수
id_var = tk.StringVar()
pw_var = tk.StringVar()

# ---- Placeholder 함수 ----
def add_placeholder(entry, placeholder_text, is_password=False):
    entry.insert(0, placeholder_text)
    entry.config(fg="gray")
    if is_password:
        entry.config(show="")  # placeholder는 보이게

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg="black")
            if is_password:
                entry.config(show="*")  # 입력 시 비밀번호는 * 처리

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg="gray")
            if is_password:
                entry.config(show="")  # placeholder일 땐 평문 보이게

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ---- 아이디 입력창 ----
id_entry = tk.Entry(root, textvariable=id_var,
                    font=custom_font,
                    fg="black", bg="#bdefff",
                    bd=0, highlightthickness=0,
                    justify="center", insertbackground="black")
id_entry.place(x=180, y=160, width=200, height=30)
add_placeholder(id_entry, "아이디")

# ---- 비밀번호 입력창 ----
pw_entry = tk.Entry(root, textvariable=pw_var,
                    font=custom_font,
                    fg="black", bg="#bdefff",
                    bd=0, highlightthickness=0,
                    justify="center", insertbackground="black")
pw_entry.place(x=180, y=200, width=200, height=30)
add_placeholder(pw_entry, "비밀번호", is_password=True)

# 제출 버튼 이미지
submit_img = PhotoImage(file="./img/submit.png")

def submit_action():
    print("아이디:", id_var.get())
    print("비밀번호:", pw_var.get())

submit_btn = tk.Button(root, image=submit_img, command=submit_action,
                       bd=0, highlightthickness=0, relief="flat", cursor="hand2")
submit_btn.place(x=180, y=240)

root.mainloop()
