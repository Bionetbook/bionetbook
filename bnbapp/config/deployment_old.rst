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
    heroku config:add AWS_ACCESS_KEY_ID=XXX
    heroku config:add AWS_SECRET_ACCESS_KEY=XXX
    heroku pg:promote DATABASE_COLOR
    git push heroku master
    