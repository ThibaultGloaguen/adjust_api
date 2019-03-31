from flask import Blueprint

views = Blueprint('views', __name__, url_prefix='/')


@views.route('/metrics', methods=['GET'])
def get_metrics_api():
    return 'mock'
