# Android APK Build Instructions

이 앱은 **Flet** 프레임워크로 작성되었습니다. 안드로이드 APK로 변환하려면 다음 방법 중 하나를 사용하세요.

## 1. 윈도우에서 직접 빌드하기 (WSL 필요)
윈도우에서 직접 빌드하려면 **WSL (리눅스 서브시스템)** 이 설치되어 있어야 합니다.
(설정이 복잡할 수 있습니다)

1.  WSL 터미널 열기
2.  필수 패키지 설치:
    ```bash
    sudo apt update
    sudo apt install -y git python3-pip python3-venv libgtk-3-dev libmpv1
    ```
3.  Flet 설치 및 빌드:
    ```bash
    pip install flet
    flet build apk
    ```

## 2. (추천) GitHub Actions 이용하기
코드를 GitHub에 올리면 자동으로 빌드되게 설정할 수 있습니다.


# Macro10
