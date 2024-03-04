import json

from flask import Flask

from .helpers import killport
from .pages.index import index_page_creator
from .pages.trace import trace_page_creator

PORT = 5000


def launch_app(results):
    try:
        killport(PORT)
    except:
        pass

    app = Flask(__name__, static_url_path="")

    app.register_blueprint(index_page_creator({"results": results}))
    app.register_blueprint(trace_page_creator({"results": results}))
    app.run(port=PORT)


if __name__ == "__main__":
    results = []
    with open("results.json") as f:
        results = json.loads(f.read())
    launch_app(results)
