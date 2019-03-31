from flask import request, jsonify, Blueprint, make_response, abort
from application.database_service import get_result
import sys

views = Blueprint('views', __name__, url_prefix='/')


@views.route('/metrics', methods=['GET'])
def get_metrics_api():
    try:
        fields = request.args.get('field')
        operation = request.args.get('operation')
        date_from = request.args.get('date_from')
        channel = request.args.get('channel')
        os = request.args.get('os')
        country = request.args.get('country')
        date_to = request.args.get('date_to')
        group_by = request.args.get('group_by')
        sort_by = request.args.get('sort_by')
        direction = request.args.get('direction')

        output = get_result(fields, operation, date_from, date_to, group_by, sort_by, direction, channel, os, country)

        return jsonify(output)
    except ValueError as e:
        abort(400, e)


@views.errorhandler(400)
def bad_request(error):
    sys.stderr.write("Request path: %s Request method: %s with error %s\n" %
                     (request.path, request.method, str(error)))
    return make_response(jsonify({'error': str(error)}), 400)


@views.errorhandler(500)
def server_error(error):
    sys.stderr.write("Request path: %s Request method: %s with error %s\n" %
                     (request.path, request.method, str(error)))
    return make_response(jsonify({'error': 'Internal error :('}), 500)
