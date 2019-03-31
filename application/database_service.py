from application.metrics_model import Metrics
from application import db


def get_result():
    query = db.session.query(Metrics)
    return {'results': query.all()}
