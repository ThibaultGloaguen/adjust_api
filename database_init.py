from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + app.root_path + '/metrics.db'
db = SQLAlchemy(app)


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


if __name__ == '__main__':
    with open('sample_data.csv', 'rt') as csvfile:
        db.create_all()
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        next(spamreader)
        for row in spamreader:
            row = row[0].split(',')
            metric = Metrics(date=datetime.strptime(row[0], '%d.%m.%Y'),
                             channel=row[1],
                             country=row[2],
                             os=row[3],
                             impressions=row[4],
                             clicks=row[5],
                             installs=row[6],
                             spend=row[7],
                             revenue=row[8],
                             cpi=float(row[7]) / float(row[6]))
            db.session.add(metric)
        db.session.commit()
