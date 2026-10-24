DB_PATH = "levels.db"

# 메시지 1개당 지급되는 XP 범위 (랜덤)
XP_MIN = 15
XP_MAX = 25

# 같은 유저가 XP를 다시 받을 수 있기까지의 시간(초). 도배 방지용
COOLDOWN_SECONDS = 60


def xp_for_level(level: int) -> int:
    """level 에서 level+1 로 올라가는 데 필요한 XP"""
    return 5 * level**2 + 50 * level + 100
