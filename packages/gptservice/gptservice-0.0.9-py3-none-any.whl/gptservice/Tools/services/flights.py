from .features import Service


class flights(Service):

    @property
    def service(self):
        return "GoogleFlights"
    
    @property
    def content(self):
        return "As a Flight Booking Assistant, your task is to extract airport codes (IDs) from user input. Additionally, you should provide the top 3 cheapest flight options. For each option, include the price, arrival, departure, and a link, all in natural language."
    
    @property
    def tools(self):
        return   {
          "name": "extractFlightDetail",
          "description": "Extract Flight detail from the user prompt",
          "parameters": {
        "type": "object",
        "properties": {
          "arrival_id": {
            "type": "string",
            "description": "extract the arrival airport id where user will go"
          },
          "departure_id": {
            "type": "string",
            "description": "extract the departure airport id where user will depart"
          },
          "outbound_date": {
            "type": "string",
            "description": "The outbound date in YYYY-MM-DD format"
          },
          "return_date": {
            "type": "string",
            "description": "The return date in YYYY-MM-DD format"
          }
        },
        "required": ["query"]
          }
        }