'''
author: id, username
coords:
created:
title:
text:
'''
import ast

from flask import jsonify

from tools.my_dict import MyDict
from users.user import User


class Post(MyDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.author:
            self.author = User(**self.author)