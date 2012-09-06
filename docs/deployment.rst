====================
Deployment on Heroku
====================

.. parsed-literal::

    heroku create --stack cedar
    heroku addons:add memcache:5mb
    heroku addons:add sendgrid:starter
    heroku addons:add heroku-postgresql:dev
    heroku addons:add pgbackups
    heroku addons:add newrelic:standard
    heroku addons:add sentry:developer
    git push heroku master
    