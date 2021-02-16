from cingerine.database import db
from cingerine.database.models import Post, Category, Player


def create_blog_post(data):
    title = data.get('title')
    body = data.get('body')
    category_id = data.get('category_id')
    category = Category.query.filter(Category.id == category_id).one()  # noqa
    post = Post(title, body, category)
    db.session.add(post)
    db.session.commit()


def create_player(data):
    player_id = data.get('playerId')
    name = data.get('name')
    player = Player(player_id, name)
    db.session.add(player)
    db.session.commit()


def update_post(post_id, data):
    post = Post.query.filter(Post.id == post_id).one()  # noqa
    post.title = data.get('name')
    post.body = data.get('body')
    category_id = data.get('category_id')
    post.category = Category.query.filter(Category.id == category_id).one()  # noqa
    db.session.add(post)
    db.session.commit()


def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).one()  # noqa
    db.session.delete(post)
    db.session.commit()


def create_category(data):
    name = data.get('name')
    category_id = data.get('id')

    category = Category(name)
    if category_id:
        category.id = category_id

    db.session.add(category)
    db.session.commit()


def update_category(category_id, data):
    category = Category.query.filter(Category.id == category_id).one()  # noqa
    category.name = data.get('name')
    db.session.add(category)
    db.session.commit()


def delete_category(category_id):
    category = Category.query.filter(Category.id == category_id).one()  # noqa
    db.session.delete(category)
    db.session.commit()
