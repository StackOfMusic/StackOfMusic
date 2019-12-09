StackOfMusic
=============================================

![Alt text](static/img/StackOfMusic.png)

Introduce
================================================
It is a loopstation-based music composition and streaming service that utilizes MIR modules.

**We want everyone to be able to anyone can compose the music!**

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
    
Contribute
----------------
* Issue Tracker: https://github.com/StackOfMusic/StackOfMusic/issues
* Source Code: https://github.com/StackOfMusic/StackOfMusic/

Contribution guidelines
-----------------------
If you want to contribute to HML, be sure to review the [contribution guideline](https://github.com/StackOfMusic/StackOfMusic/). This project adheres to HML's code of conduct. By participating, you are expected to uphold this code.

We use GitHub issues for tracking requests and bugs.

License
------------------------
MIT license
