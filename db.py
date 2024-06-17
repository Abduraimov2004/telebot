import psycopg2 as psql


class Database:
    @staticmethod
    async def connect(query, query_type):
        """
        Berilgan SQL so'rovini bajaradi va natijani qaytaradi
        """
        db = psql.connect(
            database="n44",
            user="postgres",
            password="2004",
            host="localhost",
            port="5432"
        )
        cursor = db.cursor()
        data = ["insert", "delete"]
        cursor.execute(query)
        if query_type in data:
            db.commit()
            if query_type == "insert":
                return "inserted successfully"
        else:
            return cursor.fetchall()

    @staticmethod
    async def check_user_id(user_id: int):
        """
        Foydalanuvchi ID sini  mavjudligini tekshiradi
        """
        query = f"SELECT * FROM users WHERE user_id = {user_id}"
        check_user = await Database.connect(query, query_type="select")
        if len(check_user) == 1:
            return True
        return False
