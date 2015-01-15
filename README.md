# <a name="Sidetest"/>Sidetest<a>

I'm having fun with a traveling salesman, minimum spanning tree problem, though I'm not sure MST is the right way to pose the problem.  

# <a name='Problem'/>Problem<a>

Say you have an API that you can query with a zip code, and you get a list of the closest N stores, and you want to "visit" all the stores with as few queries as possible. 

# <a name="PossibleAlgorithms"/>Possible Algorithms

If you use Kruskal's Algorithm with stores as veriticies and zipcodes as edges, it won't be optimal, because one zip would get you 5 vertices, but Kruskal only gives you credit for 1 as it explores the graph. You could give each zip/edge/arc a weight of N or N^2 (length of 1/N or 1/N^2, where N is the number of stores in that zip query, up to some pagination limit (say 5).  This improves things a bit, and is what I've done. But since this is pretty uniform length/weight, since most queries will be limitted only by the pagination limit, it help all that much. What if you added 0-length edges between all stores returned for a given zip!? Now we're talking! But wait, you don't get ALL the possible nodes for a given zipcode query. You only get 5.  So maybe 1/N is the right cost metric (weight/length) after all. 

Here's a graph diagram of all 7,921 stores and their 34,254 edges (zip codes they share). Check out the [`attempt.py`](https://github.com/hobson/sidetest/blob/master/attempt.py) file in this repo if you want to see how this graph was created or explore it yourself:

    >>> len(G.nodes()), len(G.edges())
    (7921, 34254)

![Force-Directed Graph Diagram](spring50edges.png?raw=true "50 Store-Zipcode Edges, Force-Directed Layout")

or this

![Shell Graph Diagram](shell50edges.png?raw=true "50 Store-Zipcode Edges, Shell (Circle) Layout")

# <a name="FirstSolutionAttempt"/>First Solution Attempt

I'm using 1/min(N,5) s the length for each edge between stores sharing a zipcode query response. MST algorithms usually assume a fully connected graph -- you can see from the plots that this one isn't. So I'm doing MST (Kruskal) on each of the graph cliques. The second option is what I've chosen. Should have a solution up shortly.

Here's the first MST attempt:

    In [1]: from attempt import minimum_spanning_zipcodes
    In [2]: zipcodes = minimum_spanning_zipcodes()
    In [3]: len(zipcodes)
    Out[3]: 7659
    In [4]: len(list(set(zipcodes)))
    Out[4]: 3381

But I haven't tested it to see if it's optimal or even a complete list. With 3381 queries required for 7921 stores and 5 stores returned per zip (most of the time), this definitely seems suboptimal.

# <a name="Solution">Solution</a>

I'm not sure this problem can be easily transformed to fit an MST solver. Instead, why not just use logic to whittle it down. Start with 2 `dict`s:

    1. zip code -> stores
    1-a. store `list` -- a sequence preserves the order of pages in the query resonse
    1-b. store `set`  -- more efficiently find if it has a particular store id
    2. store   -> zip codes
    2-a. zip code `list` -- preserves the order they were originally queried
    2-b. zip code `set` -- more efficiently find if a store can be retrieved using a particular zip code

Then sort the `store_zipcodes` dict by the len of their zipcode sequences (increasing order), so that you start with stores that can only be found with one zip code query. Union all these 1-length sets of zipcodes and make sure neither the stores nor the zip codes appear anywhere else in your dictionaries (they shouldn't if the queries are invertable).

This first step only eliminates 476 stores, 5% of the 7921 stores. So this isn't saving much, even if it is an O(N) problem).

    In [1]: from attempt import zipcodes_to_query()
    In [2]: len(zipcodes_to_query())
    Out[2]: 476

Next, for the remaining stores (this should actually work from the very beginning:

    for each store:
       sort zipcodes in reverse order of the number of stores associated with them len(zipcode_stores[store])
       pick the first zipcode in the longest list that has the store in the first 5 elements of the sequence
       if still not found just pick the first zipcode (with the longest list of stores)
       eliminate this zipcode and the batch of 5 stores associated with it from the list under consideration (replacing store id's with Nones so that the sequences order and batches of 5 are preserved but set membership is not) adding all these zipcode->store pairs to your "found" list (which will be used later to execute the queries)

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
