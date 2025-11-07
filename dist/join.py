import tkinter as tk
from tkinter import PhotoImage
from tkinter import font as tkFont
import subprocess  # 다른 스크립트 실행용
from db import connect_db

root = tk.Tk()
root.title("회원가입 화면")

# 배경 이미지
bg_img = PhotoImage(file="./img/join_page.png")
canvas = tk.Canvas(root, width=bg_img.width(), height=bg_img.height(), highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=bg_img)

# 폰트
custom_font = tkFont.Font(family="./DungGeunMo.ttf", size=14)

# 입력값 변수
id_var = tk.StringVar()
pw_var = tk.StringVar()

# placeholder 함수
def add_placeholder(entry, placeholder_text, is_password=False):
    entry.insert(0, placeholder_text)
    entry.config(fg="gray")
    if is_password: entry.config(show="")

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg="black")
            if is_password: entry.config(show="*")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg="gray")
            if is_password: entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# 아이디 입력창
id_entry = tk.Entry(root, textvariable=id_var, font=custom_font, fg="black", bg="#bdefff",
                    bd=0, highlightthickness=0, justify="center", insertbackground="black")
id_entry.place(x=180, y=160, width=200, height=30)
add_placeholder(id_entry, "아이디")

# 비밀번호 입력창
pw_entry = tk.Entry(root, textvariable=pw_var, font=custom_font, fg="black", bg="#bdefff",
                    bd=0, highlightthickness=0, justify="center", insertbackground="black")
pw_entry.place(x=180, y=200, width=200, height=30)
add_placeholder(pw_entry, "비밀번호", is_password=True)

# 제출 버튼 이미지
submit_img = PhotoImage(file="./img/submit.png")

def submit_action():
    user_id = id_var.get()
    user_pw = pw_var.get()
    
    # placeholder 값이면 저장하지 않음
    if user_id == "아이디" or user_pw == "비밀번호":
        tk.messagebox.showwarning("경고", "아이디와 비밀번호를 입력하세요!")
        return

    # 1) DB 저장
    try:
        conn = connect_db()
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (userid, userpassword) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, user_pw))
        conn.commit()
        conn.close()
        print("DB 저장 완료:", user_id)
    except Exception as e:
        print("DB 저장 오류:", e)
        tk.messagebox.showerror("오류", "DB 저장 실패")
        return

    # 2) takephoto.py 실행
    root.destroy()  # 현재 창 닫기
    subprocess.run(["python", "takephoto.py"])  # 새 창 실행

submit_btn = tk.Button(root, image=submit_img, command=submit_action,
                       bd=0, highlightthickness=0, relief="flat", cursor="hand2")
submit_btn.place(x=180, y=240)

root.mainloop()
