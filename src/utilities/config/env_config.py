from dotenv import load_dotenv


def _load_env_config():
    load_dotenv(".env")


load = (lambda: _load_env_config)()