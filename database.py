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