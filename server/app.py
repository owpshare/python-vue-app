from flask import Flask, jsonify, send_from_directory, Response
import os
import random
from werkzeug.exceptions import NotFound

from server.calculator import get_baltic_electricity_prices

app = Flask(__name__)

def build_directory_report():
    directories = [os.getcwd(), "/home/site/wwwroot", "/home/site/wwwroot/dist"]
    lines = ["Running the Flask application..."]

    for directory in directories:
        lines.append(f"Directory: {directory}")
        if not os.path.isdir(directory):
            lines.extend(["All items: unavailable", "Files only: unavailable", ""])
            continue

        entries = os.listdir(directory)
        files_only = [f for f in entries if os.path.isfile(os.path.join(directory, f))]
        lines.extend([f"All items: {entries}", f"Files only: {files_only}", ""])
    report = "\n".join(lines)
    print(report)
    return report


@app.route('/files')
def logs():
    report = build_directory_report()
    return Response(report, mimetype='text/plain')

@app.route('/prices')
def get_prices():
    prices = get_baltic_electricity_prices()
    return prices


@app.route('/version')
def get_version():
    return jsonify({"version": "1.0.2"})


@app.route('/api/random-number', methods=['GET'])
def get_random_number():
    return jsonify({"number": random.randint(1, 100)})


def get_dist_path():
    dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))
    if not os.path.isdir(dist_path):
        dist_path = "/home/site/wwwroot/dist"
    return dist_path if os.path.isdir(dist_path) else None


@app.route('/')
def get_index():
    dist_path = get_dist_path()
    if not dist_path:
        return "File not found", 404
    return send_from_directory(dist_path, "index.html")


@app.route('/<path:path>')
def get_frontend_path(path):
    dist_path = get_dist_path()
    if not dist_path:
        return "File not found", 404
    try:
        return send_from_directory(dist_path, path)
    except NotFound:
        return send_from_directory(dist_path, "index.html")

if __name__ == '__main__':
    app.run()
