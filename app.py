from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Inisialisasi Flask
app = Flask(__name__)

# Konfigurasi database SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi SQLAlchemy
db = SQLAlchemy(app)

# Model untuk tabel File
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Buat database (jika belum ada)
with app.app_context():
    db.create_all()

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# API untuk mengambil semua file
@app.route('/api/files', methods=['GET'])
def get_files():
    files = File.query.all()
    files_data = [{"id": file.id, "name": file.name, "content": file.content} for file in files]
    return jsonify(files_data)

# API untuk menyimpan file baru
@app.route('/api/files', methods=['POST'])
def save_file():
    data = request.json
    new_file = File(name=data['name'], content=data['content'])
    db.session.add(new_file)
    db.session.commit()
    return jsonify({"message": "File berhasil disimpan!", "id": new_file.id})

# API untuk menghapus file
@app.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file = File.query.get(file_id)
    if file:
        db.session.delete(file)
        db.session.commit()
        return jsonify({"message": "File berhasil dihapus!"})
    return jsonify({"message": "File tidak ditemukan!"}), 404

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
