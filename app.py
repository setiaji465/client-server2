from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/mahasiswa'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

#Rohmat setiaji 18090119 4B

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/admin/')
def admin_page():
    return 'Ini adalah halaman admin'


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/HelloWorld')


class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(8),unique=True)
    nama_mhs = db.Column(db.String(60))
    email = db.Column(db.String(100))
    alamat = db.Column(db.String(100))

    def __init__(self, nim, nama_mhs, email, alamat):
        self.nim = nim
        self.nama_mhs = nama_mhs
        self.email = email
        self.alamat = alamat

    @staticmethod
    def get_all_mhs():
        return Mahasiswa.query.all()


class MahasiswaSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nim', 'nama_mhs', 'email', 'alamat')


mahasiswa_schema =  MahasiswaSchema()
mhs_schema =  MahasiswaSchema(many=True)


@app.route('/mahasiswa', methods=["POST"])
def add_mahasiswa():
    nim = request.json['nim']
    nama_mhs = request.json['nama_mhs']
    email = request.json['email']
    alamat = request.json['password']
    new_mahasiswa = Mahasiswa(nim=nim,nama_mhs=nama_mhs,email=email,alamat=alamat)
    db.session.add(new_mahasiswa)
    db.session.commit()
    return jsonify(person.dump(new_mahasiswa))

@app.route("/mahasiswa", methods=["GET"])
def get_mahasiswa():
    all_mhs = Mahasiswa.get_all_mhs()
    result = mhs_schema.dump(all_mhs)
    return jsonify(result)


@app.route('/mahasiswa/<int:id>',methods=["PUT"])
def get_mahasiswa(id):
    mahasiswa_data = Mahasiswa.query.get(id)
    mahasiswa_data.nim = request.json['nim']
    mahasiswa_data.nama_mhs = request.json['nama_mhs']
    mahasiswa_data.email = request.json['email']
    mahasiswa_data.alamat = request.json['alamat']
    db.session.commit()
    return jsonify(person.dump(mahasiswa_data))

@app.route('/person/<int:id>',methods=["DELETE"])
def person_delete(id):
    mahasiswa_data = Mahasiswa.query.get(id)
    db.session.delete(mahasiswa_data)
    db.session.commit()
    return jsonify(person.dump(mahasiswa_data))

if __name__ == '__main__':
    app.run()
