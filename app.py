from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@172.17.0.3/SuperVoices'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Users(db.Model):
    email = db.Column(db.String(100), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    pwd = db.Column(db.String(100), nullable=False)

    def __init__(self, email, name, pwd, last_name):
        self.email = email
        self.name = name
        self.pwd = pwd
        self.last_name = last_name


class Companies(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin_email = db.Column(db.String(100), db.ForeignKey('users.email'))

    def __init__(self, id, name, admin_email):
        self.id = id
        self.name = name
        self.admin_email = admin_email


class AccesLevel(db.Model):
    email = db.Column(db.String(100), db.ForeignKey('users.email'), nullable=False, primary_key=True)
    access_level = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, primary_key=True)

    def __init__(self, email, access_level, company_id):
        self.email = email
        self.access_level = access_level
        self.company_id = company_id


class Contests(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    banner = db.Column(db.String(100), nullable=False)
    contest_url = db.Column(db.String(100), nullable=False)
    starting_date = db.Column(db.DateTime(), nullable=False)
    ending_date = db.Column(db.DateTime(), nullable=False)
    voice_price_tag = db.Column(db.Integer)
    script = db.Column(db.String(200))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    email = db.Column(db.String(100), db.ForeignKey('users.email'), nullable=False)

    def __init__(self, id, name, banner, contest_url, starting_date, ending_date, voice_preice_tag, script, company_id, email):
        self.id = id
        self.name = name
        self.banner = banner
        self.contest_url = contest_url
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.voice_price_tag = voice_preice_tag
        self.script = script
        self.email = email
        self.company_id = company_id


class Voices(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    voice_url = db.Column(db.String(100), nullable=False)
    contest_id = db.Column(db.Integer, db.ForeignKey('contests.id'), nullable=False)
    status = db.Column(db.String(100), default='Created')
    email = db.Column(db.String(100), db.ForeignKey('users.email'), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, id, voice_url, contest_id, status, email, created_at):
        self.id = id
        self.voice_url = voice_url
        self.contest_id = contest_id
        self.status = status
        self.email = email
        self.created_at = created_at


db.create_all()


@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
