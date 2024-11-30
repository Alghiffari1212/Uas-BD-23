from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mahasiswa(db.Model):
    _tablename_ = 'mahasiswa'
    NIM = db.Column(db.BigInteger, primary_key=True)
    nama_mahasiswa = db.Column(db.String(100), nullable=False)
    alamat_mahasiswa = db.Column(db.String(200), nullable=True)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)

    def _repr_(self):
        return f"<Mahasiswa {self.nama_mahasiswa}>"


class MataKuliah(db.Model):
    _tablename_ = 'mata_kuliah'
    kode_mk = db.Column(db.String(16), primary_key=True)
    nama_mk = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)

    def _repr_(self):
        return f"<MataKuliah {self.nama_mk}>"


class JadwalKuliah(db.Model):
    _tablename_ = 'jadwal_kuliah'
    id_jadwal = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hari = db.Column(db.String(20), nullable=False)
    jam_mulai = db.Column(db.Time, nullable=False)
    jam_selesai = db.Column(db.Time, nullable=False)

    def _repr_(self):
        return f"<JadwalKuliah {self.hari} ({self.jam_mulai}-{self.jam_selesai})>"


class MahasiswaKeJadwal(db.Model):
    _tablename_ = 'mahasiswa_ke_jadwal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mahasiswa_id = db.Column(db.BigInteger, db.ForeignKey('mahasiswa.NIM'), nullable=False)
    jadwal_kuliah_id = db.Column(db.Integer, db.ForeignKey('jadwal_kuliah.id_jadwal'), nullable=False)

    mahasiswa = db.relationship('Mahasiswa', backref='jadwal_mahasiswa')
    jadwal_kuliah = db.relationship('JadwalKuliah', backref='mahasiswa_jadwal')

    def _repr_(self):
        return f"<MahasiswaKeJadwal {self.mahasiswa.nama_mahasiswa} - {self.jadwal_kuliah}>"


class MatkulKeJadwal(db.Model):
    _tablename_ = 'matkul_ke_jadwal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mata_kuliah_id = db.Column(db.String(16), db.ForeignKey('mata_kuliah.kode_mk'), nullable=False)
    jadwal_kuliah_id = db.Column(db.Integer, db.ForeignKey('jadwal_kuliah.id_jadwal'), nullable=False)

    mata_kuliah = db.relationship('MataKuliah', backref='jadwal_matkul')
    jadwal_kuliah = db.relationship('JadwalKuliah', backref='matkul_jadwal')

    def _repr_(self):
        return f"<MatkulKeJadwal {self.mata_kuliah.nama_mk} - {self.jadwal_kuliah}>"