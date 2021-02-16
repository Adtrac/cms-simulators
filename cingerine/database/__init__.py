from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from cingerine.database.models import Post, Category, Player
    db.drop_all()
    db.create_all()
