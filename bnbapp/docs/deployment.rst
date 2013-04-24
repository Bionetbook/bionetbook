====================
Deployment on Heroku
====================

.. parsed-literal::

    git push git@heroku.com:bnbapp.git master
    




Useful commands
    heroku run python bnbapp/bionetbook/manage.py syncdb --settings=bionetbook.settings.heroku --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py collectstatic --noinput --settings=bionetbook.settings.heroku --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py help --settings=bionetbook.settings.heroku --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py createsuperuser --settings=bionetbook.settings.heroku --app bnbapp
    heroku logs --app bnbapp
    heroku pgbackups:capture --expire