from flask_restplus import fields
from cingerine.api.restplus import api


pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})


opening_hours = api.model('Opening Hour', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an OpeningHours record'),
    'weekdays': fields.Integer(readOnly=True, description='Integer representing the weekdays: bit 0 = Sunday'),
    'fromHour': fields.Integer(required=True, description='The hour when to start'),
    'toHour': fields.Integer(attribute='The hour when to stop'),
})


player = api.model('Player', {
    'playerId': fields.String(required=True, description='The unique identifier of the player'),
    'name': fields.String(required=True, description='A readable identifyer'),
 })

page_of_players = api.inherit('Page of Players', pagination, {
    'items': fields.List(fields.Nested(player))
})

player_with_opening_hours = api.inherit('Player with opening hours', player, {
    'openingHours': fields.List(fields.Nested(opening_hours))
})


################################

blog_post = api.model('Blog post', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
    'title': fields.String(required=True, description='Article title'),
    'body': fields.String(required=True, description='Article content'),
    'pub_date': fields.DateTime,
    'category_id': fields.Integer(attribute='category.id'),
    'category': fields.String(attribute='category.name'),
})


page_of_blog_posts = api.inherit('Page of blog posts', pagination, {
    'items': fields.List(fields.Nested(blog_post))
})

category = api.model('Blog category', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    'name': fields.String(required=True, description='Category name'),
})

category_with_posts = api.inherit('Blog category with posts', category, {
    'posts': fields.List(fields.Nested(blog_post))
})
