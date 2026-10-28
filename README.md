# 캐릭터 이동 애니메이션

Python과 pico2d, transitions를 사용한다.

## 실행

```powershell
python -m pip install -r requirements.txt
python main.py
```

좌우 방향키로 이동하고 키를 놓으면 대기한다. 대기 5초 후 수면에 들어간다.
수면에서는 Space로 일어나거나 좌우 방향키로 이동한다. Escape 또는 창 닫기로 종료한다.

대기 중 **A 키**를 누르면 5초 동안 자동으로 달린다. A를 놓아도 이동하며,
속도는 일반 달리기의 2배, 크기는 1.5배다. 화면 양 끝에서 자동으로 방향을 바꾼다.
좌우 방향키를 누르면 그 방향의 일반 달리기로 즉시 전환한다.
5초가 지나면 기본 크기의 대기로 돌아간다. 다시 자동으로 달리려면 A를 놓았다가 누른다.

한국어 [상태 다이어그램과 전환 규칙](state_machine.md)을 참고한다.

## 검증

```powershell
python -m unittest discover -s tests -v
```

테스트에서는 이미지 로딩과 시간을 대체하여 창을 열지 않고 상태와 이동을 검증한다.
17개 테스트로 기존 상태, 자동 이동·경계·확대 그리기 인자, 정확한 5초 만료,
키 반복과 재진입, 입력 우선순위, Escape·창 닫기를 확인한다.

실제 이미지 리소스로 화면 없이 SDL 소프트웨어 렌더링을 확인하려면 다음을 실행한다.

```powershell
python tools/verify_render.py
```

이 검사는 실제 `Boy`·`Grass`를 150프레임 그린다. 사용자 화면에서의 직접 조작 검사는
`python main.py`를 실행하여 A 키, 좌우 경계, 방향키 취소, 5초 종료를 확인한다.
