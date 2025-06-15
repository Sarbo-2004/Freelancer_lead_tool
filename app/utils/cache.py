import json

def save_json(path: str, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_json(path: str):
    with open(path, "r") as f:
        data = json.load(f)
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        return data
