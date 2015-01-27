#!/usr/bin/env python 
import json
import os
from collections import Counter
import pandas as pd
import itertools
from collections import OrderedDict

import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json

# requires future package
import http.server


def load_dataframe(path='responses.json'):
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


def split_into_connected_graphs(G):
    """CRUFT: Equivalent to list(nx.connected_component_subgraphs(G))"""
    CGs = []
    for cc in nx.connected_components(G):
        CG = nx.Graph()
        for node_label in cc:
            # this will add edges in both directions, so 2x inefficient
            for target_label in G[node_label].keys():
                CG.add_edge(node_label, target_label, **G.get_edge_data(node_label, target_label))
        CGs += [CG]
    return CGs


def api(product='e00d60d327046ad96439559e177a4ade361c8688', zipcode='76065', page=1):
    """Return at most 5 product records for stores in or near the indicated zipcode

    Arguments:
      product_id (str): hexadecimal identifier for a product type or model (NOT a physical item serial number)
      zip_code (str): 5 or 9-digit zip-code near which you want to find products
      page (int): 1-offset page number for pagenated output from a chain store website

    Returns:
      list of tuple: A `list` of at most 5 `tuple`s containing product location information for an individual item
        None if no products of the requested type near the specified location exist, or if
        the page number is beyond the complete list of all neaby products. 
    """
    db = api.db
    df = db[(db['product_id'] == product) & (db['zipcode'] == zipcode+'_{0}'.format(page))].head(5)
    return list(df.to_records())
    # return {"product_id": "e00d60d327046ad96439559e177a4ade361c8688", "store_id": "store_11926", "zipcode": "76801_1", "ts": "2013-12-18 23:01:49", "availability": 0, "quantity": 0}
# maintain a single copy of the database (a pandas dataframe) in RAM
api.db = load_dataframe()


def minimum_spanning_zipcodes():
    zipcode_query_sequence = []
    G = build_graph(api.db, limit=1000000)
    for CG in nx.connected_component_subgraphs(G):
        for edge in nx.minimum_spanning_edges(CG):
            zipcode_query_sequence += [edge[2]['zipcode']]
    return zipcode_query_sequence


def zipcodes_to_query():
    """Second attempt at a simpler non-grpahy solution


    for each store:
       sort zipcodes in reverse order of the number of stores associated with them len(zipcode_stores[store])
       pick the first zipcode in the longest list that has the store in the first 5 elements of the sequence
       if still not found just pick the first zipcode (with the longest list of stores)
       eliminate this zipcode and the batch of 5 stores associated with it from the list under consideration 
          (replacing store id's with Nones so that the sequences order and batches of 5 are preserved but set membership is not) adding all these zipcode->store pairs to your "found" list (which will be used later to execute the queries)

    """
    queries = []
    query_set = []
    stores_found = set()

    # hash-tables of all the zipcodes that could be queried to produce a store, and all stores that are returned in the response for each zipcode
    store_zipcodes, zipcode_stores = {}, {}
    for zipcode, store in api.db[['zipcode', 'store_id']].values:
        zipcode = int(zipcode.split('_')[0])
        store = int(store.split('_')[1])
        store_zipcodes[store] = store_zipcodes.get(store, []) + [zipcode]
        zipcode_stores[zipcode] = zipcode_stores.get(zipcode, []) + [store]
    zipcode_store_set = {}
    for zipcode in zipcode_stores:
        zipcode_store_set[zipcode] = set(zipcode_stores[zipcode])
    store_zipcode_set = {}
    for store in store_zipcodes:
        store_zipcode_set[store] = set(store_zipcodes[store])

    zipcode_stores = OrderedDict(sorted(zipcode_stores.items(), key=lambda pair: -len(pair[1])))
    store_zipcodes = OrderedDict(sorted(store_zipcodes.items(), key=lambda pair: +len(pair[1])))

    for store, zipcodes in store_zipcodes.iteritems():
        if len(zipcodes) > 1:
            break
        zc = zipcodes[0]
        queries += [zc]
        stores_found.add(store)
        del store_zipcode_set[store]
        # store_zipcodes unchanged

    for store, zipcode_set in store_zipcode_set.iteritems():
        # TODO
        pass

    return queries


