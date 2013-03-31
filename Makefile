# Some helpful utility commands.

all: deploy

deploy:
	# heroku pgbackups:capture --expire
	git push git@heroku.com:bnbapp.git master
	heroku run python bnbapp/bionetbook/manage.py syncdb --noinput  --settings=bionetbook.settings.heroku --app bnbapp
	heroku run python bnbapp/bionetbook/manage.py migrate --settings=bionetbook.settings.heroku --app bnbapp

style:
	git push heroku master
	heroku run python bionetbook/manage.py collectstatic --noinput --settings=bionetbook.settings.heroku

restoredata:
	heroku pgbackups:capture --expire
	curl -o latest.dump `heroku pgbackups:url`
	dropdb bionetbook
	createdb bionetbook
	pg_restore --verbose --clean --no-acl --no-owner -d bionetbook latest.dump
