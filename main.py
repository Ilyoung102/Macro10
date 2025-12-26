import flet as ft
import datetime
import asyncio

# Android/Mobile compatible version of "Button Click 10"
# NOTE: Global screen clicking (pyautogui) is NOT possible on standard Android apps due to security sandbox.
# This version focuses on the Timer and URL Opening features.

def main(page: ft.Page):
    page.title = "매크로 순향 (Android)"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#0d1117"

    # State variables
    running = False
    
    # UI Components
    title_text = ft.Text("매크로 순향", size=38, weight=ft.FontWeight.BOLD, color="#00ffff")
    
    # Target Time Input
    default_time = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S.%f")
    time_input = ft.TextField(
        label="목표 시간",
        value=default_time,
        text_style=ft.TextStyle(size=18, font_family="Consolas"),
        color="#79c0ff",
        bgcolor="#21262d",
        border_color="#30363d"
    )

    # URL Input
    url_input = ft.TextField(
        label="사이트 주소",
        value="https://cgv.co.kr/cnm/movieBook",
        text_style=ft.TextStyle(size=14, font_family="Consolas"),
        color="#a5d6ff",
        bgcolor="#21262d",
        border_color="#30363d"
    )

    open_site_checkbox = ft.Checkbox(label="시간 되면 자동으로 사이트 열기", value=True)

    # Status Display using a Container for styling
    timer_display = ft.Text("00:00.000", size=40, weight=ft.FontWeight.BOLD, font_family="Consolas", color="#79c0ff")
    status_text = ft.Text("대기 중...", size=20, color="grey")

    # Start/Stop Button Logic
    async def toggle_timer(e):
        nonlocal running
        if not running:
            # Start
            try:
                target_str = time_input.value.strip()
                target_dt = datetime.datetime.strptime(target_str, "%Y-%m-%d %H:%M:%S.%f")
                
                if target_dt < datetime.datetime.now():
                    page.snack_bar = ft.SnackBar(ft.Text("이미 지난 시간입니다! 미래의 시간을 입력하세요."))
                    page.snack_bar.open = True
                    page.update()
                    return

                running = True
                start_btn.text = "중지"
                start_btn.bgcolor = "#b33a3a" # Red
                time_input.read_only = True
                page.update()

                while running:
                    now = datetime.datetime.now()
                    diff = (target_dt - now).total_seconds()

                    if diff <= 0:
                        # Action Trigger
                        timer_display.value = "ACTION!"
                        timer_display.color = "#00ff00"
                        status_text.value = "완료! (자동 클릭은 안드로이드 보안상 불가)"
                        
                        if open_site_checkbox.value and url_input.value:
                            page.launch_url(url_input.value)
                        
                        # Reset
                        running = False
                        start_btn.text = "시작하기"
                        start_btn.bgcolor = "#238636"
                        time_input.read_only = False
                        page.update()
                        break

                    # Update Display
                    mins, secs = divmod(int(diff), 60)
                    ms = int((diff % 1) * 1000)
                    timer_display.value = f"{mins:02d}:{secs:02d}.{ms:03d}"
                    timer_display.color = "#79c0ff"
                    
                    await asyncio.sleep(0.01)
                    page.update()

            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("시간 형식이 잘못되었습니다! (YYYY-MM-DD HH:MM:SS.sss)"))
                page.snack_bar.open = True
                page.update()
        else:
            # Stop manually
            running = False
            start_btn.text = "시작하기"
            start_btn.bgcolor = "#238636"
            time_input.read_only = False
            status_text.value = "중지됨"
            timer_display.value = "00:00.000"
            page.update()

    start_btn = ft.ElevatedButton(
        text="시작하기",
        on_click=toggle_timer,
        style=ft.ButtonStyle(
            color="white",
            bgcolor="#238636", # Green
            padding=20,
        ),
        width=200, 
        height=60,
    )

    # Layout
    page.add(
        ft.Column(
            [
                ft.Container(content=title_text, alignment=ft.alignment.center, padding=20),
                ft.Container(
                    content=ft.Column([
                        ft.Text("설정", size=20, weight=ft.FontWeight.BOLD, color="orange"),
                        time_input,
                        url_input,
                        open_site_checkbox,
                        ft.Divider(color="grey"),
                        ft.Container(
                            content=ft.Column([
                                timer_display,
                                status_text
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center,
                            padding=20,
                            bgcolor="#161b22",
                            border_radius=10
                        ),
                    ]),
                    padding=20,
                    bgcolor="#161b22",
                    border_radius=15
                ),
                ft.Container(height=20),
                ft.Container(content=start_btn, alignment=ft.alignment.center)
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
