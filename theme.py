import json

Theme = None

def load_theme(filepath = "themes/basic.json"):
    global Theme
    with open(filepath, encoding="UTF_8") as data:
        Theme = json.dumps(data.read())

""" class Theme():
    def load(filepath = "themes/basic.txt"):
        with open(filepath, 'r', encoding = "UTF-8") as f:
            Theme.hor = f.readline().strip()
            Theme.vert = f.readline().strip()
            Theme.tl = f.readline().strip()
            Theme.tr = f.readline().strip()
            Theme.bl = f.readline().strip()
            Theme.br = f.readline().strip()
            Theme.block = f.readline().strip()

    def load_json(filepath = "themes/basic.txt"):
        with open(filepath) as data:
            self.theme = json.load(data) """
