rm -f cingerine/db.sqlite
rm -rf cingerine/migrations
cd cingerine || exit
flask db init
flask db migrate
flask db upgrade
