import aiosqlite

async def init_db():
    async with aiosqlite.connect("bot_database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                first_name TEXT NOT NULL
                )
        """)
        await db.commit()
        print("База данных успешно инициализирована")

async def add_user(user_id, username, first_name):
    async with aiosqlite.connect("bot_database.db") as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        await db.commit()