from datetime import datetime


class InMemoryPostsRepo:
    def __init__(self):
        self.next_id = 1
        self.by_id = {}

    def get_all(self):
        return tuple(self.by_id.values())

    def request_create(self, post):
        post.id = self.next_id
        post.created = datetime.now()
        self.by_id[post.id] = post
        self.next_id += 1
        return post

    def get_by_id(self, id):
        return self.by_id.get(id, None)

    def request_delete(self, id, user):
        p = self.get_by_id(id)
        if not p:
            return f"post doesn't exists for id: {id}"
        if p.author.id != user.id:
            return f"you arent author for this post id: {id}"
        del self.by_id[id]
        return None

    def request_update(self, id, user, post):
        p = self.get_by_id(id)
        if not p:
            return f"post doesn't exists for id: {id}"
        if p.author.id != user.id:
            return f"you arent author for this post id: {id}"
        self.by_id[id] = post
        return None
