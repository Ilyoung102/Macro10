# REAL_FINAL_v10.py  ← 이 파일만 저장하면 무조건 보입니다!
import tkinter as tk
from tkinter import messagebox
import pyautogui
import webbrowser
import datetime
import threading
import time

pyautogui.PAUSE = 0.001
pyautogui.FAILSAFE = False

class RealFinalV10:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("최종 병기 v10 - 버튼 절대 안 잘림")
        self.root.geometry("840x960")        # 아주 넉넉하게!
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

        self.target_time = None
        self.click_x = self.click_y = None
        self.running = False
        self.mini = None

        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        # ===== 상단 제목 =====
        tk.Label(self.root, text="초고속 예매 병기 v10", font=("맑은 고딭", 26, "bold"),
                fg="#00ffff", bg="#0d1117").pack(pady=(30, 20))

        # ===== 메인 프레임 =====
        main = tk.Frame(self.root, bg="#161b22")
        main.pack(pady=20, padx=40, fill="both", expand=True)

        # 목표 시간
        tk.Label(main, text="목표 시간 (밀리초 필수)", fg="#c9d1d9", bg="#161b22", font=12).pack(anchor="w", padx=20, pady=(10,5))
        self.time_entry = tk.Entry(main, font=("Consolas", 16), width=34, justify="center", bg="#21262d", fg="#79c0ff")
        self.time_entry.insert(0, "2025-11-23 10:00:00.000")
        self.time_entry.pack(pady=10)

        # URL + 체크박스
        tk.Label(main, text="사이트 주소 (체크 해제 = 미리 열어놓기 추천)", fg="#c9d1d9", bg="#161b22").pack(anchor="w", padx=20, pady=(15,5))
        self.url_entry = tk.Entry(main, font=("Consolas", 12), width=66, bg="#21262d", fg="#a5d6ff")
        self.url_entry.insert(0, "https://www.korail.com/ticket/search/general")
        self.url_entry.pack(pady=8)

        self.open_site_var = tk.BooleanVar(value=False)
        tk.Checkbutton(main, text="시간 되면 사이트 자동 열기", variable=self.open_site_var,
                      fg="#58a6ff", bg="#161b22", selectcolor="#161b22").pack(anchor="w", padx=20, pady=10)

        # 좌표 설정
        tk.Label(main, text="클릭 위치 설정", font=("맑은 고딕", 16, "bold"), fg="#ffa500", bg="#161b22").pack(anchor="w", padx=20, pady=(30,10))
        btn_coord = tk.Button(main, text="좌표 잡기 시작", command=self.start_overlay,
                             bg="#238636", fg="white", font=("bold", 14), width=24, height=2, relief="flat")
        btn_coord.pack(pady=15)

        self.coord_label = tk.Label(main, text="좌표: 아직 없음", font=("Consolas", 18, "bold"), fg="#ff5555", bg="#161b22")
        self.coord_label.pack(pady=20)

        # 클릭 설정
        tk.Label(main, text="클릭 횟수 / 간격", font=("맑은 고딕", 14, "bold"), fg="#ffa500", bg="#161b22").pack(anchor="w", padx=20, pady=(20,5))
        opt = tk.Frame(main, bg="#161b22"); opt.pack(pady=12)
        tk.Label(opt, text="횟수:", fg="#ccc", bg="#161b22").grid(row=0, column=0, padx=15)
        self.click_count = tk.Spinbox(opt, from_=1, to=30, width=6, font=12); self.click_count.grid(row=0, column=1, padx=10)
        self.click_count.delete(0,"end"); self.click_count.insert(0,"5")
        tk.Label(opt, text="간격(초):", fg="#ccc", bg="#161b22").grid(row=0, column=2, padx=15)
        self.interval = tk.Entry(opt, width=10, font=12); self.interval.grid(row=0, column=3, padx=10)
        self.interval.insert(0,"0.03")

        # 카운트다운 (항상 보이게)
        self.countdown_label = tk.Label(self.root, text="대기 중", font=("Consolas", 28, "bold"), fg="#79c0ff", bg="#0d1117")
        self.countdown_label.pack(pady=(30, 40))

        # ===== 시작하기 버튼 강제 하단 고정 =====
        bottom_frame = tk.Frame(self.root, bg="#0d1117")
        bottom_frame.pack(side="bottom", pady=(0, 40))  # 제일 아래로!

        self.start_btn = tk.Button(bottom_frame, text="시작하기", command=self.start_macro,
                                  bg="#e63946", fg="white", font=("맑은 고딕", 24, "bold"),
                                  width=26, height=3, relief="flat", state="disabled")
        self.start_btn.pack()

        # 마우스 오버 효과
        self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg="#ff3366"))
        self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg="#e63946"))

    def start_overlay(self):
        self.root.iconify()
        ov = tk.Toplevel()
        ov.attributes("-fullscreen", True)
        ov.attributes("-alpha", 0.4)
        ov.configure(bg="black")
        ov.overrideredirect(True)
        tk.Label(ov, text="버튼 위에서 클릭!\nESC로 취소", font=("맑은 고딕", 44, "bold"),
                fg="#00ffaa", bg="black").place(relx=0.5, rely=0.5, anchor="center")
        ov.bind("<Button-1>", lambda e: self.set_pos(ov))
        ov.bind("<Escape>", lambda e: ov.destroy() or self.root.deiconify())

    def set_pos(self, ov):
        x, y = pyautogui.position()
        self.click_x, self.click_y = x, y
        ov.destroy()
        self.root.deiconify()
        self.coord_label.config(text=f"좌표 완료 → X={x} Y={y}", fg="#79c0ff")
        self.start_btn.config(state="normal")

    def start_macro(self):
        if not self.click_x: return
        try:
            self.target_time = datetime.datetime.strptime(self.time_entry.get().strip(), "%Y-%m-%d %H:%M:%S.%f")
        except:
            messagebox.showerror("오류", "시간 형식 확인!")
            return

        self.root.withdraw()
        self.create_mini()
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def create_mini(self):
        self.mini = tk.Toplevel()
        self.mini.geometry("400x100")
        self.mini.configure(bg="#1e1e1e")
        self.mini.attributes("-topmost", True)
        self.mini.overrideredirect(True)
        self.mini.geometry("+{}+{}".format(
            self.mini.winfo_screenwidth()//2 - 200, 40))  # 상단 중앙

        tk.Label(self.mini, text="실행 중 - 더블클릭으로 복구", font=("맑은 고딕", 14), fg="#00ffaa", bg="#1e1e1e").pack(pady=10)
        self.mini_label = tk.Label(self.mini, text="00:00.000", font=("Consolas", 32, "bold"), fg="#79c0ff", bg="#1e1e1e")
        self.mini_label.pack()
        self.mini.bind("<Double-Button-1>", lambda e: self.restore())

    def restore(self):
        if self.mini: self.mini.destroy()
        self.root.deiconify()
        self.running = False

    def run(self):
        url = self.url_entry.get().strip()
        open_site = self.open_site_var.get()
        clicks = int(self.click_count.get())
        interval = float(self.interval.get() or "0.03")

        while self.running:
            diff = (self.target_time - datetime.datetime.now()).total_seconds()
            if diff <= 0:
                if open_site and url:
                    webbrowser.open_new_tab(url)
                    time.sleep(1.3)
                for _ in range(clicks):
                    pyautogui.click(self.click_x, self.click_y)
                    time.sleep(interval)
                if self.mini: self.mini_label.config(text="완료!", fg="#00ff00")
                break

            mins, secs = divmod(int(diff), 60)
            ms = int((diff % 1)*1000)
            text = f"{mins:02d}:{secs:02d}.{ms:03d}"
            if self.mini: self.mini_label.config(text=text)

            time.sleep(0.0005)

        self.root.after(3000, self.restore)

if __name__ == "__main__":
    RealFinalV10()