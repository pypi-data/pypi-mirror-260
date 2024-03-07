from .features import Service


class shopping(Service):

    @property
    def service(self):
        return "GoogleShopping"
    
    @property
    def content(self):
        return "You are a shopping assistant. Provide me the top 3 shopping results. Only get the title, price and link for each item in natural language."
    
    @property
    def tools(self):
        return   {
      "name": "extractShoppingDetail",
      "description": "Extract shopping detail from the user prompt",
      "parameters": {
        "type": "object",
        "properties": {
          "item": {
            "type": "string",
            "description": "The item name"
          },
          "amount": {
            "type": "number",
            "description": "The amount of the item"
          },
          "brand": {
            "type": "string",
            "description": "The brand of the item"
          },
          "price": {
            "type": "number",
            "description": "The price of the item"
          }
        },
        "required": ["query"]
      }
    }