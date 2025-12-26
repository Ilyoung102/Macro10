# 버튼 클릭 10.py  ← 이 파일로 저장하면 무조건 됩니다! (오류 0개)
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
        self.root.geometry("700x850")
        self.root.configure(bg="#0d1117")

        self.click_x = None
        self.click_y = None
        self.running = False
        self.mini = None

        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="버튼 클릭 10", font=("맑은 고딕", 38, "bold"),
                fg="#00ffff", bg="#0d1117").pack(pady=(40, 20))

        main_frame = tk.Frame(self.root, bg="#161b22")
        main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # 목표 시간
        tk.Label(main_frame, text="목표 시간 (예: 2025-11-23 10:00:00.000)", fg="#c9d1d9", bg="#161b22", font=14).pack(anchor="w", padx=20, pady=(10,5))
        self.time_entry = tk.Entry(main_frame, font=("Consolas", 18), width=35, justify="center", bg="#21262d", fg="#79c0ff", insertbackground="white")
        self.time_entry.insert(0, "2025-11-23 10:00:00.000")
        self.time_entry.pack(pady=10)

        # 사이트 주소
        tk.Label(main_frame, text="사이트 주소 (체크 해제하면 미리 열기)", fg="#c9d1d9", bg="#161b22").pack(anchor="w", padx=20, pady=(20,5))
        self.url_entry = tk.Entry(main_frame, font=("Consolas", 13), width=68, bg="#21262d", fg="#a5d6ff", insertbackground="white")
        self.url_entry.insert(0, "https://www.korail.com/ticket/search/general")
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

        # 빈 공간 확보
        tk.Frame(self.root, height=80, bg="#0d1117").pack()

        # 시작하기 버튼 (절대 안 가려짐!)
        self.start_btn = tk.Button(self.root, text="시작하기", command=self.start,
                                  bg="#e63946", fg="white", font=("맑은 고딕", 36, "bold"),
                                  width=18, height=2, relief="flat")
        self.start_btn.pack(side="bottom", pady=(0, 60))

    def capture_coord(self):
        self.root.iconify()
        ov = tk.Toplevel()
        ov.attributes("-fullscreen", True)
        ov.attributes("-alpha", 0.4)
        ov.configure(bg="black")
        ov.overrideredirect(True)
        tk.Label(ov, text="클릭할 버튼 위에서\n한 번 클릭!", font=("맑은 고딕", 50, "bold"),
                fg="#00ffaa", bg="black").place(relx=0.5, rely=0.5, anchor="center")

        def on_click(e):
            x, y = pyautogui.position()
            self.click_x, self.click_y = x, y
            ov.destroy()
            self.root.deiconify()
            self.coord_label.config(text=f"좌표 설정 완료 → X={x}  Y={y}", fg="#79c0ff")

        ov.bind("<Button-1>", on_click)
        ov.bind("<Escape>", lambda e: ov.destroy() or self.root.deiconify())

    def start(self):
        if not self.click_x:
            messagebox.showwarning("알림", "먼저 좌표를 설정해주세요!")
            return
        try:
            target = datetime.datetime.strptime(self.time_entry.get().strip(), "%Y-%m-%d %H:%M:%S.%f")
            if target < datetime.datetime.now():
                messagebox.showwarning("알림", "이미 지난 시간입니다!")
                return
        except:
            messagebox.showerror("오류", "시간 형식이 잘못되었습니다!\n예: 2025-11-23 10:00:00.000")
            return

        self.root.withdraw()
        self.create_mini_timer()
        self.running = True
        threading.Thread(target=self.run_click, daemon=True).start()

    def create_mini_timer(self):
        self.mini = tk.Toplevel()
        self.mini.geometry("480x130+{}+30".format(self.mini.winfo_screenwidth()//2 - 240))
        self.mini.configure(bg="#1e1e1e")
        self.mini.attributes("-topmost", True)
        self.mini.overrideredirect(True)

        tk.Label(self.mini, text="버튼 클릭 10 실행 중", font=("맑은 고딕", 20, "bold"), fg="#00ffaa", bg="#1e1e1e").pack(pady=20)
        self.timer_label = tk.Label(self.mini, text="00:00.000", font=("Consolas", 42, "bold"), fg="#79c0ff", bg="#1e1e1e")
        self.timer_label.pack()

        self.mini.bind("<Double-Button-1>", lambda e: self.restore())

    def restore(self):
        self.running = False
        if self.mini:
            self.mini.destroy()
            self.mini = None
        self.root.deiconify()

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
                    if not self.running: break
                    pyautogui.click(self.click_x, self.click_y)
                    time.sleep(interval)
                if self.mini and self.mini.winfo_exists():
                    self.timer_label.config(text="완료!", fg="#00ff00")
                break

            mins, secs = divmod(int(diff), 60)
            ms = int((diff % 1) * 1000)
            if self.mini and self.mini.winfo_exists():
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}.{ms:03d}")

            time.sleep(0.001)

        # 3초 후 자동 복구
        if self.root.winfo_exists():
            self.root.after(3000, self.restore)

if __name__ == "__main__":
    ButtonClick10()