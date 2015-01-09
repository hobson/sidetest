import json
from collections import Counter
import pandas as pd

def query_walgreens():
    """Return at most 5 product records for stores in or near the indicated zipcode

    Arguments:
      product_id (str): hexadecimal identifier for a product type or model (NOT a physical item serial number)
      zip_code (str): 5 or 9-digit zip-code near which you want to find products
      page (int): 1-offset page number for pagenated output from Walgreens.com

    Returns:
      list of dict: A list of at most 5 dicts containing product location information for an individual item
        None if no products of the requested type near the specified location exist, or if
        the page number is beyond the complete list of all neaby products. 
    """
    return {"product_id": "e00d60d327046ad96439559e177a4ade361c8688", "store_id": "walgreens_11926", "zipcode": "76801_1", "ts": "2013-12-18 23:01:49", "availability": 0, "quantity": 0}


def mirror_walgreens():
   """Generate all retail products (and their store zip codes) for Walgreens

   A correct and complete strategy would be to query a zipcode not in those already found for each individual product until all zipcodes have been queried at least once for each product. This seem like an O(N*M*P) solution, where N = # zipcodes, M = # product types, P = # pages.
   But worst case optimal solution would be O(N*M) if no duplicate product-store pairs were returned for the same zipcode query.
   To reduce duplicate queries need to maintain list of all possible N*M  product-store combinations

   """


def index_products(path='gistfile1.json'):
    """Index (create hash table) of a table of records from a json file"""
    js = json.load(open(path, 'r'))
    labels = js[0].keys()
    keys = ('product_id', 'store_id')
    store_products = {}
    for rec in js:
        i = '|'.join(rec[k] for k in keys)
        # need to make sure all the columns are processed in the same order to reuse the canonical labels list
        store_products[i] = [rec[k] for k in labels]
    assert(len(js)==len(store_products))
    return store_products



def load_dataframe(path='gistfile1.json'):
    """Create a pandas dataframe from a list of objects in a json file"""
    js = json.load(open(path, 'r'))
    df = pd.DataFrame.from_records(js)
    print df.describe()
    assert(len(df)==len(js))
    return df
    keys = ('product_id', 'store_id')
    store_products = {}
    for rec in js:
        i = '|'.join(rec[k] for k in keys)
        store_products[i] = rec


def analyze(df=None):
    df = df or load_dataframe()
    print df.describe()
    for col in df.columns:
        c = Counter(df[col])
        print '========== {N} ==========\n{col} item: count...'.format(N=len(c), col=col)
        print dict((k,v) for i,(k,v) in enumerate(c.iteritems()) if i < 20)

