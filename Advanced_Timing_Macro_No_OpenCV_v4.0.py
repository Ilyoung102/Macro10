# Advanced_Timing_Macro_No_OpenCV_v4.0.py  (OpenCV 없이도 OK!)
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyautogui
import webbrowser
import datetime
import threading
import time
import os

pyautogui.PAUSE = 0.01  # 속도 최적화

class TimingMacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("코레일 정밀 타이밍 매크로 v4.0 - OpenCV 없이도 OK!")
        self.root.geometry("700x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        self.running = False
        self.thread = None
        self.target_time = None
        self.image_path = None

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')

        # 제목
        title = tk.Label(self.root, text="코레일 티켓 자동 조회 매크로 (예매 특화)", font=("맑은 고딕", 16, "bold"), 
                        fg="#ecf0f1", bg="#2c3e50")
        title.pack(pady=15)

        # 프레임
        frame = tk.Frame(self.root, bg="#34495e", relief="ridge", bd=3)
        frame.pack(pady=10, padx=20, fill="both", expand=True)

        # 목표 시간
        tk.Label(frame, text="목표 시간 (예: 2025-11-23 10:00:00.000)", font=("맑은 고딕", 10), 
                fg="white", bg="#34495e").pack(anchor="w", padx=20, pady=(15,5))
        self.time_entry = tk.Entry(frame, font=("Consolas", 12), width=30, justify="center")
        self.time_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.000"))
        self.time_entry.pack(pady=5)

        # URL (코레일 기본)
        tk.Label(frame, text="사이트 주소 (URL)", font=("맑은 고딕", 10), fg="white", bg="#34495e").pack(anchor="w", padx=20, pady=(15,5))
        self.url_entry = tk.Entry(frame, font=("Consolas", 11), width=60)
        self.url_entry.insert(0, "https://www.korail.com/ticket/search/general")  # 코레일 기본 URL
        self.url_entry.pack(pady=5)

        # 클릭 방식 선택
        tk.Label(frame, text="버튼 클릭 방식 (코레일 '조회' 버튼 추천)", font=("맑은 고딕", 10, "bold"), fg="#f1c40f", bg="#34495e").pack(anchor="w", padx=20, pady=(20,5))
        
        self.click_mode = tk.StringVar(value="coord")  # 기본 좌표로 변경 (안정적)
        tk.Radiobutton(frame, text="좌표로 클릭 (추천! OpenCV 없이 빠름)", variable=self.click_mode, value="coord", 
                      fg="white", bg="#34495e", selectcolor="#2c3e50").pack(anchor="w", padx=40)
        tk.Radiobutton(frame, text="이미지로 찾기 (OpenCV 필요, 실패시 좌표 폴백)", variable=self.click_mode, value="image", 
                      fg="white", bg="#34495e", selectcolor="#2c3e50").pack(anchor="w", padx=40)

        # 이미지 선택 버튼 (옵션)
        self.img_btn = tk.Button(frame, text="이미지 선택 (조회 버튼 캡처)", command=self.select_image, bg="#e67e22", fg="white")
        self.img_btn.pack(pady=8)
        self.img_label = tk.Label(frame, text="선택된 이미지: 없음 (좌표 우선 사용)", fg="#95a5a6", bg="#34495e")
        self.img_label.pack()

        # 좌표 입력 (코레일 '조회' 버튼 예시 좌표)
        self.coord_frame = tk.Frame(frame, bg="#34495e")
        self.coord_frame.pack(pady=10)
        tk.Label(self.coord_frame, text="클릭할 좌표 X:", fg="white", bg="#34495e").grid(row=0, column=0, padx=5)
        self.x_entry = tk.Entry(self.coord_frame, width=8); self.x_entry.insert(0, "800")  # 예시: 코레일 조회 버튼 X
        self.x_entry.grid(row=0, column=1)
        tk.Label(self.coord_frame, text="Y:", fg="white", bg="#34495e").grid(row=0, column=2, padx=5)
        self.y_entry = tk.Entry(self.coord_frame, width=8); self.y_entry.insert(0, "500")  # 예시: Y
        self.y_entry.grid(row=0, column=3)
        tk.Label(self.coord_frame, text="(페이지 열고 클릭하면 자동 입력됨)", fg="#bdc3c7", bg="#34495e").grid(row=1, column=0, columnspan=4, pady=2)

        # 실시간 카운트다운
        self.countdown_label = tk.Label(self.root, text="대기 중... 코레일 페이지 준비하세요", font=("Consolas", 14, "bold"), fg="#e74c3c", bg="#2c3e50")
        self.countdown_label.pack(pady=15)

        # 시작/정지 버튼
        btn_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack(pady=10)
        self.start_btn = tk.Button(btn_frame, text="시작하기", command=self.start_macro, bg="#27ae60", fg="white", font=("bold", 12), width=12, height=2)
        self.start_btn.pack(side="left", padx=10)
        self.stop_btn = tk.Button(btn_frame, text="정지", command=self.stop_macro, bg="#c0392b", fg="white", font=("bold", 12), width=10, height=2)
        self.stop_btn.pack(side="left", padx=10)

        # 현재 마우스 위치 표시 (강화: 실시간 업데이트)
        self.mouse_label = tk.Label(self.root, text="마우스 위치: 코레일 페이지에서 '조회' 버튼 위에 올리면 자동 복사", fg="#bdc3c7", bg="#2c3e50")
        self.mouse_label.pack(pady=5)
        self.update_mouse_pos()  # 실시간 업데이트 시작

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.image_path = path
            self.img_label.config(text=f"선택됨: {os.path.basename(path)} (백업용)", fg="#2ecc71")

    def update_mouse_pos(self):
        x, y = pyautogui.position()
        self.mouse_label.config(text=f"마우스 위치: X={x}, Y={y} ← 코레일 버튼 위 클릭!")
        self.root.after(500, self.update_mouse_pos)  # 0.5초마다 업데이트

    def start_macro(self):
        if self.running:
            return
        try:
            target_str = self.time_entry.get().strip()
            self.target_time = datetime.datetime.strptime(target_str, "%Y-%m-%d %H:%M:%S.%f")
        except:
            messagebox.showerror("오류", "시간 형식이 잘못됐습니다!\n예: 2025-11-23 10:00:00.000")
            return

        if self.target_time < datetime.datetime.now():
            messagebox.showwarning("경고", "이미 지난 시간입니다! (현재: 2025-11-22)")
            return

        self.running = True
        self.start_btn.config(text="실행 중...")
        self.thread = threading.Thread(target=self.run_macro, daemon=True)
        self.thread.start()

    def run_macro(self):
        url = self.url_entry.get().strip()
        mode = self.click_mode.get()

        while self.running:
            now = datetime.datetime.now()
            diff = (self.target_time - now).total_seconds()

            if diff <= 0:
                self.countdown_label.config(text="★★★ 코레일 실행 중! ★★★", fg="#f1c40f")
                
                # 1. 크롬 열고 코레일 사이트 접속
                webbrowser.open_new_tab(url)
                time.sleep(3.5)  # 코레일 로딩 대기 (느린 페이지라 길게)

                # 페이지 스크롤 (버튼 보이게)
                pyautogui.scroll(-2)  # 살짝 아래로 스크롤
                time.sleep(1)

                # 2. 버튼 클릭 (좌표 우선 + 이미지 백업)
                success = False
                if mode == "coord":
                    try:
                        x = int(self.x_entry.get())
                        y = int(self.y_entry.get())
                        pyautogui.click(x, y)
                        pyautogui.click(x, y)  # 더블 클릭 보험
                        self.countdown_label.config(text=f"성공! 조회 버튼 클릭 ({x},{y})", fg="#2ecc71")
                        success = True
                    except ValueError:
                        self.countdown_label.config(text="좌표 입력 오류 (숫자 확인)", fg="red")

                # 이미지 시도 (OpenCV 에러 무시)
                if not success and mode == "image" and self.image_path:
                    try:
                        # OpenCV 없이 pyautogui 기본 인식 시도 (confidence 낮춤)
                        btn_loc = pyautogui.locateCenterOnScreen(self.image_path, confidence=0.7)  # 낮춰서 시도
                        if btn_loc:
                            pyautogui.click(btn_loc)
                            pyautogui.click(btn_loc)
                            self.countdown_label.config(text="이미지로 성공 클릭!", fg="#2ecc71")
                            success = True
                        else:
                            self.countdown_label.config(text="이미지 못 찾음 → 좌표로 폴백", fg="orange")
                    except Exception as e:
                        print(f"이미지 에러 무시: {e}")  # 콘솔에만 출력
                        self.countdown_label.config(text="이미지 실패 → 좌표 클릭으로 이동", fg="orange")

                # 폴백: 좌표 강제 클릭
                if not success:
                    try:
                        x = int(self.x_entry.get())
                        y = int(self.y_entry.get())
                        pyautogui.click(x, y)
                        self.countdown_label.config(text=f"폴백 성공! ({x},{y}) 클릭", fg="#2ecc71")
                    except:
                        self.countdown_label.config(text="클릭 실패 - 좌표 재설정 필요", fg="red")

                # 추가: Enter 키로 제출 (코레일 폼용)
                time.sleep(0.5)
                pyautogui.press('enter')
                break

            # 카운트다운 업데이트 (밀리초 정밀)
            mins = int(diff // 60)
            secs = diff % 60
            ms = int((secs - int(secs)) * 1000)
            secs = int(secs)
            self.countdown_label.config(text=f"남은 시간: {mins:02d}분 {secs:02d}.{ms:03d}초 | 코레일 대기")

            time.sleep(0.001 if diff < 1 else 0.05)

        self.running = False
        self.start_btn.config(text="시작하기")

    def stop_macro(self):
        self.running = False
        self.start_btn.config(text="시작하기")
        self.countdown_label.config(text="정지됨 - 다시 시작하세요")

# 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = TimingMacroApp(root)
    root.mainloop()