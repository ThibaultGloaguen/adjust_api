from flask import Blueprint, jsonify
from application.database_service import get_result

views = Blueprint('views', __name__, url_prefix='/')


@views.route('/metrics', methods=['GET'])
def get_metrics_api():
    output = get_result()
    return jsonify(output)
