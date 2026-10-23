import yaml


class Config:
    def __init__(self, data):
        self.database_url = data["database_url"]
        self.log_level = data.get("log_level", "info")


def load_config(path="config.yaml"):
    with open(path) as f:
        return Config(yaml.safe_load(f))
