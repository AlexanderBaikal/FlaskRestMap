import json
from ast import literal_eval
from datetime import datetime

from posts import post
from tools.misc import get_connection_cursor


class SqlitePostsRepo:
    def __init__(self, name):
        self.name = name

    def get_all(self):
        query = """SELECT *
                    FROM posts JOIN users ON posts.user_id = users.id"""
        con, cur = get_connection_cursor(self.name)
        results = cur.execute(query).fetchall()
        res = list()

        for elem in results:
            author = {'username': elem[7], 'id': elem[6]}
            res.append(post.Post(id=elem[0], title=elem[1], text=elem[2],
                                 created=elem[3], coords=literal_eval(elem[4]), user_id=elem[5],
                                 author=author))
        con.close()
        return res

    def get_by_id(self, id):
        query = """SELECT *
                    FROM posts JOIN users ON posts.user_id=users.id
                    WHERE posts.id = ?"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (id,)).fetchone()
        if result is None:
            con.close()
            return None
        con.close()
        author = {'username': result[7], 'id': result[6]}
        return post.Post(id=result[0], title=result[1], text=result[2],
                         created=result[3], coords=result[4], user_id=result[5],
                         author=author)

    def request_create(self, local_post):
        query = """INSERT INTO posts(title, text, created, coords, user_id)
                            VALUES (?, ?, ?, ?, (SELECT id FROM users WHERE username = ?))"""
        con, cur = get_connection_cursor(self.name)
        tuple_args = (local_post.title, local_post.text, datetime.now(),
                      local_post.coords,
                      local_post.author['username'])
        result = cur.execute(query, tuple_args)
        if not result.rowcount > 0:
            con.close()
            return None
        coords = literal_eval(local_post.coords)
        dict_args = {'id': result.lastrowid, 'title': local_post.title, 'text': local_post.text,
                     'created': datetime.now(), 'coords': coords, 'author': local_post.author}
        new_post = post.Post(**dict_args)
        con.commit()
        con.close()
        return new_post

    def request_delete(self, id, user):
        query = """DELETE FROM posts
                WHERE id=? AND user_id=?"""
        con, cur = get_connection_cursor(self.name)
        cur.execute(query, (id, user.id))
        # return message?
        con.commit()
        con.close()

    def request_update(self, id, user, post):
        query = """UPDATE posts
                SET title=?, text=?, coords=?
                WHERE id=? AND user_id=?"""
        con, cur = get_connection_cursor(self.name)
        cur.execute(query, (post.title, post.text, post.coords, id, user.id))
        con.commit()
        con.close()

    def get_by_username(self, username):
        query = """SELECT * FROM posts JOIN users ON posts.user_id=users.id
                WHERE user_id=(SELECT id from users WHERE username=?)"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (username,)).fetchall()
        if result is None:
            con.close()
            return None
        con.close()
        res = list()
        for elem in result:
            author = {'username': elem[7], 'id': elem[6]}
            res.append(post.Post(id=elem[0], title=elem[1], text=elem[2],
                                 created=elem[3], coords=elem[4], user_id=elem[5],
                                 author=author))
        return res

    def get_by_category(self, category):
        query = """SELECT * FROM posts
                WHERE category=?"""
        con, cur = get_connection_cursor(self.name)
        result = cur.execute(query, (category,))
        if result is None:
            con.close()
            return None
        con.close()
        return post.Post(id=result[0], title=result[1], text=result[2],
                         created=result[3], coords=result[4], user_id=result[5])
