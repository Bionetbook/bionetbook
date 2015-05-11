====================
Deployment on Heroku
====================

.. parsed-literal::

    git push git@heroku.com:bnbapp.git master
    


http://kencochrane.net/blog/2011/11/developers-guide-for-running-django-apps-on-heroku/

Useful commands
    heroku run python bnbapp/bionetbook/manage.py syncdb --settings=bionetbook.settings.heroku --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py collectstatic --noinput --settings=bionetbook.settings.heroku --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py help --settings=bionetbook.settings.heroku --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py createsuperuser --settings=bionetbook.settings.heroku --app bnbapp
    heroku logs --app bnbapp
    heroku run env --app bnbapp
    heroku pgbackups:capture --expire