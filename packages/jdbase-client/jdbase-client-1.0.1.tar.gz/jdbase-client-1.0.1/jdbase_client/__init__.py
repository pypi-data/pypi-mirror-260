import requests as req


class Database:
    def __init__(self, config) -> None:
        self.api_key = config['api_key']
        self.db = config['db']
        self.api_endpoint = config['api_endpoint']
        self.headers = {
            'api_key': self.api_key
        }

    def create(self, query):
        data = {
            'db': self.db,
            'query': query,
            'type': 'create'
        }
        return req.post(self.api_endpoint, headers=self.headers, json=data).json()
    
    def get_by(self, query):
        data = {
            'db': self.db,
            'query': query,
            'type': 'read'
        }
        return req.post(self.api_endpoint, headers=self.headers, json=data).json()
    
    def update(self, query, update_query):
        data = {
            'db': self.db,
            'query': query,
            'type': 'update',
            'update_query': update_query
        }
        return req.post(self.api_endpoint, headers=self.headers, json=data).json()
    
    def delete(self, query):
        data = {
            'db': self.db,
            'query': query,
            'type': 'delete'
        }
        return req.post(self.api_endpoint, headers=self.headers, json=data).json()
    
    def match(self, query):
        data = {
            'db': self.db,
            'query': query,
            'type': 'match'
        }
        return req.post(self.api_endpoint, headers=self.headers, json=data).json()
    
    def create_db(self, query):
        data = {
            'db': self.db,
            'type': 'create_db',
            'query': query
        }
        return req.post(self.api_endpoint, headers=self.headers, json=data).json()
    

