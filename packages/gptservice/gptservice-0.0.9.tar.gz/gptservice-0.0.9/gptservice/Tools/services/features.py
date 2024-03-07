from abc import ABC

class Service(ABC):
    
    @property
    def service(self):
        return self.service
    
    @property
    def content(self):
        return self.content
    
    @property
    def tools(self):
        return self.tools