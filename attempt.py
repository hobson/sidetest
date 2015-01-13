#!/usr/bin/env python 
import json
from collections import Counter
import pandas as pd
import itertools


def load_dataframe(path='gistfile1.json'):
    """Create a pandas dataframe from a list of objects in a json file"""
    js = json.load(open(path, 'r'))
    df = pd.DataFrame.from_records(js)
    assert(len(df)==len(js))
    return df


def analyze(df=None):
    df = df or load_dataframe()
    # statistics for real-valued columns:
    print df.describe()
    # unique record counts for all data columns (including strs):
    for col in df.columns:
        c = Counter(df[col])
        print '========== {N} ==========\n{col} item: count...'.format(N=len(c), col=col)
        print dict((k,v) for i,(k,v) in enumerate(c.iteritems()) if i < 20)


def query_walgreens(product='e00d60d327046ad96439559e177a4ade361c8688', zipcode='76065', page=1):
    """Return at most 5 product records for stores in or near the indicated zipcode

    Arguments:
      product_id (str): hexadecimal identifier for a product type or model (NOT a physical item serial number)
      zip_code (str): 5 or 9-digit zip-code near which you want to find products
      page (int): 1-offset page number for pagenated output from Walgreens.com

    Returns:
      list of tuple: A `list` of at most 5 `tuple`s containing product location information for an individual item
        None if no products of the requested type near the specified location exist, or if
        the page number is beyond the complete list of all neaby products. 
    """
    db = query_walgreens.db
    df = db[(db['product_id'] == product) & (db['zipcode'] == zipcode+'_{0}'.format(page))].head(5)
    return list(df.to_records())
    # return {"product_id": "e00d60d327046ad96439559e177a4ade361c8688", "store_id": "walgreens_11926", "zipcode": "76801_1", "ts": "2013-12-18 23:01:49", "availability": 0, "quantity": 0}
# maintain a single copy of the database (a pandas dataframe) in RAM
query_walgreens.db = load_dataframe()

import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, labels=None, layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    """from https://www.udacity.com/wiki/creating-network-graphs-with-python"""

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    if labels:
        edge_labels = dict(zip(graph, labels))
        nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                     label_pos=edge_text_pos)

    # show graph
    plt.show()


# def main():
db = query_walgreens.db  # 38025 total records
# records_per_zipcode = Counter(db['zipcode'])  #  5725 zipcodes 
# records_per_store = Counter(db['store_id'])   #  8131 stores
zipcode_store_pairs = Counter((row[0].split('_')[0], row[1].split('_')[1]) for row in db[['zipcode', 'store_id']].values)  # 26615 unique store-zipcode pairs, so stores are showing up in multiple zipcode queries (as stated in the problem statement)


# a list of all the zipcodes for each store
store_zipcodes, zipcode_stores = {}, {}
for zipcode, store in zipcode_store_pairs:
    store_zipcodes[store] = store_zipcodes.get(store, []) + [zipcode]
    zipcode_stores[zipcode] = zipcode_stores.get(zipcode, []) + [store] 


draw_graph(sorted(store_zipcode_pairs.keys())[:20], labels=False, layout='spring')

# # now just need to find the optimal zipcodes to query so that all the stores will be
# if __name__ == '__main__':
#     main()