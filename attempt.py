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

   A correct and complete strategy would be to query a zipcode not in those already found for each individual product until all zipcodes have been queried at least once for each product. This seem like an O(N*M) solution, where N is the number of zipcodes and M the number of product types.

   """
