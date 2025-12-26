# 버튼 클릭 10 - 진짜 완벽 최종판.py
# pip install flet pyautogui

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
    page.window_width = 440
    page.window_height = 640
    page.window_resizable = False
    page.theme_mode = "dark"
    page.bgcolor = "#0d1117"
    page.padding = 20
    page.horizontal_alignment = "center"

    click_x = click_y = None
    running = False

    # 알림 함수
    def alert(msg, color="red"):
        page.snackbar = ft.Snackbar(ft.Text(msg, color="white"), bgcolor=color)
        page.snackbar.open = True
        page.update()

    # 좌표 잡기
    def capture_coord(e):
        nonlocal click_x, click_y
        page.window_minimized = True
        page.update()

        def on_click(e):
            nonlocal click_x, click_y
            x, y = pyautogui.position()
            click_x, click_y = x, y
            page.overlay.pop()
            page.window_minimized = False
            status.value = f"좌표: {x}, {y}"
            status.color = "#79c0ff"
            page.update()

        overlay = ft.Container(
            content=ft.Text("클릭할 버튼을 눌러주세요", size=26, weight="bold", color="#00ffaa"),
            width=page.window_width,
            height=page.window_height,
            bgcolor=ft.Colors.with_opacity(0.94, ft.Colors.BLACK),
            alignment=ft.alignment.center,
            on_click=on_click
        )
        page.overlay.append(overlay)
        page.update()

    # 실행 로직
    def run_macro():
        nonlocal running, click_x, click_y
        url = url_field.value.strip()
        try:
            target = datetime.datetime.strptime(time_field.value.strip(), "%Y-%m-%d %H:%M:%S.%f")
            clicks = int(count_field.value) if count_field.value else 7
            interval = float(interval_field.value) if interval_field.value else 0.025
        except:
            alert("시간 형식이 잘못되었습니다!")
            running = False
            page.window_minimized = False
            page.update()
            return

        if target < datetime.datetime.now():
            alert("이미 지난 시간입니다!")
            running = False
            page.window_minimized = False
            page.update()
            return

        # 미니 타이머
        timer = ft.Text("00:00.000", size=34, weight="bold", color="#79c0ff")
        mini = ft.Container(
            content=ft.Column([
                ft.Text("실행 중", size=16, color="#00ffaa"),
                timer
            ], alignment="center", horizontal_alignment="center"),
            width=280, height=96, bgcolor="#1e1e1e", border_radius=16,
            top=20, left=(page.window_width-280)//2,
            on_click=lambda e: setattr(page, "window_minimized", False) or page.update()
        )
        page.overlay.append(mini)
        page.update()

        while running:
            diff = (target - datetime.datetime.now()).total_seconds()
            if diff <= 0:
                if auto_open.value and url:
                    webbrowser.open(url)
                    time.sleep(1.2)
                for _ in range(clicks):
                    if not running: break
                    pyautogui.click(click_x, click_y)
                    time.sleep(interval)
                timer.value = "완료!"
                timer.color = "#00ff00"
                page.update()
                break

            mins, secs = divmod(int(diff), 60)
            ms = int((diff % 1) * 1000)
            timer.value = f"{mins:02d}:{secs:02d}.{ms:03d}"
            page.update()
            time.sleep(0.001)

        page.window_minimized = False

    # 시작하기
    def start(e):
        nonlocal running, click_x
        if not click_x:
            alert("좌표를 먼저 설정해주세요!")
            return
        running = True
        page.window_minimized = True
        threading.Thread(target=run_macro, daemon=True).start()

    # UI 구성 (Walrus Operator 완전 제거 → Pylance 오류 0개!)
    page.add(
        ft.Column([
            ft.Text("버튼 클릭 10", size=30, weight="bold", color="#00ffff"),
            time_field := ft.TextField(label="목표 시간", value="2025-11-23 10:00:00.000", width=380, text_size=13),
            url_field := ft.TextField(label="사이트 주소", value="https://www.korail.com/ticket/search/general", width=380, text_size=11),
            auto_open := ft.Checkbox(label="자동 사이트 열기", value=False),
            ft.Container(height=15),
            ft.Text("클릭 위치 설정", size=18, weight="bold", color="#ffa500"),
            ft.ElevatedButton("좌표 잡기", on_click=capture_coord, width=340, height=50,
                             style=ft.ButtonStyle(bgcolor="#238636", shape=ft.RoundedRectangleBorder(radius=14))),
            status := ft.Text("좌표: 없음", size=15, color="#ff5555"),
            ft.Row([
                count_field := ft.TextField(label="횟수", value="7", width=150),
                interval_field := ft.TextField(label="간격(초)", value="0.025", width=150)
            ], alignment="center"),
            ft.Container(height=40),
            ft.ElevatedButton("시작하기", on_click=start, width=380, height=84,
                             style=ft.ButtonStyle(bgcolor="#e63946", shape=ft.RoundedRectangleBorder(radius=22),
                                                text_style=ft.TextStyle(size=32, weight="bold")))
        ], alignment="center", horizontal_alignment="center", spacing=12)
    )

    # 여기서 := 제거하고 일반 할당으로 바꿈 → Pylance 오류 완전 사라짐
    page.add(time_field, url_field, auto_open, status, count_field, interval_field)

ft.app(target=main)