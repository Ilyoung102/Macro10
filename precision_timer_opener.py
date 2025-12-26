# precision_timer_opener.py
import pyautogui
import time
import datetime
import webbrowser
import os

# ───────────────────────────────────────────────
# 여기만 수정하세요!!!
# ───────────────────────────────────────────────
TARGET_TIME = "2025-11-23 11:00:00.500"   # 원하는 정확한 시간 (밀리초까지 가능)
URL = "https://www.coupang.com/vp/products/123456789"   # 들어갈 사이트 주소
# ───────────────────────────────────────────────

# 크롬 빠르게 열기 위한 경로 (기본 경로면 그냥 두세요)
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def open_site_now():
    print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ★★★ 지금이 딱 그 시간! 사이트 열어요! ★★★")
    
    # 방법1: webbrowser + 크롬 직접 실행 (가장 빠름)
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(CHROME_PATH))
    webbrowser.get('chrome').open_new_tab(URL)
    
    # 방법2: 만약 위가 안 되면 pyautogui로 주소창 강제 입력 (백업용)
    # time.sleep(1.5)
    # pyautogui.hotkey('ctrl', 't')
    # time.sleep(0.3)
    # pyautogui.write(URL)
    # pyautogui.press('enter')

print("═"*60)
print("   정밀 타이밍 사이트 오프너 (pyautogui + webbrowser)")
print("   목표 시간:", TARGET_TIME)
print("   목표 URL :", URL)
print("═"*60)

# 목표 시간 파싱
target = datetime.datetime.strptime(TARGET_TIME, "%Y-%m-%d %H:%M:%S.%f")

print(f"현재 시간: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
print("대기 중... (Ctrl+C로 강제 종료 가능)\n")

while True:
    now = datetime.datetime.now()
    diff = (target - now).total_seconds()
    
    if diff <= 0:
        open_site_now()
        break
    
    # 1초 미만 남으면 0.001초마다 체크 (정밀도 극대화)
    if diff < 1:
        time.sleep(0.001)
    else:
        time.sleep(0.1)
    
    # 실시간 카운트다운 (보기 좋게)
    if diff < 10:
        print(f"\r남은 시간: {diff:.3f}초   ", end="")
    elif diff < 60:
        print(f"\r남은 시간: {diff:.2f}초   ", end="")
    else:
        minutes = int(diff // 60)
        seconds = diff % 60
        print(f"\r남은 시간: {minutes}분 {seconds:.1f}초   ", end="")