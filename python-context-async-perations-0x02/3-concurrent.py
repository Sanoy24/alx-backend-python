import aiosqlite
import asyncio


async def async_fetch_users():
    try:
        async with aiosqlite.connect("users.db") as db:
            async with db.execute("SELECT * FROM users") as cursor:
                users = await cursor.fetchall()
                print("[All Users]")
                for user in users:
                    print(user)
                return users
    except aiosqlite.Error as e:
        print(f"Database error in get_users: {e}")
        return []


async def async_fetch_older_users():
    try:
        async with aiosqlite.connect("users.db") as db:
            async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
                users = await cursor.fetchall()
                print("[Users over 40]")
                for user in users:
                    print(user)
                return users
    except aiosqlite.Error as e:
        print(f"Database error in get_users: {e}")
        return []


async def fetch_concurrently():
    try:
        await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    except Exception as e:
        print(f"Error in fetch_users_concurrently: {e}")
        return []


asyncio.run(fetch_concurrently())
