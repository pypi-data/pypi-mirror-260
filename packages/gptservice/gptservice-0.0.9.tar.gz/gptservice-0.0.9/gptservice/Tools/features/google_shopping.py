import os
import json
import serpapi

serpapi_key = os.environ.get('serpapi_key')

class GoogleShopping:
    def __init__(self, **args):
        self.item = args.get('item')
        self.brand = args.get('brand')
        self.price = args.get('price')
        self.amount = args.get('amount')

    def invoke_service(self):
        try:
            search = serpapi.GoogleSearch({
                "engine": "google_shopping",
                "q": self.brand + " " + self.item,
                "hl": "en",
                "gl": "in",
                "tbm": "mr:1,price:1,ppr_max:{}".format(self.price),
                "api_key": os.environ.get('serpapi_key')
            })

            results = search.get_dict()
            products = results['shopping_results'][:3]
            # print(products)
            return products
        
        except Exception as e:
            print('Error extracting shopping details')
            print(e)
            return