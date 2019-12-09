StackOfMusic
=============================================

![Alt text](static/img/StackOfMusic.png)

Introduce
================================================
It is a loopstation-based music composition and streaming service that utilizes MIR modules.

StackOfMusic Server installation
====================================
We also support Windows OS, but we recommend Ubuntu OS.

Set up python
----------------------------------
********************************

    To set up python: http://www.python.org
    $ sudo apt-get install python3


How to install
--------------------------------
**************************

    $ git clone https://github.com/StackOfMusic/StackOfMusic.git
    $ cd StackOfMusic
    ## Please create a virtual environment and install Python package. ##
    $ virtualenv -p python3 myvenv
    $ . myvenv/bin/activate
    $ pip install -r requirements.txt

How to run in local
--------------------------------
***************************

    $ cd StackOfMusic/StackOfMusic
    $ python manage.py runserver
    
    ## Please turn on the other terminal. ##
    $ celery -A StackOfMusic worker -l info
    