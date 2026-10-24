
import time

import aiosqlite

from config import COOLDOWN_SECONDS, DB_PATH, xp_for_level


async def init_db() -> None:
    """봇 시작 시 테이블이 없으면 만든다."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                guild_id    INTEGER NOT NULL,
                user_id     INTEGER NOT NULL,
                xp          INTEGER NOT NULL DEFAULT 0,   -- 현재 레벨 안에서 쌓인 XP
                level       INTEGER NOT NULL DEFAULT 0,
                last_xp_at  REAL    NOT NULL DEFAULT 0,   -- 마지막으로 XP 받은 시각
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )
        await db.commit()


async def get_user(guild_id: int, user_id: int) -> tuple[int, int]:
    """(xp, level) 반환. 기록이 없으면 (0, 0)."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT xp, level FROM users WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        row = await cur.fetchone()
    return (row[0], row[1]) if row else (0, 0)


async def add_xp(guild_id: int, user_id: int, amount: int) -> int | None:
    now = time.time()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT xp, level, last_xp_at FROM users WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        row = await cur.fetchone()
        xp, level, last = row if row else (0, 0, 0.0)

        if now - last < COOLDOWN_SECONDS:
            return None

        xp += amount
        leveled_up = False
        while xp >= xp_for_level(level):
            xp -= xp_for_level(level)
            level += 1
            leveled_up = True

        await db.execute(
            """
            INSERT INTO users (guild_id, user_id, xp, level, last_xp_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (guild_id, user_id)
            DO UPDATE SET xp = excluded.xp,
                          level = excluded.level,
                          last_xp_at = excluded.last_xp_at
            """,
            (guild_id, user_id, xp, level, now),
        )
        await db.commit()

    return level if leveled_up else None
