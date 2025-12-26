import flet as ft
import datetime
import asyncio

# Logic to handle platform-specific features
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

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

    # Click Settings (Enhanced)
    clicks_input = ft.TextField(
        label="클릭 횟수",
        value="7",
        width=100,
        text_style=ft.TextStyle(font_family="Consolas"),
        bgcolor="#21262d", 
        border_color="#30363d"
    )
    
    interval_input = ft.TextField(
        label="간격(초)",
        value="0.025",
        width=100,
        text_style=ft.TextStyle(font_family="Consolas"),
        bgcolor="#21262d", 
        border_color="#30363d"
    )

    # Coordinate Manual Input
    res_text = ft.Text("현재 창/화면 크기: 불러오는 중...", size=14, color="orange")
    x_input = ft.TextField(label="X 좌표", value="500", width=100, bgcolor="#21262d", border_color="#30363d")
    y_input = ft.TextField(label="Y 좌표", value="1000", width=100, bgcolor="#21262d", border_color="#30363d")

    def page_resize(e):
        # On Windows with pyautogui, show the Monitor Resolution
        if HAS_PYAUTOGUI:
            w, h = pyautogui.size()
            res_text.value = f"모니터 해상도: {w} x {h} (현재 창: {int(page.width)}x{int(page.height)})"
        else:
            # On Mobile, page.width/height IS the screen size (logical)
            res_text.value = f"현재 화면(창) 크기: {int(page.width)} x {int(page.height)}"
        page.update()

    page.on_resized = page_resize 

    # Windows-only Capture Logic
    async def capture_coord_win(e):
        if not HAS_PYAUTOGUI:
            return
        
        page.window_minimize = True
        page.update()
        
        # Wait a bit for minimize animation
        await asyncio.sleep(0.5)
        
        # Simple instruction - unlike original Tkinter overlay, Flet overlay is hard.
        # We'll just wait for a click or use immediate position after a delay?
        # Creating a full-screen transparent overlay in Flet is tricky.
        # Instead, we will use a "3 second delay" approach for simplicity, 
        # or just grab the CURRENT mouse position if the user aligns it first?
        # Let's try to mimic the "Click to set" behavior using a loop monitoring mouse state 
        # is hard without blocking.
        # EASIEST PROVEN WAY: Give 3 seconds to move mouse, then capture.
        
        # BUT user wanted "Click" to capture. 
        # Since we can't easily overlay, let's use the '3 second timer' method which is robust.
        
        # NOTE: User asked for "Capture". Original used specific click. 
        # I will use a hybrid: visual countdown overlay then capture.
        pass # Replaced by logic in layout section to avoid async complexity here if possible, 
             # but actually we need the function here.

    # 3-Second Capture Implementation (Better than overlay for Flet)
    async def start_capture_win(e):
        page.window_minimize = True
        page.update()
        
        # We can't easily detect "Global Click" without a hook. 
        # PyAutoGUI doesn't listen for clicks, only controls. 
        # Pynput is needed for listeners, but that adds dependency.
        # The original script used a Tkinter overlay to detect click.
        # Since we are in Flet, let's stick to "Move mouse to target in 3 seconds".
        
        for i in range(3, 0, -1):
            # We can't show UI if minimized, so we maybe shouldn't minimize fully? 
            # Or just rely on user understanding. 
            pass 
        
        # Actually, let's use a Dialog to instruct.
        page.window_restore = True
        page.update()
        # This function will be defined properly with the button below.

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
                
                # Check required inputs
                num_clicks = int(clicks_input.value)
                click_interval = float(interval_input.value)
                target_x = int(x_input.value)
                target_y = int(y_input.value)

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

                # Enter Mini Mode
                main_content.visible = False
                mini_view.visible = True
                page.window_width = 150
                page.window_height = 80
                page.window_always_on_top = True 
                page.update()

                while running:
                    now = datetime.datetime.now()
                    diff = (target_dt - now).total_seconds()

                    if diff <= 0:
                        # Action Trigger
                        
                        # Open URL first
                        if open_site_checkbox.value and url_input.value:
                            page.launch_url(url_input.value)
                            await asyncio.sleep(1.0) 

                        # Simulate Clicks
                        status_text.value = f"클릭 {num_clicks}회 실행 중..."
                        mini_status.value = "Clicking..."
                        timer_display.color = "#00ff00"
                        mini_timer.color = "#00ff00"
                        page.update()

                        for i in range(num_clicks):
                            if not running: break
                            timer_display.value = f"CLICK! {i+1}/{num_clicks}"
                            mini_timer.value = f"{i+1}/{num_clicks}"
                            # Visual Click Feedback
                            page.bgcolor = "#30363d"
                            page.update()
                            await asyncio.sleep(0.05)
                            page.bgcolor = "#0d1117"
                            page.update()
                            await asyncio.sleep(click_interval)

                        status_text.value = "완료!"
                        timer_display.value = "DONE"
                        mini_timer.value = "DONE"
                        
                        # Reset & Restore
                        await asyncio.sleep(2) # Show DONE for 2 seconds
                        running = False
                        restore_view(None) # Call restore logic
                        break

                    # Update Display
                    mins, secs = divmod(int(diff), 60)
                    ms = int((diff % 1) * 1000)
                    time_str = f"{mins:02d}:{secs:02d}.{ms:03d}"
                    
                    timer_display.value = time_str
                    mini_timer.value = time_str
                    
                    await asyncio.sleep(0.01)
                    page.update()

            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("입력 값이 잘못되었습니다!"))
                page.snack_bar.open = True
                page.update()
        else:
            # Stop manually
            restore_view(None)

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

    # Windows Capture Overlay Logic
    async def complete_capture_win(e):
        if not HAS_PYAUTOGUI:
            return

        # Capture Position
        # using pyautogui for global consistency, though e.global_x/y works too relative to window
        cx, cy = pyautogui.position()
        
        # Restore Window
        page.window_full_screen = False
        page.window_opacity = 1.0
        page.window_bgcolor = "#0d1117" # Restore bg color
        page.window_always_on_top = False
        
        # Hide Overlay
        capture_overlay.visible = False
        main_content.visible = True
        
        # Update Values
        x_input.value = str(cx)
        y_input.value = str(cy)
        
        # Feedback
        page.snack_bar = ft.SnackBar(ft.Text(f"좌표 확인: X={cx}, Y={cy}"))
        page.snack_bar.open = True
        page.update()

    capture_overlay = ft.Container(
        content=ft.Column([
            ft.Text("마우스로 원하는 위치를 클릭하세요!", size=30, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("(클릭 시 좌표가 저장되고 창이 복귀됩니다)", size=20, color="yellow"),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        on_click=complete_capture_win,
        bgcolor="#33000000", # 20% opacity black
        visible=False,
    )

    async def run_windows_capture(e):
        # Setup Overlay Mode
        main_content.visible = False
        capture_overlay.visible = True
        
        # Make Window Transparent & Full Screen
        page.window_full_screen = True
        page.window_opacity = 0.4 # Semi-transparent to see target
        page.window_always_on_top = True
        # page.window_bgcolor = ft.colors.TRANSPARENT # Flet desktop limitation: explicit transparent might be tricky depending on OS compositing
        # We rely on opacity for now.
        
        page.update()

    win_capture_btn = ft.ElevatedButton(
        text="좌표 잡기 (클릭)", 
        on_click=run_windows_capture,
        style=ft.ButtonStyle(bgcolor="#4d535e", color="white")
    )

    # Mini Mode (Execution View)
    mini_timer = ft.Text("00:00.000", size=18, weight=ft.FontWeight.BOLD, color="#00ffaa")
    mini_status = ft.Text("실행 중...", size=10, color="white")
    
    def restore_view(e):
        nonlocal running
        # Always stop and reset
        running = False
        start_btn.text = "시작하기"
        start_btn.bgcolor = "#238636"
        time_input.read_only = False
        status_text.value = "대기 중..."
        
        # Restore UI
        main_content.visible = True
        mini_view.visible = False
        
        # Restore Window
        # Force a small change if needed, but usually just setting props works.
        page.window_width = 480 
        page.window_height = 800
        page.window_always_on_top = False
        page.update()

    mini_restore_btn = ft.ElevatedButton("중지/복귀", on_click=restore_view, style=ft.ButtonStyle(bgcolor="#b33a3a", color="white", padding=5), height=30)
    
    mini_view = ft.Container(
        content=ft.Column([
            ft.Text("매크로 실행 중", color="orange", weight=ft.FontWeight.BOLD),
            mini_timer,
            mini_status,
            mini_restore_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        visible=False, # Hidden by default
        bgcolor="#1e1e1e",
        padding=10
    )

    # Layout Construction
    controls_list = [
        ft.Text("좌표:", size=16),
        x_input, 
        y_input
    ]
    if HAS_PYAUTOGUI:
        controls_list.append(win_capture_btn)

    # Main Content Wrapper
    main_content = ft.Column(
        [
            ft.Container(content=title_text, alignment=ft.alignment.center, padding=20),
            ft.Container(
                content=ft.Column([
                    ft.Text("설정", size=20, weight=ft.FontWeight.BOLD, color="orange"),
                    time_input,
                    url_input,
                    open_site_checkbox,
                    ft.Divider(color="grey"),
                    
                    # Coordinates
                    ft.Text("좌표 및 클릭 설정", size=16, weight=ft.FontWeight.BOLD, color="orange"),
                    res_text,
                    ft.Row(controls_list, alignment=ft.MainAxisAlignment.START, wrap=True),
                    
                    ft.Container(height=10),
                    ft.Row([clicks_input, interval_input], alignment=ft.MainAxisAlignment.START),
                    
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

    # Layout
    page.add(
        main_content,
        mini_view,
        capture_overlay
    )
    
    page_resize(None)

    # Update Start Logic to trigger Mini Mode
    # We need to modify toggle_timer, but it is defined ABOVE. 
    # To avoid massive file rewrite errors, I will define a wrappers loop handling logic inside start_btn?
    # No, I should redefine toggle_timer logic.
    # But toggle_timer is complex.
    # Let's injecting the "Mini Mode Switch" inside the existing toggle_timer running loop.
    
    # Wait, I can't easily edit toggle_timer from here. 
    # I need to rewrite the entire toggle_timer function AND the main layout part.
    # This replacement is replacing lines 286-343 (The Layout Part).
    # I still need to update the `toggle_timer` function which is lines 142-240.
    
    # Let's do this in two steps.
    # Step 1: Replace layout (This tool call).
    # Step 2: Update toggle_timer to manipulate `main_content` and `mini_view`.

if __name__ == "__main__":
    ft.app(target=main)
