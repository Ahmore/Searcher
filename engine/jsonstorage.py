import json


class JSONStorage:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        with open(self.filename) as json_data:
            return json.load(json_data)

    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)