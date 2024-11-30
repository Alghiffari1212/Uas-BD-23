from flask import Flask, request, jsonify, session
from flask_alchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# Model Mahasiswa
class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    NIM = db.Column(db.BigInteger, primary_key=True)
    nama_mahasiswa = db.Column(db.String(100), nullable=False)
    alamat_mahasiswa = db.Column(db.String(200), nullable=True)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Mahasiswa {self.nama_mahasiswa}>"

# Endpoint untuk registrasi
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('NIM') or not data.get('nama_mahasiswa') or not data.get('password'):
        return jsonify({'message': 'NIM, nama, dan password wajib diisi!'}), 400

    if Mahasiswa.query.get(data['NIM']):
        return jsonify({'message': 'NIM sudah terdaftar!'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_mahasiswa = Mahasiswa(
        NIM=data['NIM'],
        nama_mahasiswa=data['nama_mahasiswa'],
        alamat_mahasiswa=data.get('alamat_mahasiswa'),
        tanggal_lahir=data['tanggal_lahir'],
        jenis_kelamin=data['jenis_kelamin'],
        password=hashed_password
    )
    db.session.add(new_mahasiswa)
    db.session.commit()

    return jsonify({'message': 'Registrasi berhasil!'}), 201

# Endpoint untuk login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data.get('NIM') or not data.get('password'):
        return jsonify({'message': 'NIM dan password wajib diisi!'}), 400

    mahasiswa = Mahasiswa.query.get(data['NIM'])
    if not mahasiswa or not check_password_hash(mahasiswa.password, data['password']):
        return jsonify({'message': 'NIM atau password salah!'}), 401

    session['nim'] = mahasiswa.NIM
    return jsonify({'message': 'Login berhasil!', 'NIM': mahasiswa.NIM}), 200

# Endpoint untuk logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('nim', None)
    return jsonify({'message': 'Logout berhasil!'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
