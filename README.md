# 레벨링 봇

채팅하면 XP가 쌓이고 레벨업하는 디스코드 봇입니다. (뼈대 + XP 적립 + 레벨업)

## 파일설명
- `bot.py`: 봇 시작, Cog 불러오기
- `config.py`: XP 범위, 쿨타임, 레벨 공식
- `database.py`: DB 읽기/쓰기
- `cogs/leveling.py`: XP 적립, 레벨업 알림

## 새 기능 추가하는법
1. `cogs/` 에 새 파일 만들기 (예: `cogs/ranking.py`)
2. 파일 끝에 `async def setup(bot)` 작성
3. `bot.py` 의 `EXTENSIONS` 목록에 `"cogs.ranking"` 추가

## 자주 막히는점
- XP가 안쌓여요 → Message Content Intent 를 포털에서 켰는지 확인
- 슬래시 명령어가 안보여요 → 디스코드 재시작 또는 몇분 대기
- 쿨타임이 60초라 테스트가 느려요 → `config.py` 의 `COOLDOWN_SECONDS` 를 잠깐 5로
