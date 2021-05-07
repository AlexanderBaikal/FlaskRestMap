from tools.misc import get_connection_cursor
from users import user


class SqliteUsersRepo:
    def __init__(self, name):
        self.name = name

    def get_all(self):
        query = """Select id, username, password
                    FROM users"""
        con, cur = get_connection_cursor(self.name)
        results = cur.execute(query).fetchall()
        res = list()
        for elem in results:
            res.append(user.User(id=elem[0], username=elem[1], password=elem[2]))
        con.close()
        return res

    def get_by_id(self, id):
        query = """Select id, username, password
                    FROM users
                    WHERE id = ?"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (id,)).fetchone()
        if result is None:
            con.close()
            return None
        con.close()
        return user.User(id=result[0], username=result[1], password=result[2])

    def get_by_name(self, name):
        query = """SELECT id, username, password
                    FROM users
                    WHERE username = ?"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (name,)).fetchone()
        if result is None:
            con.close()
            return None
        con.close()
        return user.User(id=result[0], username=result[1], password=result[2])

    def request_create(self, name, password):
        found = self.get_by_name(name)
        if not (found is None):
            return None
        query = """INSERT INTO users(username, password)
                            VALUES (?, ?)"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (name, password))
        if not result.rowcount > 0:
            con.close()
            return None
        new_user = user.User(id=result.lastrowid, username=name, password=password)
        con.commit()
        con.close()
        return new_user

    def request_update(self, id, name, password):
        query = """UPDATE users
                SET username=?, password=?
                WHERE id=?"""
        con, cur = get_connection_cursor(self.name)
        cur.execute(query, (name, password, id))
        con.commit()
        con.close()

    def request_delete(self, id):
        query = """DELETE FROM users
                WHERE id=?"""
        con, cur = get_connection_cursor(self.name)
        cur.execute(query, (id, ))
        con.commit()
        con.close()

    def authorize(self, login, password):
        user = self.get_by_name(login)
        if user is None:
            return None, 'no user'
        if user.password != password:
            return None, 'Bad password'
        return user, ''