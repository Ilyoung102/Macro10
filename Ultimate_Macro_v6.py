# Ultimate_Macro_v6.py  ← 이 이름으로 저장하세요!
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import webbrowser
import datetime
import threading
import time

pyautogui.PAUSE = 0.005

class UltimateMacro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("정밀 타이밍 매크로 v6.0 - 모든 사이트 지원")
        self.root.geometry("760x720")           # 창 크게!
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.target_time = None
        self.click_x = None
        self.click_y = None
        self.running = False
        self.overlay = None

        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')

        # 제목
        title = tk.Label(self.root, text="정밀 타이밍 자동 클릭 매크로", 
                        font=("맑은 고딕", 20, "bold"), fg="#00D4FF", bg="#121212")
        title.pack(pady=25)

        main_frame = tk.Frame(self.root, bg="#1e1e1e", relief="flat", bd=5)
        main_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # 목표 시간
        tk.Label(main_frame, text="목표 시간 (밀리초까지 입력)", font=("맑은 고딕", 11), 
                fg="#cccccc", bg="#1e1e1e").pack(anchor="w", padx=25, pady=(10,5))
        self.time_entry = tk.Entry(main_frame, font=("Consolas", 14), width=32, justify="center", bg="#2d2d2d", fg="#00ff80", insertbackground="white")
        self.time_entry.insert(0, "2025-11-23 10:00:00.000")
        self.time_entry.pack(pady=8)

        # URL 입력 (자유롭게 변경 가능!)
        tk.Label(main_frame, text="사이트 주소 (URL)", font=("맑은 고딕", 11), 
                fg="#cccccc", bg="#1e1e1e").pack(anchor="w", padx=25, pady=(20,5))
        self.url_entry = tk.Entry(main_frame, font=("Consolas", 12), width=60, bg="#2d2d2d", fg="#88ff88", insertbackground="white")
        self.url_entry.insert(0, "https://www.korail.com/ticket/search/general")
        self.url_entry.pack(pady=8)

        # 좌표 설정 섹션
        tk.Label(main_frame, text="클릭할 버튼 좌표 설정", font=("맑은 고딕", 13, "bold"), 
                fg="#FFD60A", bg="#1e1e1e").pack(anchor="w", padx=25, pady=(30,10))

        # 세련된 좌표 잡기 버튼 (작고 예쁘게)
        self.coord_btn = tk.Button(main_frame, text="좌표 잡기 시작", 
                                  command=self.start_overlay_capture,
                                  bg="#4361EE", fg="white", font=("맑은 고딕", 11, "bold"),
                                  width=20, height=2, relief="flat", cursor="hand2")
        self.coord_btn.pack(pady=12)

        # 좌표 표시 라벨
        self.coord_label = tk.Label(main_frame, text="좌표: 아직 설정되지 않음", 
                                   font=("Consolas", 15, "bold"), fg="#FF6B6B", bg="#1e1e1e")
        self.coord_label.pack(pady=15)

        # 카운트다운
        self.countdown_label = tk.Label(self.root, text="대기 중...", 
                                       font=("Consolas", 18, "bold"), fg="#FFA500", bg="#121212")
        self.countdown_label.pack(pady=25)

        # 시작하기 버튼 (크고 잘 보이게)
        btn_frame = tk.Frame(self.root, bg="#121212")
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="시작하기", command=self.start_macro,
                                  bg="#2ECC71", fg="white", font=("맑은 고딕", 16, "bold"),
                                  width=16, height=2, state="disabled", relief="flat", cursor="hand2")
        self.start_btn.pack(side="left", padx=15)

        self.stop_btn = tk.Button(btn_frame, text="정지", command=self.stop_macro,
                                 bg="#E74C3C", fg="white", font=("bold", 14), width=10, height=2, relief="flat")
        self.stop_btn.pack(side="left", padx=15)

    def start_overlay_capture(self):
        if self.overlay:
            return
        self.root.iconify()

        self.overlay = tk.Toplevel()
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.4)
        self.overlay.configure(bg="#0a0a0a")
        self.overlay.overrideredirect(True)

        guide_text = ("아래 사이트에서 클릭할 버튼 위에 마우스를 올리고\n"
                     "한 번 클릭하세요!\n\n"
                     "ESC 키를 누르면 취소됩니다.")
        guide = tk.Label(self.overlay, text=guide_text, font=("맑은 고딕", 32, "bold"),
                        fg="#00FF88", bg="#0a0a0a", justify="center")
        guide.place(relx=0.5, rely=0.5, anchor="center")

        self.overlay.bind("<Button-1>", self.capture_click)
        self.overlay.bind("<Escape>", lambda e: self.cancel_capture())

    def capture_click(self, event):
        x, y = pyautogui.position()
        self.click_x, self.click_y = x, y
        self.close_overlay()
        self.coord_label.config(text=f"좌표 설정 완료 → X={x}  Y={y}", fg="#2ECC71")
        self.start_btn.config(state="normal")

    def cancel_capture(self):
        self.close_overlay()

    def close_overlay(self):
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None
        self.root.deiconify()

    def start_macro(self):
        if self.running or not self.click_x:
            return

        try:
            self.target_time = datetime.datetime.strptime(self.time_entry.get().strip(), "%Y-%m-%d %H:%M:%S.%f")
        except:
            messagebox.showerror("시간 오류", "형식: 2025-11-23 10:00:00.000")
            return

        if self.target_time < datetime.datetime.now():
            messagebox.showwarning("경고", "이미 지난 시간입니다!")
            return

        self.running = True
        self.start_btn.config(text="실행 중...", state="disabled")
        threading.Thread(target=self.run_macro, daemon=True).start()

    def run_macro(self):
        url = self.url_entry.get().strip()

        while self.running:
            diff = (self.target_time - datetime.datetime.now()).total_seconds()

            if diff <= 0:
                self.countdown_label.config(text="실행! 사이트 열고 클릭 중...", fg="#00FF00")
                webbrowser.open_new_tab(url)
                time.sleep(4.0)

                pyautogui.click(self.click_x, self.click_y)
                time.sleep(0.3)
                pyautogui.click(self.click_x, self.click_y)
                time.sleep(0.5)
                pyautogui.press("enter")

                self.countdown_label.config(text="성공! 클릭 완료", fg="#2ECC71")
                break

            mins = int(diff // 60)
            secs = int(diff % 60)
            ms = int((diff % 1) * 1000)
            self.countdown_label.config(text=f"남은 시간: {mins:02d}분 {secs:02d}.{ms:03d}초")

            time.sleep(0.001 if diff < 1 else 0.05)

        self.running = False
        self.start_btn.config(text="시작하기", state="normal" if self.click_x else "disabled")

    def stop_macro(self):
        self.running = False
        self.start_btn.config(text="시작하기", state="normal" if self.click_x else "disabled")
        self.countdown_label.config(text="정지됨")

# 실행
if __name__ == "__main__":
    UltimateMacro()