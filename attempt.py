import json
from collections import Counter
import pandas as pd


def mirror_walgreens():
    """Generate all retail products (and their store zip codes) for Walgreens

    Each query to the website takes a product_id and zipcode and page number. 
    Each page of a query response should return 5 product-store pairs with a count of the quantity at that location 
    (though the actual Walgreens site returns 6 different products when I excercise it manually, without a product_id)

    A correct and complete strategy would be to query a zipcode not in those already found for each individual product until all zipcodes have been queried at least once for each product. This seem like an O(N*M*P) solution, where N = # zipcodes, M = # product types, P = # pages.
    But worst case optimal solution would be O(N*M) if no duplicate product-store pairs were returned for the same zipcode query.
    To reduce duplicate queries need to maintain list of all possible N*M  product-store combinations

    you'd preprocess your list of store_ids and zipcodes to count the number of stores in each zipcode, that number divided by 5 is the number of pages you'd have to request
    More optimally, for each product you'd like to
        1. iterate through zipcodes querying the db for that product at that location, page 1
        2. query that zipcode for another page only if more than 5 stores exist in that zip
        3. cross off a store-product pair from each of the <=5 records retrieved, using a master "TBD" list of store-prod pairs
        4. move on to the zipcode of the next store-product pair in your TBD list
        5. build up an adjacency graph of store locations for future optimization (path planning through the graph)
    typical database record:
    {"product_id": "e00d60d327046ad96439559e177a4ade361c8688", "store_id": "walgreens_5210", "zipcode": "76065_1", "ts": "2013-12-18 23:02:13", "availability": 0, "quantity": 0}
    """
    # presumably you'd already have a list of all the products you want to query, if not this would have to be obtained with another function optimized for that purpose
    # Only have 1 product in this test database
    products = ['e00d60d327046ad96439559e177a4ade361c8688']
    # strip the '_1' to mimic a real database
    # presumably you'd already have a list of all the zipcodes you want to query
    zipcodes = [s[:-2] for s in Counter(query_wallgreens.db['zipcode']).keys()]
    # likewise for walgreens store location ids
    stores = [s.split('_')[0] for s in Counter(query_wallgreens.db['store_id']).keys()]
    tbd = list(itertools.product(products, stores))
    records = []
    for product, zc in itertools.product(products, zipcodes):
        for zc in zipcodes:
            zip_records = []
            while True:
                zip_records += list(query_wallgreens(product, zc, page))
                if len(zip_records) >= stores_in_zipcode(zc):
                    break
            records += zip_records
    print records

# you probably want to memoize this since it's called deep in your loop
# @pug.decorators.memoize
def stores_in_zipcode(zipcode):
    return 5

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
    # statistics for real-valued columns:
    print df.describe()
    # unique record counts for all data columns (including strs):
    for col in df.columns:
        c = Counter(df[col])
        print '========== {N} ==========\n{col} item: count...'.format(N=len(c), col=col)
        print dict((k,v) for i,(k,v) in enumerate(c.iteritems()) if i < 20)


def query_walgreens(product, zipcode, page=1):
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
    db = query_walgreens.db
    return db[(db['product_id'] == product) & (db['zipcode'] == zipcode)].head(5)
    # return {"product_id": "e00d60d327046ad96439559e177a4ade361c8688", "store_id": "walgreens_11926", "zipcode": "76801_1", "ts": "2013-12-18 23:01:49", "availability": 0, "quantity": 0}
# maintain a single copy of the database (a pandas dataframe) in RAM
query_walgreens.db = load_dataframe()
