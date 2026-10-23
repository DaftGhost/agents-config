from app.config import load_config

config = load_config()


def run():
    print(f"connecting to {config.database_url}")
