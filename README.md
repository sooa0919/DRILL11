# 캐릭터 이동 애니메이션

Python과 pico2d, transitions를 사용한다.

## 실행

```powershell
python -m pip install -r requirements.txt
python main.py
```

좌우 방향키로 이동하고 키를 놓으면 대기한다. 대기 5초 후 수면에 들어간다.
수면에서는 Space로 일어나거나 좌우 방향키로 이동한다. Escape 또는 창 닫기로 종료한다.

## 검증

```powershell
python -m unittest discover -s tests -v
```

테스트에서는 이미지 로딩과 시간을 대체하여 창을 열지 않고 상태와 이동을 검증한다.
