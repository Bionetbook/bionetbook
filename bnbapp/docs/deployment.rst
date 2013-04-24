====================
Deployment on Heroku
====================

.. parsed-literal::

    git push git@heroku.com:bnbapp.git master
    




Useful commands
    heroku run python bnbapp/bionetbook/manage.py syncdb --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py collectstatic --noinput --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py help --app bnbapp
    heroku run python bnbapp/bionetbook/manage.py createsuperuser --settings=bionetbook.settings.heroku --app bnbapp
    heroku logs --app bnbapp
    heroku pgbackups:capture --expire