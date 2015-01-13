# sidetest

A real-world traveling salesman, spanning tree problem, sort-of. You Get  list of the closest 5 stores for each zip code query (edge?) and you want to "visit" all the stores with as few queries as possible. If you use Kruskal with stores as veriticies and zipcodes as edges, it won't be optimal, because one zip would get you 5 verices, but Kruskal only gives you credit for 1. You'd Have to weight each zip/edge by 1/N-sqrd where N is the number of stores in that zip query (usually 5). 


Here's a graph diagram of 50 edges, where edges connect stores to zipcodes.

![Force-Directed Graph Diagram](spring50edges.png?raw=true "50 Store-Zipcode Edges, Force-Directed Layout")

or this

![Shell Graph Diagram](shell50edges.png?raw=true "50 Store-Zipcode Edges, Shell (Circle) Layout")

Here are the first 7 store -> zipcode edges:

![Force-Directed Graph, 7 Stores](first7stores.png?raw=true "First 7 Stores, Force-Directed Layout")


# Installation

If you use pip, virtualenv, and virtualenvwrapper (you really should):

    mkvirtualenv sidetest
    workon sidetest
    git clone https://github.com/hobson/sidetest.git
    cd sidetest

Be patient with the installation of requirements, especially if you have never installed pandas, numpy, six and the other dependencies before:

    pip install -r requirements.txt

# Usage

With all the dependencies installed you should be ready to run it as a script to see example output.  

    python attempt.py

Check out the doctsring in attempts.py if you want to run it within an ipython console (REPL). This example just outputs the first 100 query responses:

    >>> import attempt
    >>> for i, rec in enumerate(attempt.generate_walgreens()):
    ...     print(rec)
    ...     if i > 100:
    ...         break
    (18716, 1, u'e00d60d327046ad96439559e177a4ade361c8688', 0, u'walgreens_4926', u'2013-12-18 23:52:03', u'19135_1')
    (18717, 0, u'e00d60d327046ad96439559e177a4ade361c8688', 0, u'walgreens_5522', u'2013-12-18 23:52:03', u'19135_1')
    ...

# I want to learn python "best practices"

Virtualenvs help you maintain repeatable development environments. Virtualenvwrapper makes it even easier. Follow the instructions for installing virtualenvwrapper [here](http://virtualenvwrapper.readthedocs.org/en/latest/install.html). Or if you want a bit more customized instructions for Mac OSX, this might help: http://jamie.curle.io/blog/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x/

# I don't want to use a virtualenv

    git clone https://github.com/hobson/sidetest.git
    cd sidetest
    sudo pip install -r requirements.txt
    python attempt.py

# I don't want to use pip

Follow the official instructions for installing pandas [here](http://pandas.pydata.org/pandas-docs/stable/install.html)

Find the isntructions for installing `networkx` on your system and install it as well.

The other dependencies listed in `requirements.txt` should have been installed with `pandas` and `networkx`.

You can then clone the repo and run the attempts.py script:

    git clone https://github.com/hobson/sidetest.git
    cd sidetest
    python attempt.py
