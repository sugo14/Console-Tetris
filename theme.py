import json

class Theme():
    obj = None

    def load_theme(filepath = "themes/clean.json"):
        with open(filepath, encoding="UTF_8") as data:
            Theme.obj = json.load(data)

    def char(char_name):
        return Theme.obj["chars"][char_name] if (Theme.obj and char_name in Theme.obj["chars"]) else None
    
    def fg(tetromino):
        return Theme.obj["fg"]["tets"][tetromino] if (Theme.obj and tetromino in Theme.obj["fg"]["tets"]) else None
