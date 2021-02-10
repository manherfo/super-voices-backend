from flask import Flask, request
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

    def __init__(self, email, name, last_name, pwd):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.pwd = pwd


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

    def __init__(self, id, name, banner, contest_url, starting_date, ending_date, voice_preice_tag, script, company_id,
                 email):
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


class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'name', 'last_name', 'pwd')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class CompanySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'admin_email')


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


class AccessLevelSchema(ma.Schema):
    class Meta:
        fields = ('email', 'access_level', 'company_id')


access_level_schema = AccessLevelSchema()
access_levels_schema = AccessLevelSchema(many=True)


class ContestSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'banner', 'contest_url', 'starting_date', 'ending_date', 'voice_preice_tag', 'script',
                  'company_id', 'email')


contest_schema = ContestSchema()
contests_schema = ContestSchema(many=True)


class VoiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'voice_url', 'contest_id', 'status', 'email', 'created_at')


voice_schema = ContestSchema()
voices_schema = ContestSchema(many=True)


@app.route('/signups', methods=['PUT'])
def create_task():
    new_email = request.json['email']
    new_name = request.json['name']
    new_last_name = request.json['last_name']
    new_pwd = request.json['pwd']
    new_user = Users(new_email, new_name, new_last_name, new_pwd)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
