from datetime import time

from flask_restplus import fields
from flask_restplus.fields import Raw, MarshallingError

from cingerine.api.restplus import api


class Time(Raw):
    """
    Return a formatted time string in %H:%M.
    """

    __schema_type__ = "string"
    __schema_format__ = "time"

    def __init__(self, time_format="%H:%M%:%S", **kwargs):
        super(Time, self).__init__(**kwargs)
        self.time_format = time_format

    def format(self, value):
        try:
            value = self.parse(value)
            if self.time_format == "iso":
                return value.isoformat()
            elif self.time_format:
                return value.strftime(self.time_format)
            else:
                raise MarshallingError("Unsupported time format %s" % self.time_format)
        except (AttributeError, ValueError) as e:
            raise MarshallingError(e)

    @staticmethod
    def parse(value):
        if isinstance(value, time):
            return value
        if isinstance(value, str):
            return time.fromisoformat(value)
        else:
            raise ValueError("Unsupported Time format")


blog_post = api.model('Blog post', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
    'title': fields.String(required=True, description='Article title'),
    'body': fields.String(required=True, description='Article content'),
    'pub_date': fields.DateTime,
    'category_id': fields.Integer(attribute='category.id'),
    'category': fields.String(attribute='category.name')
})

report_item = api.model('Report item', {
    'a': fields.String(required=True, description='Asset ID'),
    'p': fields.String(required=True, description='Player ID'),
    'd': fields.String(required=True, description='Date'),
    'h': fields.Integer(required=True, description='Hour'),
    'c': fields.Integer(required=True, description='Count')
})

openingHours = api.model('Opening Hours', {
    'weekday': fields.Integer(required=True, description='Weekday enumerated from 0 (Monday) to 6 (Sunday)'),
    'fromTime': Time(description='begin of the period like HH:MM:SS'),
    'toTime': Time(description='end of the period like HH:MM:SS')
})

specialHours = api.model('Special Hours', {
    'date': fields.Date(required=True, dt_format='YYYY-MM-DD', description='The date with exceptional opening hours'),
    'fromTime': Time(description='begin of the period like HH:MM:SS'),
    'toTime': Time(description='end of the period like HH:MM:SS')
})

player = api.model('Player', {
    'playerId': fields.String(readOnly=True, description='The unique identifier of the player'),
    'groupId': fields.String(required=False, description='Optional grouping identifier'),
    'name': fields.String(required=True, description='A readable identifyer'),
    'location': fields.String(required=False, description='Optional location tag'),
    'latitude': fields.Fixed(requiured=False, decimals=6, description="Latitude ISO-6709"),
    'longitude': fields.Fixed(required=False, decimals=6, description='Longitude ISO-6709'),
    'orientation': fields.String(required=True, description="Screen orientation, 'vertical' or 'horizontal'"),
    'width': fields.Integer(required=True, description='The width of the visible screen in pixels'),
    'height': fields.Integer(required=True, description='The height of the visible screen in pixels'),
    'openingHours': fields.List(fields.Nested(openingHours), required=False),
    'specialHours': fields.List(fields.Nested(specialHours), required=False)
})

playerState = api.model('PlayerState', {
    'playerId': fields.String(readOnly=True, description='The unique identifier of the player'),
    'playerState': fields.String(required=False, description="Any of 'running', 'stopped', 'unknown'"),
    'lastActive': fields.DateTime
})

targetGroup = api.model('Target Group', {
    'gender': fields.String(),
    'startAge': fields.Integer,
    'endAge': fields.Integer
})

playoutPlan = api.model('Playout Plan', {
    'playoutId': fields.String(readOnly=True, description='The unique identifier of the playout'),
    'fromDate': fields.Date(required=True, dt_format='YYYY-MM-DD',
                            description='The date with exceptional opening hours'),
    'toDate': fields.Date(required=True, dt_format='YYYY-MM-DD', description='The date with exceptional opening hours'),
    'fromTime': Time(description='begin of the period like HH:MM:SS'),
    'toTime': Time(description='end of the period like HH:MM:SS'),
    'assetId': fields.String(required=True, description='The unique identifier of the playoutr'),
    'count': fields.Integer(required=True, description='The width of the visible screen in pixels'),
    'priority': fields.Integer(required=True, description='The height of the visible screen in pixels'),
    'assetLag': fields.Integer(required=True, description='The height of the visible screen in pixels'),
    'playerIds': fields.List(fields.String, required=True),
    'targetGroup': fields.Nested(targetGroup, required=False)
})


pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results')
})


page_of_blog_posts = api.inherit('Page of blog posts', pagination, {
    'items': fields.List(fields.Nested(blog_post))
})


page_of_players = api.inherit('Page of Players', pagination, {
    'items': fields.List(fields.Nested(player))
})

page_of_playouts = api.inherit('Page of Playout Plans', pagination, {
    'items': fields.List(fields.Nested(playoutPlan))
})

list_of_counts = api.model('Playout Count', {
    'report': fields.List(fields.Nested(report_item))
})

category = api.model('Blog category', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    'name': fields.String(required=True, description='Category name'),
})

category_with_posts = api.inherit('Blog category with posts', category, {
    'posts': fields.List(fields.Nested(blog_post))
})