def build_graph(df, limit=1000000, max_stores_per_query=5):
    """Construct a networkx graph from a DataFrame of API responses containing `zipcode` and `store_id` columns.""" 

    # hash-tables of all the zipcodes that could be queried to produce a store, and all stores that are returned in the response for each zipcode
    store_zipcodes, zipcode_stores = {}, {}
    for zipcode, store in df[['zipcode', 'store_id']].values:
        zipcode = zipcode.split('_')[0]
        store = 's' + store.split('_')[1]
        store_zipcodes[store] = store_zipcodes.get(store, []) + [zipcode]
        zipcode_stores[zipcode] = zipcode_stores.get(zipcode, []) + [store] 

    zipcode_stores = OrderedDict(sorted(zipcode_stores.items()))

    G = nx.Graph(name='Stores')

    # Lengths are proportional to the number of stores that are returned for the same zipcode query, maximum of 5 for the pagination limit
    for zc, stores in zipcode_stores.iteritems():
        L = 1.0 / min(len(stores), float(max_stores_per_query))
        # connect all zipcodes returned by a single query with a zero-length edge
        for edge in itertools.combinations(stores[:max_stores_per_query], 2):
            if edge[0] == edge[1]:
                continue
            length, zipcode = L, zc
            # the edge may already exist (stores may share another zip too), so must chose the shortest length of the two
            if G.has_edge(*edge):
                existing_edge = G.edge[edge[0]][edge[1]]
                # reuse the old zipcode even if the new one is the same length (to diversify the zipcode queries amd maximize the 5-store zipcode responses)
                if existing_edge['length'] < length:
                    length, zipcode = existing_edge['length'], existing_edge['zipcode']
            G.add_edge(edge[0], edge[1], weight=1.0/length, length=length, zipcode=zipcode)
        # only recheck the limit length after a zipcode batch has been processed
        if len(G.nodes()) >= limit:
            break
    return G


def write_d3_json(G):
    for node in G:
        G.node[node]['name'] = node
    # node-link (d3.js) format data stucture
    d = json_graph.node_link_data(G) 
    # serialize the node-link list
    json.dump(d, open('force/force.json','w'), indent=2)


def serve_d3_json(port=8000):
    print('Browse to file://{0} with your browser'.format(os.path.join(os.path.realpath('./force/'), 'force.html')))
    print('Hit Ctrl-C to stop the server')
    httpd = http.server.HTTPServer(('', port), http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()


def draw_graph(G, labels=None, layout='shell',
               node_size=400, node_color='blue', node_alpha=0.3,
               node_text_size=6,
               edge_color='blue', edge_alpha=0.3, edge_thickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    """from https://www.udacity.com/wiki/creating-network-graphs-with-python"""
    plt.figure(figsize=(12, 8))

    # spring, spectral, random, and shell layout algorithms:
    if layout.lower().strip()[:3] == 'spr':
        graph_pos=nx.spring_layout(G)
    elif layout.lower().strip()[:3] in ('spe', 'spc'):
        graph_pos=nx.spectral_layout(G)
    elif layout.lower().strip()[0] == 'r':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G, graph_pos, node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G, graph_pos, width=edge_thickness,
                           alpha=edge_alpha, edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos, font_size=node_text_size,
                            font_family=text_font)

    # if labels is None:
    #     labels = range(len(graph))

    # if labels:
    #     edge_labels = dict(zip(graph, labels))
    #     nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
    #                                  label_pos=edge_text_pos)

    # show graph
    plt.title('{0} Stores (Nodes) x {1} Edges'.format(len(G.nodes()), len(G.edges())))
    plt.show(block=False)

    return G


def main(limit=100):
    # # records_per_zipcode = Counter(df['zipcode'])  #  5725 zipcodes 
    # # records_per_store = Counter(df['store_id'])   #  8131 stores
    # zipcode_store = Counter((row[0].split('_')[0], 's'+row[1].split('_')[1]) for row in df[['zipcode', 'store_id']].values)  # 26615 unique store-zipcode pairs, so stores are showing up in multiple zipcode queries (as stated in the problem statement)
    # store_zipcode = Counter(('s'+row[1].split('_')[1], row[0].split('_')[0]) for row in df[['zipcode', 'store_id']].values)  

    # # list all the zipcodes for each store, and all stores for each zipcode
    # store_zipcodes, zipcode_stores = {}, {}
    # for zipcode, store in zipcode_store:
    #     store_zipcodes[store] = store_zipcodes.get(store, []) + [zipcode]
    #     zipcode_stores[zipcode] = zipcode_stores.get(zipcode, []) + [store] 

    G = draw_graph(build_graph(df=api.db, limit=limit), labels=False, layout='spring')
    
    # draw_graph(sorted(zipcode_store.keys())[:50], labels=False, layout='shell')
    # plt.title('Shell: 50 Zipcode->Store Edges')
    # draw_graph(sorted(store_zipcode.keys())[:20], labels=False, layout='spring')
    # plt.title('Force-Directed: 20 Store->Zipcode Edges')
    return G


if __name__ == '__main__':
    main()

