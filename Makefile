# Some helpful utility commands.

all: deploy

deploy:
	heroku pgbackups:capture --expire --app bnbapp
	git push git@heroku.com:bnbapp.git release_alpha_1:master
	heroku run python bnbapp/bionetbook/manage.py syncdb --noinput  --settings=bionetbook.settings.heroku --app bnbapp
	heroku run python bnbapp/bionetbook/manage.py migrate --settings=bionetbook.settings.heroku --app bnbapp

style:
	git push git@heroku.com:bnbapp.git release_alpha_1:master
	heroku run python bnbapp/bionetbook/manage.py collectstatic --noinput --settings=bionetbook.settings.heroku --app bnbapp

restoredata:
	heroku pgbackups:capture --expire --app bnbapp
	curl -o latest.dump `heroku pgbackups:url`
	dropdb bionetbook
	createdb bionetbook
	pg_restore --verbose --clean --no-acl --no-owner -d bionetbook latest.dump


# OTHER USEFUL COMMANDS (NOTES)
#	heroku domains:add www.bionetbook.com --app bnbapp		# https://devcenter.heroku.com/articles/custom-domains
#	heroku logs --app bnbapp								# view the logs
#	heroku run python bnbapp/bionetbook/manage.py collectstatic --noinput --settings=bionetbook.settings.heroku --app bnbapp
#	heroku run python bnbapp/bionetbook/manage.py help --settings=bionetbook.settings.heroku --app bnbapp
