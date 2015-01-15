# <a name='Sidetest'/>Sidetest<a>

I'm having fun, here with a traveling salesman, minimum spanning tree problem, though I'm not sure MST is the right way to pose the problem.  

# <a name='Problem'/>Problem<a>

Say you have an API that you can query with a zip code, and you get a list of the closest N stores, and you want to "visit" all the stores with as few queries as possible. 

# <a name='PossibleAlgorithms'/>Possible Algorithms</a>

If you use Kruskal's Algorithm with stores as veriticies and zipcodes as edges, it won't be optimal, because one zip would get you 5 vertices, but Kruskal only gives you credit for 1 as it explores the graph. You could give each zip/edge/arc a weight of N or N^2 (length of 1/N or 1/N^2, where N is the number of stores in that zip query, up to some pagination limit (say 5).  This improves things a bit, and is what I've done. But since this is pretty uniform length/weight, since most queries will be limitted only by the pagination limit, it help all that much. What if you added 0-length edges between all stores returned for a given zip!? Now we're talking! But wait, you don't get ALL the possible nodes for a given zipcode query. You only get 5.  So maybe 1/N is the right cost metric (weight/length) after all. 

Here's a graph diagram of all 7,921 stores and their 34,254 edges (zip codes they share). Check out the [`attempt.py`](https://github.com/hobson/sidetest/blob/master/attempt.py) file in this repo if you want to see how this graph was created or explore it yourself:

    >>> len(G.nodes()), len(G.edges())
    (7921, 34254)

![Force-Directed Graph Diagram](spring50edges.png?raw=true "50 Store-Zipcode Edges, Force-Directed Layout")

or this

![Shell Graph Diagram](shell50edges.png?raw=true "50 Store-Zipcode Edges, Shell (Circle) Layout")

Here are the first 7 store -> zipcode edges:

![Force-Directed Graph, 7 Stores](first7stores.png?raw=true "First 7 Stores, Force-Directed Layout")

# <a name='MyAttempt'/>My Attempt</a>

I'm using 1/min(N,5) s the length for each edge between stores sharing a zipcode query response. MST algorithms usually assume a fully connected graph -- you can see from the plots that this one isn't. So I'm doing MST (Kruskal) on each of the graph cliques. The second option is what I've chosen. Should have a solution up shortly.

# <a name='Installation'/>Installation</a>

If you use pip, virtualenv, and virtualenvwrapper (you really should):

    mkvirtualenv sidetest
    workon sidetest
    git clone https://github.com/hobson/sidetest.git
    cd sidetest

Be patient with the installation of requirements, especially if you have never installed pandas, numpy, six and the other dependencies before:

    pip install -r requirements.txt

# <a name='Usage'/>Usage</a>

With all the dependencies installed you should be ready to run it as a script to see example output.  

    python attempt.py


# <a name='UsePythonBestPractices'/>Use python "best practices"</a>

Virtualenvs help you maintain repeatable development environments. Virtualenvwrapper makes it even easier. Follow the instructions for installing virtualenvwrapper [here](http://virtualenvwrapper.readthedocs.org/en/latest/install.html). Or if you want a bit more customized instructions for Mac OSX, this might help: http://jamie.curle.io/blog/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x/

# I don't want to use `virtualenv`

    git clone https://github.com/hobson/sidetest.git
    cd sidetest
    sudo pip install -r requirements.txt
    python attempt.py

# I don't want to use `pip`

`Sidetest` depends on 3 python packages:

    1. `pandas` (efficient querying or large datasets in RAM)
    2. `networkx` (efficient graph algorithms and data structures)
    3. `future` (python 2/3 compatability for `http.server` module to serve pretty d3.js plots)

Follow the official instructions for installing pandas [here](http://pandas.pydata.org/pandas-docs/stable/install.html)

You can find `networkx` [here](https://networkx.github.io/download.html).

The other dependencies listed in `sidetest/requirements.txt` should have been installed already when you isntalled `pandas` and `networkx`.

You can then clone the repo and run the attempts.py script:

    git clone https://github.com/hobson/sidetest.git
    cd sidetest
    python attempt.py
