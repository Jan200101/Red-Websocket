import json

class DataIO:
    def load_json(self, filename):
        with open(filename, "r") as fd:
            print(fd)
            return json.load(fd)

    def save_json(self, filename, content):
        with open(filename, "w") as fd:
            json.dump(content, fd)
        return True

    def is_valid_json(self, filename):
        try:
            self.load_json(filename)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return False
        return True

dataIO = DataIO()