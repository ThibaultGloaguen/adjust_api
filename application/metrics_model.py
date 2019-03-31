from application import db


class Metrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    channel = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    os = db.Column(db.String(), nullable=False)
    impressions = db.Column(db.Integer(), nullable=False)
    clicks = db.Column(db.Integer(), nullable=False)
    installs = db.Column(db.Integer(), nullable=False)
    spend = db.Column(db.Integer(), nullable=False)
    revenue = db.Column(db.Integer(), nullable=False)
    cpi = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return '<Metrics %r >' % self.id
