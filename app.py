from flask import Flask, jsonify, request  # Corrected import
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)

class Pegawai(db.Model):
    __tablename__ = 'pegawai'
    id = db.Column(db.String(10), primary_key=True)
    nama = db.Column(db.String(100))
    pengalaman = db.Column(db.String(100))
    jabatan = db.Column(db.String(100))
    umur = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'pengalaman': self.pengalaman,  # Corrected to match attribute name
            'jabatan': self.jabatan,
            'umur': self.umur
        }


@app.route('/cek_koneksi_db', methods=['GET'])
def cek_koneksi_db():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'message': 'Koneksi database Berhasil'}), 200
    except OperationalError:
        return jsonify({'message': 'Koneksi database Gagal'}), 500

@app.route('/Pegawai', methods=['GET'])
def get_Pegawai():
    pegawai = Pegawai.query.all()
    return jsonify([m.to_dict() for m in pegawai])

@app.route('/Pegawai/<int:id>', methods=['GET'])  # Corrected to <int:id>
def get_Pegawai_by_id(id):
    pegawai = Pegawai.query.get(id)
    if pegawai:
        return jsonify(pegawai.to_dict())
    else:
        return jsonify({'message': 'Data pegawai tidak ditemukan'}), 404

@app.route('/tambah_Pegawai', methods=['POST'])
def add_Pegawai():
    
    new_id = request.form.get('id')  # Corrected to request.form.get
    new_nama = request.form.get('nama')
    new_pengalaman = request.form.get('pengalaman')
    new_jabatan = request.form.get('jabatan')
    new_umur = request.form.get('umur')

    new_pegawai = Pegawai(id=new_id, nama=new_nama, pengalaman=new_pengalaman, jabatan=new_jabatan, umur=new_umur)
    db.session.add(new_pegawai)
    db.session.commit()
    return jsonify({'message': 'Data pegawai berhasil ditambahkan'}), 201

@app.route('/update_Pegawai/<int:id>', methods=['PUT'])  # Corrected to <int:id>
def update_Pegawai(id):
    
    pegawai = Pegawai.query.get(id)
    if pegawai:
        pegawai.id = request.form.get('id')
        pegawai.nama = request.form.get('nama')
        pegawai.pengalaman = request.form.get('pengalaman')
        pegawai.jabatan = request.form.get('jabatan')
        pegawai.umur = request.form.get('umur')
        db.session.commit()
        return jsonify({'message': 'Data pegawai berhasil diupdate'})
    else:
        return jsonify({'message': 'Data pegawai tidak ditemukan'}), 404

@app.route('/delete_Pegawai/<int:id>', methods=['DELETE'])  # Corrected to <int:id>
def delete_Pegawai(id):
    pegawai = Pegawai.query.get(id)
    if pegawai:
        db.session.delete(pegawai)
        db.session.commit()
        return jsonify({'message': 'Data pegawai berhasil dihapus'})
    else:
        return jsonify({'message': 'Data pegawai tidak ditemukan'}), 404

if __name__ == '__main__':
    app.run(debug=True)