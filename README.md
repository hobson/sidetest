# sidetest

This is example code for a job application

# Installation

If you use pip, virtualenv, and virtualenvwrapper (you really should):

    mkvirtualenv sidetest
    workon sidetest
    git clone https://github.com/hobson/sidetest.git
    cd sidetest
    pip install -r requirements.txt
    python attempt.py

# I want to learn python "best practices"

Virtualenvs help you maintain repeatable development environments. Virtualenvwrapper makes it even easier. Follow the instructions for installing virtualenvwrapper [here](http://virtualenvwrapper.readthedocs.org/en/latest/install.html). Or if you want a bit more customized instructions for Mac OSX, this might help: http://jamie.curle.io/blog/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x/

# I don't want to use a virtualenv

    git clone https://github.com/hobson/sidetest.git
    cd sidetest
    sudo pip install -r requirements.txt
    python attempt.py

# I don't want to use pip

Follow the official instructions for installing pandas [here](http://pandas.pydata.org/pandas-docs/stable/install.html)

You can then clone the repo and run the attempts.py script:

    git clone https://github.com/hobson/sidetest.git
    cd sidetest
    python attempt.py
