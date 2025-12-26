# Korail_Macro_v5_ClickToSet.py  ← 이 이름으로 저장하세요!
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import webbrowser
import datetime
import threading
import time

pyautogui.PAUSE = 0.005

class KorailMacroV5:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("코레일 매크로 v5 - 클릭 한 번으로 좌표 설정!")
        self.root.geometry("720x660")
        self.root.configure(bg="#1e272e")
        self.root.resizable(False, False)

        self.target_time = None
        self.click_x = None
        self.click_y = None
        self.running = False

        # 투명 오버레이 창 (좌표 잡기용)
        self.overlay = None

        self.create_main_ui()
        self.root.mainloop()

    def create_main_ui(self):
        # 제목
        title = tk.Label(self.root, text="코레일 열차조회 자동 클릭 매크로", font=("맑은 고딕", 18, "bold"), fg="#00d2ff", bg="#1e272e")
        title.pack(pady=20)

        frame = tk.Frame(self.root, bg="#2d3a45", relief="groove", bd=4)
        frame.pack(pady=15, padx=20, fill="both", expand=True)

        # 목표 시간 입력
        tk.Label(frame, text="목표 시간 (예: 2025-11-23 10:00:00.000)", font=("맑은 고딕", 11), fg="white", bg="#2d3a45").pack(anchor="w", padx=20, pady=(10,5))
        self.time_entry = tk.Entry(frame, font=("Consolas", 13), width=32, justify="center")
        self.time_entry.insert(0, "2025-11-23 10:00:00.000")
        self.time_entry.pack(pady=5)

        # URL (고정)
        tk.Label(frame, text="사이트: 코레일 일반예매 페이지", font=("맑은 고딕", 10), fg="#a0a0a0", bg="#2d3a45").pack(anchor="w", padx=20, pady=(15,0))
        tk.Label(frame, text="https://www.korail.com/ticket/search/general", font=("Consolas", 10), fg="#00ff80", bg="#2d3a45").pack(anchor="w", padx=25)

        # 좌표 설정 버튼 (핵심!)
        tk.Label(frame, text="좌표 설정 방법 (30초 안에 끝납니다)", font=("맑은 고딕", 12, "bold"), fg="#ffd93d", bg="#2d3a45").pack(anchor="w", padx=20, pady=(25,10))
        
        self.coord_btn = tk.Button(frame, text="좌표 잡기 시작 → 클릭 한 번으로 설정!", 
                                  command=self.start_overlay_capture, bg="#ff3b30", fg="white", 
                                  font=("맑은 고딕", 14, "bold"), height=3, width=40)
        self.coord_btn.pack(pady=15)

        # 현재 좌표 표시
        self.coord_label = tk.Label(frame, text="좌표: 아직 설정되지 않음", font=("Consolas", 14), fg="#ff6b6b", bg="#2d3a45")
        self.coord_label.pack(pady=10)

        # 카운트다운 라벨
        self.countdown_label = tk.Label(self.root, text="대기 중...", font=("Consolas", 16, "bold"), fg="#f39c12", bg="#1e272e")
        self.countdown_label.pack(pady=20)

        # 시작 버튼 (처음엔 비활성화)
        self.start_btn = tk.Button(self.root, text="시작하기", command=self.start_macro, 
                                  bg="#2ecc71", fg="white", font=("bold", 16), width=15, height=2, state="disabled")
        self.start_btn.pack(pady=10)

        # 정지 버튼
        self.stop_btn = tk.Button(self.root, text="정지", command=self.stop_macro, bg="#e74c3c", fg="white", width=10)
        self.stop_btn.pack(pady=5)

    def start_overlay_capture(self):
        """투명 오버레이 띄우고 클릭 한 번으로 좌표 잡기"""
        if self.overlay:
            return

        # 메인 창 최소화
        self.root.iconify()

        # 투명 오버레이 창 생성 (전체 화면)
        self.overlay = tk.Toplevel()
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.3)  # 반투명
        self.overlay.configure(bg="black")
        self.overlay.overrideredirect(True)  # 타이틀바 없애기

        # 안내 문구
        guide = tk.Label(self.overlay, text="코레일 페이지에서\n'열차 조회' 버튼 위에서\n한 번 클릭하세요!", 
                        font=("맑은 고딕", 36, "bold"), fg="#00ff00", bg="black", justify="center")
        guide.place(relx=0.5, rely=0.5, anchor="center")

        # 클릭 이벤트 바인딩
        self.overlay.bind("<Button-1>", self.capture_click)
        self.overlay.bind("<Escape>", lambda e: self.cancel_capture())  # ESC로 취소

    def capture_click(self, event):
        """클릭한 위치 좌표 저장"""
        x, y = pyautogui.position()
        self.click_x, self.click_y = x, y

        # 오버레이 종료
        self.overlay.destroy()
        self.overlay = None

        # 메인 창 복구
        self.root.deiconify()

        # 좌표 표시 & 시작버튼 활성화
        self.coord_label.config(text=f"좌표 설정 완료 → X={x}, Y={y}", fg="#2ecc71")
        self.start_btn.config(state="normal", bg="#2ecc71")

    def cancel_capture(self):
        """ESC 누르면 취소"""
        self.overlay.destroy()
        self.overlay = None
        self.root.deiconify()

    def start_macro(self):
        if self.running or not self.click_x:
            return

        try:
            time_str = self.time_entry.get().strip()
            self.target_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
        except:
            messagebox.showerror("오류", "시간 형식이 틀렸습니다!\n예: 2025-11-23 10:00:00.000")
            return

        if self.target_time < datetime.datetime.now():
            messagebox.showwarning("경고", "이미 지난 시간입니다!")
            return

        self.running = True
        self.start_btn.config(text="실행 중...", state="disabled")
        threading.Thread(target=self.run_macro, daemon=True).start()

    def run_macro(self):
        url = "https://www.korail.com/ticket/search/general"

        while self.running:
            diff = (self.target_time - datetime.datetime.now()).total_seconds()

            if diff <= 0:
                self.countdown_label.config(text="실행 중! 열차조회 클릭!", fg="#00ff00")
                webbrowser.open_new_tab(url)
                time.sleep(3.8)  # 코레일 로딩 대기

                # 클릭 두 번 (보험)
                pyautogui.click(self.click_x, self.click_y)
                time.sleep(0.3)
                pyautogui.click(self.click_x, self.click_y)
                time.sleep(0.5)
                pyautogui.press("enter")

                self.countdown_label.config(text="성공! 조회 완료!", fg="#2ecc71")
                break

            mins = int(diff // 60)
            secs = int(diff % 60)
            ms = int((diff - int(diff)) * 1000)
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
    KorailMacroV5()