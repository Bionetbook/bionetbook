# Some helpful utility commands.

all: deploy

deploy:
	heroku pgbackups:capture --expire
	git push heroku master
	heroku run python bionetbook/manage.py syncdb --noinput  --settings=bionetbook.settings.heroku
	heroku run python bionetbook/manage.py migrate --settings=bionetbook.settings.heroku

style:
	git push heroku master
	heroku run python bionetbook/manage.py collectstatic --noinput --settings=bionetbook.settings.heroku

restoredata:
	heroku pgbackups:capture --expire
	curl -o latest.dump `heroku pgbackups:url`
	dropdb lac
	createdb lac
	pg_restore --verbose --clean --no-acl --no-owner -d bionetbook latest.dump
