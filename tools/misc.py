import sqlite3

from flask import make_response, jsonify
from flask_jwt_simple import create_jwt

from users.user import User


def make_resp(message, status):
    resp = make_response(message, status)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp


def check_keys(dct, keys):
    return all(key in dct for key in keys)


def create_jwt_for_user(user):
    cp_user = User(**user)
    del cp_user['password']
    print(user)
    j_token = {'token': create_jwt(identity=cp_user)}
    return j_token


def get_connection_cursor(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    return con, cur