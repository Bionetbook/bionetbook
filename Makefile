# Some helpful utility commands.

all: deploy

deploy:
	heroku pgbackups:capture --expire
	git push heroku master
	heroku run python lac/manage.py syncdb --noinput  --settings=lac.settings.heroku
	heroku run python lac/manage.py migrate --settings=lac.settings.heroku

style:
	git push heroku master
	heroku run python lac/manage.py collectstatic --noinput --settings=lac.settings.heroku

restoredata:
	heroku pgbackups:capture --expire
	curl -o latest.dump `heroku pgbackups:url`
	dropdb lac
	createdb lac
	pg_restore --verbose --clean --no-acl --no-owner -d lac latest.dump
