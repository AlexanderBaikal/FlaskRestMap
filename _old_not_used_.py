from datetime import timedelta

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin
from flask_jwt_simple import JWTManager, get_jwt_identity, jwt_required
from posts.post import Post
from posts.repo import InMemoryPostsRepo
from tools.misc import check_keys, make_resp  # , create_jwt_generate_response
from users.sqlite_repo import SqliteUsersRepo
from users.user import User

app = Flask(__name__)
app.user_repo = SqliteUsersRepo('./db/mapdb.db')
app.post_repo = InMemoryPostsRepo()

app.user_repo.request_create('alex', 'pass')
post_example = {
    "author": {
        "id": 3213,
        "username": "brwwewwfsu1"
    },
    "coords": {
        "lat": 52.2308,
        "lng": 104.3041
    },
    "created": "Wed, 05 May 2021 22:20:29 GMT",
    "id": 1232,
    "text": "my 1st marker",
    "title": "hello"
}
post = Post(**post_example)
app.post_repo.request_create(post)

post_example = {
    "author": {
        "id": 31232234,
        "username": "qweqewqwqesd"
    },
    "coords": {
        "lat": 52.2408,
        "lng": 104.3041
    },
    "created": "Wed, 05 May 2021 22:50:29 GMT",
    "id": 41232233,
    "text": "my 2nd marker",
    "title": "hellooo"
}
post = Post(**post_example)
app.post_repo.request_create(post)

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRES'] = timedelta(hours=24)
app.config['JWT_IDENTITY_CLAIM'] = 'user'
app.config['JWT_HEADER_NAME'] = 'authorization'
app.jwt = JWTManager(app)


# @app.route("/")
# def root():
#     return app.send_static_file('index.html')


# @app.route("/api/register", methods=['POST'])
# def register():
#     in_json = request.json
#     if not in_json:
#         return make_resp(jsonify({'message': 'empty request'}), 400)
#     elif not check_keys(in_json, ('username', 'password')):
#         return make_resp(jsonify({'message': 'bad request'}), 400)
#     created_user = app.user_repo.request_create(**in_json)
#     if created_user is None:
#         return make_resp(jsonify({'message': 'duplicated user'}), 400)
#     return create_jwt_generate_response(created_user)


# @app.route("/api/login", methods=['POST'])
# def login():
#     in_json = request.json
#     if not in_json:
#         return make_resp(jsonify({'message': 'empty request'}), 400)
#     elif not check_keys(in_json, ('username', 'password')):
#         return make_resp(jsonify({'message': 'bad request'}), 400)
#     user, error = app.user_repo.authorize(**in_json)
#     if user is None:
#         return make_resp(jsonify({'message': error}), 400)
#     # return create_jwt_generate_response(user)


# @app.route("/api/posts/", methods=['GET'])
# def get_all_posts():
#     return make_resp(jsonify(app.post_repo.get_all()), 200)


# @app.route("/api/post/<int:post_id>", methods=['DELETE'])
# @jwt_required
# def delete_post_by_id(post_id):
#     result = app.post_repo.request_delete(post_id, User(**get_jwt_identity()))
#     if result is not None:
#         return make_resp(jsonify({'message': result}), 400)
#     return make_resp(jsonify({'message': 'success'}), 200)


# @app.route("/api/post/<int:post_id>", methods=['GET'])
# def get_post_by_id(post_id):
#     return make_resp(jsonify(app.post_repo.get_by_id(post_id)), 200)


# @app.route("/api/post/<int:post_id>", methods=['PUT'])
# @jwt_required
# def put_post_by_id(post_id):
#     in_json = request.json
#     if not in_json:
#         return make_resp(jsonify({'message': 'empty request'}), 400)
#     elif not check_keys(in_json, ('title', 'text', 'coords', 'id')):
#         return make_resp(jsonify({'message': 'bad request'}), 400)
#     post = Post(**in_json)
#     post.author = User(**get_jwt_identity())
#     result = app.post_repo.request_update(post_id, post.author, post)
#     if result is not None:
#         return make_resp(jsonify({'message': result}), 400)
#     return make_resp(jsonify({'message': 'success'}), 200)


# @app.route("/api/posts", methods=['POST'])
# @jwt_required
# def add_post():
#     in_json = request.json
#     if not in_json:
#         return make_resp(jsonify({'message': 'empty request'}), 400)
#     elif not check_keys(in_json, ('title', 'text', 'coords')):
#         return make_resp(jsonify({'message': 'bad request'}), 400)
#     post = Post(**in_json)
#     post.author = User(**get_jwt_identity())
#     post = app.post_repo.request_create(post)
#     return make_resp(jsonify(post), 200)


if __name__ == '__main__':
    app.run(debug=True)
