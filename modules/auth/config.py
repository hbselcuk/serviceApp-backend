import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class config:
    auth0_algorithms = os.environ.get("AUTH0_ALGORITHMS")
    auth0_api_audience = os.environ.get("AUTH0_API_AUDIENCE")
    auth0_issuer = os.environ.get("AUTH0_ISSUER")

def get_settings():
    return config