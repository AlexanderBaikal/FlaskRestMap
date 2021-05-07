from api.posts import PostListRes, PostRes
from api.users import RegisterRes, LoginRes
from app.app import main_app


@main_app.route("/")
def root():
    return main_app.send_static_file('index.html')


main_app.api.add_resource(RegisterRes, '/api/register')
main_app.api.add_resource(LoginRes, '/api/login')
main_app.api.add_resource(PostListRes, '/api/posts/')
main_app.api.add_resource(PostRes, '/api/post/<int:post_id>')

if __name__ == '__main__':
    main_app.run()