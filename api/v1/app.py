#!/usr/bin/python3
""" Flask app """

from models import storage
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_request(exception=None):
    """
    Method to close the connection when the execution finish
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Method to manage the url's that doesn't exists
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """
    Main function
    """
    my_host = environ.get("HBNB_API_HOST")
    my_port = environ.get("HBNB_API_PORT")
    app.run(host=my_host, port=my_port, threaded=True)
