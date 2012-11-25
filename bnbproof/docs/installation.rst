============
Installation
============

Dependencies:

* Python 2.7.1
* VirtualEnv
* Pip
* PostGresql

Actions
---------

.. parsed-literal::

    pip install -r requirements.txt
    

Testing email
----------------

In a new shell, type:

    python -m smtpd -n -c DebuggingServer localhost:1025