import tkinter as tk
from tkinter import PhotoImage
from tkinter import font as tkFont
import pymysql
import subprocess
import sys

root = tk.Tk()
root.title("로그인 화면")

# 배경 이미지 로드
bg_img = PhotoImage(file="./img/login_page.png")
canvas = tk.Canvas(root, width=bg_img.width(), height=bg_img.height(), highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=bg_img)

custom_font = tkFont.Font(family="DungGeunMo", size=14)

id_var = tk.StringVar()
pw_var = tk.StringVar()

def add_placeholder(entry, placeholder_text, is_password=False):
    entry.insert(0, placeholder_text)
    entry.config(fg="gray")
    if is_password:
        entry.config(show="")

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg="black")
            if is_password:
                entry.config(show="*")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg="gray")
            if is_password:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

id_entry = tk.Entry(root, textvariable=id_var,
                    font=custom_font, fg="black", bg="#bdefff",
                    bd=0, highlightthickness=0,
                    justify="center", insertbackground="black")
id_entry.place(x=180, y=160, width=200, height=30)
add_placeholder(id_entry, "아이디")

pw_entry = tk.Entry(root, textvariable=pw_var,
                    font=custom_font, fg="black", bg="#bdefff",
                    bd=0, highlightthickness=0,
                    justify="center", insertbackground="black")
pw_entry.place(x=180, y=200, width=200, height=30)
add_placeholder(pw_entry, "비밀번호", is_password=True)

submit_img = PhotoImage(file="./img/submit.png")

def submit_action():
    userid = id_var.get()
    userpassword = pw_var.get()

    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            passwd="Mysql4344!",
            database="bePerson",
            charset="utf8mb4"
        )
        cursor = conn.cursor()
        sql = "SELECT id, userid FROM USERS WHERE userid = %s AND userpassword = %s"
        cursor.execute(sql, (userid, userpassword))
        result = cursor.fetchone()

        if result:
            user_id_pk, user_id_str = result  # ✅ DB에서 PK(id)와 userid 둘 다 가져오기
            print(f"로그인 성공: id={user_id_pk}, userid={user_id_str}")

            root.destroy()
            # ✅ id(PK)와 userid 둘 다 인자로 전달
            subprocess.Popen(["python", "login_Success.py", str(user_id_pk), user_id_str])

        else:
            print("로그인 실패")
            fail_label = tk.Label(root, text="아이디 또는 비밀번호 오류", fg="red", font=custom_font, bg="#ffffff")
            fail_label.place(x=180, y=280)

        conn.close()

    except Exception as e:
        print("DB 연결 오류:", e)
        error_label = tk.Label(root, text="DB 연결 실패", fg="red", font=custom_font, bg="#ffffff")
        error_label.place(x=200, y=280)

submit_btn = tk.Button(root, image=submit_img, command=submit_action,
                       bd=0, highlightthickness=0, relief="flat", cursor="hand2")
submit_btn.place(x=180, y=240)

root.mainloop()
