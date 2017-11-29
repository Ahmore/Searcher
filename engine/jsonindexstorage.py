import json


class JSONIndexStorage:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        with open(self.filename) as json_data:
            return json.load(json_data)

    def save(self, data):
        print("saving...")
        with open(self.filename, 'w') as f:
            json.dump(data, f)