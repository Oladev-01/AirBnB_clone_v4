from flask import jsonify
from app_views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns JSON with status: OK"""
    return jsonify({"status": "OK"})
