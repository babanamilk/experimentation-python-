# experimentation-python-

## Snake 🐍

터미널에서 즐기는 스네이크 게임입니다. 표준 라이브러리(`curses`)만 사용합니다.

```bash
python -m snake
```

- 이동: 방향키 또는 `W` `A` `S` `D`
- 게임 오버 후 재시작: `R`
- 종료: `Q` 또는 `Esc`

> Windows에서는 먼저 `pip install windows-curses`를 설치하세요.

### 테스트

```bash
python -m unittest discover tests
```
