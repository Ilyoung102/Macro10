# 버튼 클릭 10.py  ← 이걸로 저장하면 무조건 시작하기 버튼 보입니다!
import tkinter as tk
from tkinter import messagebox
import pyautogui
import webbrowser
import datetime
import threading
import time

pyautogui.PAUSE = 0.001
pyautogui.FAILSAFE = False

class ButtonClick10:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("버튼 클릭 10")
        self.root.geometry("800x1000")
        self.root.configure(bg="#0d1117")

        self.click_x = None
        self.click_y = None
        self.running = False

        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        # 제목
        title = tk.Label(self.root, text="매크로 순향", font=("맑은 고딕", 38, "bold"),
                        fg="#00ffff", bg="#0d1117")
        title.pack(pady=(40, 20))

        # 메인 프레임 (위쪽 내용들)
        main_frame = tk.Frame(self.root, bg="#161b22")
        main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # 목표 시간
        tk.Label(main_frame, text="목표 시간 (예: 2025-11-23 10:00:00.000)", fg="#c9d1d9", bg="#161b22", font=14).pack(anchor="w", padx=20, pady=(10,5))
        self.time_entry = tk.Entry(main_frame, font=("Consolas", 18), width=35, justify="center", bg="#21262d", fg="#79c0ff", insertbackground="white")
        self.time_entry.insert(0, "2025-12-25 10:00:00.000")
        self.time_entry.pack(pady=10)

        # 사이트 주소
        tk.Label(main_frame, text="사이트 주소 (체크 해제하면 미리 열기)", fg="#c9d1d9", bg="#161b22").pack(anchor="w", padx=20, pady=(20,5))
        self.url_entry = tk.Entry(main_frame, font=("Consolas", 13), width=68, bg="#21262d", fg="#a5d6ff", insertbackground="white")
        self.url_entry.insert(0, "https://cgv.co.kr/cnm/movieBook")
        self.url_entry.pack(pady=10)

        self.open_site = tk.BooleanVar()
        tk.Checkbutton(main_frame, text="시간 되면 자동으로 사이트 열기", variable=self.open_site,
                      fg="#58a6ff", bg="#161b22", selectcolor="#161b22").pack(anchor="w", padx=20, pady=15)

        # 좌표 잡기
        tk.Label(main_frame, text="클릭할 버튼 위치 설정", font=("맑은 고딕", 16, "bold"), fg="#ffa500", bg="#161b22").pack(anchor="w", padx=20, pady=(30,10))
        tk.Button(main_frame, text="좌표 잡기 시작", command=self.capture_coord,
                 bg="#238636", fg="white", font=("bold", 16), width=32, height=2).pack(pady=15)

        self.coord_label = tk.Label(main_frame, text="좌표: 아직 설정 안 됨", font=("Consolas", 18), fg="#ff5555", bg="#161b22")
        self.coord_label.pack(pady=20)

        # 클릭 설정
        tk.Label(main_frame, text="클릭 횟수        간격(초)", fg="#ffa500", bg="#161b22", font=14).pack(anchor="w", padx=20, pady=(20,5))
        opt = tk.Frame(main_frame, bg="#161b22"); opt.pack(pady=10)
        self.clicks = tk.Spinbox(opt, from_=1, to=50, width=8, font=("Consolas", 14)); self.clicks.grid(row=0, column=0, padx=30)
        self.clicks.delete(0,"end"); self.clicks.insert(0,"7")
        self.interval = tk.Entry(opt, width=12, font=("Consolas", 14)); self.interval.grid(row=0, column=1, padx=30)
        self.interval.insert(0,"0.025")

        # ★★★ 시작하기 버튼을 제일 마지막에 강제로 배치 ★★★
        # 메인 프레임이 끝난 후에 별도로 배치
        bottom_space = tk.Frame(self.root, height=100, bg="#0d1117")
        bottom_space.pack()

        self.start_button = tk.Button(self.root, text="시작하기", command=self.start,
                                     bg="#e63946", fg="white", font=("맑은 고딕", 24, "bold"),
                                     width=18, height=2, relief="flat", bd=0)
        self.start_button.pack(side="bottom", pady=(0, 36))  # 무조건 아래에!

    def capture_coord(self):
        self.root.iconify()
        ov = tk.Toplevel()
        ov.attributes("-fullscreen", True)
        ov.attributes("-alpha", 0.4)
        ov.configure(bg="black")
        ov.overrideredirect(True)
        tk.Label(ov, text="클릭할 버튼 위에서\n한 번 클릭!", font=("맑은 고딕", 50, "bold"),
                fg="#00ffaa", bg="black").place(relx=0.5, rely=0.5, anchor="center")
        ov.bind("<Button-1>", lambda e: self.set_coord(ov))
        ov.bind("<Escape>", lambda e: ov.destroy() or self.root.deiconify())

    def set_coord(self, ov):
        x, y = pyautogui.position()
        self.click_x, self.click_y = x, y
        ov.destroy()
        self.root.deiconify()
        self.coord_label.config(text=f"좌표 설정 완료 → X={x}  Y={y}", fg="#79c0ff")

    def start(self):
        if not self.click_x:
            messagebox.showwarning("경고", "먼저 좌표를 설정해주세요!")
            return
        try:
            target = datetime.datetime.strptime(self.time_entry.get().strip(), "%Y-%m-%d %H:%M:%S.%f")
            if target < datetime.datetime.now():
                messagebox.showwarning("경고", "이미 지난 시간입니다!")
                return
        except:
            messagebox.showerror("오류", "시간 형식이 잘못되었습니다!\n예: 2025-11-23 10:00:00.000")
            return

        self.root.withdraw()
        self.show_mini()
        self.running = True
        threading.Thread(target=self.run_click, daemon=True).start()

    def show_mini(self):
        self.mini = tk.Toplevel()
        self.mini.geometry("480x130+{}+30".format(self.mini.winfo_screenwidth()//2 - 240))
        self.mini.configure(bg="#1e1e1e")
        self.mini.attributes("-topmost", True)
        self.mini.overrideredirect(True)
        tk.Label(self.mini, text="버튼 클릭 10 실행 중", font=("맑은 고딕", 20, "bold"), fg="#00ffaa", bg="#1e1e1e").pack(pady=20)
        self.timer = tk.Label(self.mini, text="00:00.000", font=("Consolas", 42, "bold"), fg="#79c0ff", bg="#1e1e1e")
        self.timer.pack()
        self.mini.bind("<Double-Button-1>", lambda e: self.restore())

    def restore(self):
        if hasattr(self, 'mini') and self.mini:
            self.mini.destroy()
        self.root.deiconify()
        self.running = False

    def run_click(self):
        target = datetime.datetime.strptime(self.time_entry.get().strip(), "%Y-%m-%d %H:%M:%S.%f")
        url = self.url_entry.get().strip()
        clicks = int(self.clicks.get())
        interval = float(self.interval.get() or "0.025")

        while self.running:
            diff = (target - datetime.datetime.now()).total_seconds()
            if diff <= 0:
                if self.open_site.get() and url:
                    webbrowser.open_new_tab(url)
                    time.sleep(1.2)
                for _ in range(clicks):
                    pyautogui.click(self.click_x, self.click_y)
                    time.sleep(interval)
                self.timer.config(text="완료!", fg="#00ff00")
                break

            mins, secs = divmod(int(diff), 60)
            ms = int((diff % 1) * 1000)
            self.timer.config(text=f"{mins:02d}:{secs:02d}.{ms:03d}")
            time.sleep(0.001)

        self.root.after(3000, self.restore)

if __name__ == "__main__":
    ButtonClick10()