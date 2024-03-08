import json
import logging
import sys

from flask import Flask

from .helpers import killport
from .pages.index import index_page_creator
from .pages.trace import trace_page_creator

PORT = 5000


def launch_iframe(width, height):
    try:
        from google.colab.output import eval_js

        webpage_url = eval_js(f"google.colab.kernel.proxyPort({PORT})")
        from IPython.display import IFrame

        return IFrame(webpage_url, width, height)
    except:
        pass


def launch_app(results: list, width=800, height=400):
    try:
        killport(PORT)
    except:
        pass
    logging.getLogger("werkzeug").setLevel(logging.WARN)
    cli = sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None
    app = Flask(__name__, static_url_path="")

    app.register_blueprint(index_page_creator({"results": results}))
    app.register_blueprint(trace_page_creator({"results": results}))
    from threading import Thread

    thread = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": PORT})
    thread.start()
    # Returning is important
    return launch_iframe(width, height)


if __name__ == "__main__":
    results = []
    with open("results.json") as f:
        results = json.loads(f.read())
    from threading import Thread

    thread = Thread(
        target=launch_app, kwargs={"results": results, "width": 800, "height": 400}
    )
    thread.start()
