import aiosqlite

class Database:
    def __init__(self, path):
        self.path = path

    async def init(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    language TEXT DEFAULT 'ru',
                    money INTEGER DEFAULT 0,
                    gems INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0
                )
            """)
            await db.commit()

    async def create_user(self, user_id, username):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )
            await db.commit()

    async def set_language(self, user_id, lang):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
            await db.commit()

    async def get_language(self, user_id):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                return row[0] if row else "ru"

    async def get_user(self, user_id):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
                return await cur.fetchone()

    async def add_gems(self, user_id, amount):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE users SET gems = gems + ? WHERE user_id = ?", (amount, user_id))
            await db.commit()

    async def add_money(self, user_id, amount):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (amount, user_id))
            await db.commit()
