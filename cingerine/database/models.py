# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships


from datetime import datetime

from cingerine.api.dooh.serializers import Time
from cingerine.database import db
import datetime as dt


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class PlayoutPlan(db.Model):
    playoutId = db.Column(db.String(48), primary_key=True)
    fromDate = db.Column(db.Date)
    toDate = db.Column(db.Date)
    fromTime = db.Column(db.Time)
    toTime = db.Column(db.Time)
    assetId = db.Column(db.String(48))
    playerIds = db.Column(db.JSON())
    count = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    assetLag = db.Column(db.Integer)
    targeting = db.Column(db.JSON())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.toTime = Time.parse(kwargs['fromTime'])
        self.fromTime = Time.parse(kwargs['toTime'])
        self.fromDate = dt.datetime.strptime(kwargs['toDate'], '%Y-%m-%d')
        self.toDate = dt.datetime.strptime(kwargs['toDate'], '%Y-%m-%d')

    def __repr__(self):
        return f'<PlayoutPlan for asset {self.assetId} from {self.fromDate} to {self.toDate}'

    __str__ = __repr__


class Player(db.Model):
    playerId = db.Column(db.String(48), primary_key=True)
    name = db.Column(db.String(80))
    groupId = db.Column(db.String(80))
    location = db.Column(db.String(80))
    orientation = db.Column(db.String(80))
    latitude = db.Column(db.Numeric(precision=6))
    longitude = db.Column(db.Numeric(precision=6))
    openingHours = db.Column(db.JSON())
    specialHours = db.Column(db.JSON())
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<Player {self.name}, ID={self.playerId}>'

    __str__ = __repr__


class PlayerState(db.Model):
    playerId = db.Column(db.Integer, primary_key=True)
    playerState = db.Column(db.String(80))
    lastActive = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<Player {self.name}, ID={self.playerId}>'

    __str__ = __repr__


class ReportItem(db.Model):
    itemId = db.Column(db.Integer, primary_key=True)
    assetId = db.Column(db.String(48))
    playerId = db.Column(db.String(48))
    date = db.Column(db.Date)
    hour = db.Column(db.Integer)
    count = db.Column(db.Integer)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

    __str__ = __repr__
