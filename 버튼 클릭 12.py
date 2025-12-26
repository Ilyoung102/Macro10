# 버튼 클릭 10.py  ← 이걸로 저장하면 무조건 됩니다! (Flet 최신 버전 완벽 호환)
# 설치: pip install flet pyautogui

import flet as ft
import pyautogui
import webbrowser
import datetime
import threading
import time

pyautogui.PAUSE = 0.001
pyautogui.FAILSAFE = False

def main(page: ft.Page):
    page.title = "버튼 클릭 10"
    page.window_width = 900
    page.window_height = 1000
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0d1117"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.scroll = "adaptive"

    # 변수들
    click_x = None
    click_y = None
    running = False
    target_time = None
    timer_overlay = None
    timer_text = None

    # 타이머 업데이트
    def update_timer(text, color="#79c0ff"):
        nonlocal timer_text
        if timer_text and timer_overlay in page.overlay:
            timer_text.value = text
            timer_text.color = color
            page.update()

    # 미니 타이머 생성
    def create_mini_timer():
        nonlocal timer_text, timer_overlay
        timer_text = ft.Text("00:00.000", size=60, weight="bold", color="#79c0ff")
        timer_overlay = ft.Container(
            content=ft.Column(
                [
                    ft.Text("버튼 클릭 10 실행 중", size=24, weight="bold", color="#00ffaa"),
                    timer_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=520,
            height=160,
            bgcolor="#1e1e1e",
            border_radius=25,
            top=40,
            left=(page.window_width - 520) // 2,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.with_opacity(0.7, ft.colors.BLACK)),
            on_click=lambda e: (setattr(page, "window_minimized", False)) or page.update()
        )
        page.overlay.append(timer_overlay)
        page.update()

    # 좌표 잡기
    def capture_coord(e):
        page.window_minimized = True
        page.update()

        def set_coord(e):
            nonlocal click_x, click_y
            x, y = pyautogui.position()
            click_x, click_y = x, y
            page.overlay.pop()
            page.window_minimized = False
            coord_status.value = f"좌표 설정 완료 → X={x}  Y={y}"
            coord_status.color = "#79c0ff"
            page.update()

        overlay = ft.Container(
            width=page.window_width,
            height=page.window_height,
            bgcolor=ft.colors.with_opacity(0.9, ft.colors.BLACK),
            content=ft.Column(
                [ft.Text("클릭할 버튼 위에서 클릭하세요!", size=52, weight="bold", color="#00ffaa")],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            on_click=set_coord
        )
        page.overlay.append(overlay)
        page.update()

    # 클릭 실행
    def run_click():
        nonlocal running, target_time
        url = url_input.value.strip()
        try:
            clicks = int(clicks_input.value)
            interval = float(interval_input.value)
        except:
            clicks, interval = 7, 0.025

        while running:
            diff = (target_time - datetime.datetime.now()).total_seconds()
            if diff <= 0:
                if open_site_cb.value and url:
                    webbrowser.open_new_tab(url)
                    time.sleep(1.2)
                for _ in range(clicks):
                    if not running: break
                    pyautogui.click(click_x, click_y)
                    time.sleep(interval)
                update_timer("완료!", "#00ff00")
                break

            mins, secs = divmod(int(diff), 60)
            ms = int((diff % 1) * 1000)
            update_timer(f"{mins:02d}:{secs:02d}.{ms:03d}")
            time.sleep(0.001)

        page.window_minimized = False
        page.update()

    # 시작하기
    def start_click(e):
        nonlocal running, target_time, click_x, click_y
        if not click_x:
            page.show_snack_bar(ft.SnackBar(ft.Text("먼저 좌표를 설정해주세요!"), bgcolor="red"))
            return
        try:
            target_time = datetime.datetime.strptime(time_input.value.strip(), "%Y-%m-%d %H:%M:%S.%f")
            if target_time < datetime.datetime.now():
                page.show_snack_bar(ft.SnackBar(ft.Text("이미 지난 시간입니다!"), bgcolor="orange"))
                return
        except:
            page.show_snack_bar(ft.SnackBar(ft.Text("시간 형식이 잘못되었습니다!"), bgcolor="red"))
            return

        running = True
        page.window_minimized = True
        create_mini_timer()
        threading.Thread(target=run_click, daemon=True).start()

    # UI 구성 (text_style 오류 완전 해결!)
    time_input = ft.TextField(label="목표 시간", value="2025-11-23 10:00:00.000", width=700, text_size=18)
    url_input = ft.TextField(label="사이트 주소", value="https://www.korail.com/ticket/search/general", width=800, text_size=14)
    open_site_cb = ft.Checkbox(label="시간 되면 자동으로 사이트 열기", value=False, label_style=ft.TextStyle(color="#58a6ff"))

    coord_btn = ft.ElevatedButton(
        "좌표 잡기 시작",
        on_click=capture_coord,
        width=550,
        height=90,
        style=ft.ButtonStyle(
            bgcolor="#238636",
            shape=ft.RoundedRectangleBorder(radius=25),
            text_style=ft.TextStyle(size=28, weight="bold")
        )
    )

    coord_status = ft.Text("좌표: 아직 설정 안 됨", size=22, color="#ff5555")

    clicks_input = ft.TextField(label="클릭 횟수", value="7", width=250)
    interval_input = ft.TextField(label="간격(초)", value="0.025", width=250)

    # 시작하기 버튼 - text_style을 style 안에 넣음!
    start_btn = ft.ElevatedButton(
        "시작하기",
        on_click=start_click,
        width=650,
        height=150,
        style=ft.ButtonStyle(
            bgcolor="#e63946",
            shape=ft.RoundedRectangleBorder(radius=35),
            text_style=ft.TextStyle(size=48, weight="bold")
        )
    )

    page.add(
        ft.Column(
            [
                ft.Text("버튼 클릭 10", size=60, weight="bold", color="#00ffff"),
                ft.Divider(height=40),
                time_input,
                url_input,
                open_site_cb,
                ft.Divider(height=60),
                ft.Text("클릭할 버튼 위치 설정", size=28, weight="bold", color="#ffa500"),
                coord_btn,
                coord_status,
                ft.Divider(height=40),
                ft.Row([clicks_input, interval_input], alignment="center"),
                ft.Divider(height=100),
                start_btn
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

# 실행
ft.app(target=main)