from flask import Flask
from app.api import ping, product_list

ACTIVE_ENDPOINTS = (
    ("/", ping),
    ("/api/v1/", product_list)
)

def create_app():
    app = Flask(__name__)
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)
    return app