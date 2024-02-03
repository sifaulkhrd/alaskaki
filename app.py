from flask import Flask, request
from models.login import get_username
from models import register 
from controller import register_controller
from controller import login_controller
from controller import kategori_controller
from controller import produk_controller
from controller import keranjang_controller
from controller import transaksi_controller
from models import produk
from models import keranjang
from db import conn
from models import user
from models import kategori
from models import transaksi
from models import transaksi_detail
import time
import os




from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "ini token nya"
CORS(app)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)


# ini untuk registrasi
@app.post('/register')
def register_new_data():
    """
    Endpoint untuk menangani registrasi data baru.

    Returns:
    - HTTP Response: Respons dari fungsi register_new_data_controller.
    """
    return register_controller.register_new_data_controller()

    
# ini untuk login
@app.post('/login')
def login():
    """
    Endpoint untuk menangani proses login pengguna.

    Returns:
    - HTTP Response: Respons dari fungsi login_user_controller.
    """
    return login_controller.login_user_controller()




# ini untuk token
@app.get('/protected')
@jwt_required()
def protected():
    """
    Endpoint yang memerlukan token akses untuk akses.

    Returns:
    - HTTP Response: Respons yang menunjukkan pengguna yang terautentikasi.
    """
    current_user = get_jwt_identity()
    return {'logged as': current_user["fullname"]}, 200



# ========================================CRUD=KATEGORI====================================================
# melihat semua kategori
@app.get("/kategori")
def get_all_kategori():
    """
    Endpoint untuk mendapatkan semua kategori produk.

    Returns:
    - HTTP Response: Respons dari fungsi get_all_kategori.
    """
    return kategori.get_all_kategori()


# melihat kategori menggunakan id
@app.get("/kategori/<int:id>")
def get_all_kategori_by_id(id):
    """
    Endpoint untuk mendapatkan kategori berdasarkan ID beserta produk yang terkait.

    Args:
    - id (int): ID kategori yang dicari.

    Returns:
    - HTTP Response: Respons dari fungsi kategori_by_id.
    """
    return kategori_controller.kategori_by_id(id)



# melihat produk yang ada di kategori
@app.get('/kategori/<int:kategori_id>/produk')
def get_all_produk_by_kategori(kategori_id):
    """
    Endpoint untuk mendapatkan semua produk berdasarkan ID kategori.

    Args:
    - kategori_id (int): ID kategori yang dicari.

    Returns:
    - HTTP Response: Respons dari fungsi kategori_id_produk_controller.
    """
    return kategori_controller.kategori_id_produk_controller(kategori_id)


# ========================================CRUD=PRODUK======================================================


@app.get('/produk')
def get_produk():
    """
    Endpoint untuk mendapatkan semua produk dengan batasan halaman, limit, dan filter opsional.

    Returns:
    - HTTP Response: Respons dari fungsi get_all_produk_controller.
    """
    return produk_controller.get_all_produk_controller()



# ini untuk melihat produk menggunakan id
@app.get("/produk/<int:id>")
def get_produk_by_id(id):
    """
    Endpoint untuk mendapatkan satu produk bersama gambar berdasarkan ID.

    Args:
    - id (int): ID produk yang dicari.

    Returns:
    - HTTP Response: Respons dari fungsi get_produk_id.
    """
    return produk_controller.get_produk_id(id)



# ini untuk menambahkan produk
@app.post("/tambah_produk")
def create_new_produk():
    """
    Endpoint untuk menambahkan produk baru.

    Returns:
    - HTTP Response: Respons dari fungsi buat_produk_baru.
    """
    return produk_controller.buat_produk_baru()



# ini untuk mengedit data produk
@app.put("/produk/<int:id>")
def update_produk_by_id(id):
    """
    Endpoint untuk mengedit data produk berdasarkan ID.

    Args:
    - id (int): ID produk yang akan diubah.

    Returns:
    - HTTP Response: Respons dari fungsi edit_produk.
    """
    return produk_controller.edit_produk(id)


# ini untuk menghapus produk
@app.delete("/produk/<int:id>")
def delete_produk_by_id(id):
    """
    Endpoint untuk menghapus produk berdasarkan ID.

    Args:
    - id (int): ID produk yang akan dihapus.

    Returns:
    - HTTP Response: Respons dari fungsi hapus_produk.
    """
    return produk_controller.hapus_produk(id)


# ========================================CRUD=KERANJANG======================================================

# ini untuk menambah pesanan
@app.post("/keranjang")
@jwt_required()
def create_new_keranjang():
    """
    Endpoint untuk menambahkan produk ke dalam keranjang pengguna.

    Returns:
    - HTTP Response: Respons dari fungsi masukan_pesanan.
    """
    return keranjang_controller.masukan_pesanan()


# Ini adalah endpoint untuk melihat semua pesanan
@app.get('/keranjang')
@jwt_required()
def get_data_keranjang():
    """
    Mengambil semua data keranjang dari database dan mengembalikannya sebagai respons.

    Returns:
    - Response: Objek respons HTTP yang berisi data keranjang.

    Note:
    - Fungsi ini memanfaatkan fungsi `get_all_keranjang` dari modul 'keranjang'.
    """
    # Memanggil fungsi dari modul 'keranjang' untuk mendapatkan semua data keranjang
    return keranjang_controller.get_all_keranjang_by_user()


# Ini adalah endpoint untuk melihat pesanan menggunakan ID
@app.get("/keranjang/<int:id>")
@jwt_required()
def get_keranjang_by_id(id):
    """
    Endpoint untuk melihat detail pesanan berdasarkan ID pesanan.

    Args:
    - id (int): ID pesanan.

    Returns:
    - HTTP Response: Respons dari fungsi lihat_pesanan_by_id.
    """
    return keranjang_controller.lihat_pesanan_by_id(id)


# Ini adalah endpoint untuk menghapus pesanan
@app.delete("/keranjang/<int:id>")
@jwt_required()
def delete_keranjang_by_id_and_user_id(id):
    """
    Endpoint untuk menghapus pesanan berdasarkan ID pesanan dan ID pengguna.

    Args:
    - id (int): ID pesanan.

    Returns:
    - HTTP Response: Respons dari fungsi hapus_pesanan.
    """
    jwt_user = get_jwt_identity()
    user_id = jwt_user["id"]
    return keranjang_controller.hapus_pesanan(id, user_id)



# ========================================CRUD=TRANSAKSI======================================================

# Ini adalah endpoint untuk menambahkan data transaksi
@app.post("/transaksi")
@jwt_required()
def create_new_transaksi():
    """
    Endpoint untuk membuat transaksi baru.

    Returns:
    - HTTP Response: Respons dari fungsi masukan_data_transaksi.
    """
    return transaksi_controller.masukan_data_transaksi()


@app.post("/transaksi/keranjang")
@jwt_required()
def transaksi_from_keranjang():
    """
    Menangani permintaan transaksi dari keranjang belanja.

    Requires:
    - Terdapat token JWT yang valid.

    Returns:
    - Jika transaksi berhasil: {'message': 'transaksi berhasil ditambahkan'}
    - Jika terdapat kesalahan: {'message': 'pesan kesalahan', 'data': []}
    """
    return transaksi_controller.transaksi_dari_keranjang()


# Ini adalah endpoint untuk melihat semua transaksi
@app.get('/transaksi')
def get_all_transaksi():
    if not transaksi.get_all_transaksi():
        return [{"message":"belum ada transaksi"},{"data": []}]
    # Memanggil fungsi dari modul 'transaksi' untuk mendapatkan semua data transaksi
    return transaksi.get_all_transaksi()

@app.get("/transaksi/<int:id>")
@jwt_required()
def get_transaksi_by_id(id):
    """
    Mendapatkan informasi transaksi berdasarkan ID.

    Requires:
    - Terdapat token JWT yang valid.

    Parameters:
    - id: ID transaksi yang akan dilihat detailnya.

    Returns:
    - Jika transaksi ditemukan: Informasi lengkap transaksi beserta detailnya.
    - Jika transaksi tidak ditemukan: {'message': 'transaksi tidak ditemukan'}
    """
    return transaksi_controller.lihat_transaksi_detail(id)

@app.delete("/transaksi/<int:transaksi_id>")
@jwt_required()
def delete_transaksi(transaksi_id: int):
    """
    Menghapus data transaksi berdasarkan ID.

    Requires:
    - Terdapat token JWT yang valid.

    Parameters:
    - transaksi_id: ID transaksi yang akan dihapus.

    Returns:
    - Jika transaksi berhasil dihapus: {'message': 'Transaksi berhasil dihapus'}
    - Jika transaksi tidak ditemukan: {'message': 'Transaksi tidak ditemukan'}
    - Jika terjadi kesalahan lainnya: {'message': 'pesan kesalahan'}
    """
    return transaksi_controller.hapus_data_transaksi(transaksi_id)













# # Ini adalah endpoint untuk menghapus data transaksi berdasarkan ID
# @app.delete("/transaksi/<int:id>")
# def delete_transaksi_by_id(id):
#     """
#     Menghapus data transaksi berdasarkan ID.

#     Parameters:
#     - id (int): ID transaksi yang akan dihapus.

#     Returns:
#     - dict: Pesan keberhasilan atau pesan kesalahan beserta kode status.

#     Note:
#     - Fungsi ini memanfaatkan fungsi `get_transaksi_by_id` dan `delete_transaksi_by_id` dari modul 'transaksi'.
#     """
#     # Memeriksa apakah data transaksi dengan ID yang diberikan ditemukan atau tidak
#     if transaksi.get_transaksi_by_id(id) is None:
#         return {'message': 'Data transaksi tidak ditemukan'}

#     # Memanggil fungsi dari modul 'transaksi' untuk menghapus data transaksi berdasarkan ID
#     transaksi.delete_transaksi_by_id(id)

#     # Memberikan respons bahwa data transaksi berhasil dihapus
#     return {'message': 'Data transaksi berhasil dihapus'}, 200


# ========================================CRUD=TRANSAKSI=DETAIL=============================================

# Ini adalah endpoint untuk menambahkan data transaksi detail
@app.post("/transaksi_detail")
def create_new_transaksi_details():
    """
    Menambahkan data transaksi detail baru berdasarkan input dari pengguna.

    Returns:
    - dict: Pesan keberhasilan atau pesan kesalahan.

    Note:
    - Fungsi ini memanfaatkan fungsi `get_produk_by_id`, `get_transaksi_by_id`, dan `create_new_transaksi_detail`
      dari modul 'produk', 'transaksi', dan 'transaksi_detail'.
    """
    # Mengambil data input dari formulir atau payload
    produk_id = request.form.get("produk_id")
    harga = request.form.get("harga")
    kuantitas = request.form.get("kuantitas")
    transaksi_id = request.form.get("transaksi_id")


    # Memeriksa apakah semua input telah diisi
    if not produk_id or not harga or not kuantitas or not transaksi_id:
        return {'message': 'Semua inputan harus diisi'}

    # Memeriksa apakah produk dengan ID yang diberikan ditemukan atau tidak
    if produk.get_produk_by_id(produk_id) is None:
        return {'message': 'Produk tidak ditemukan'}

    # Memeriksa apakah transaksi dengan ID yang diberikan ditemukan atau tidak
    if transaksi.get_transaksi_by_id(transaksi_id) is None:
        return {'message': 'Transaksi tidak ditemukan'}

    # Memeriksa apakah kuantitas dan harga merupakan angka yang lebih besar dari 0
    if not kuantitas.isdigit() or int(kuantitas) <= 0:
        return {'message': 'Kuantitas harus berupa angka dan lebih besar dari 0'}
    if not harga.isdigit() or int(harga) <= 0:
        return {'message': 'Harga harus berupa angka dan lebih besar dari 0'}

    # Memanggil fungsi dari modul 'transaksi_detail' untuk membuat data transaksi detail baru
    transaksi_detail.create_new_transaksi_detail(produk_id, harga, kuantitas, transaksi_id)

    produk.update_produk_stok(produk_id, kuantitas)
    # Memberikan respons bahwa data berhasil dimasukkan di transaksi detail
    return {'message': 'Data berhasil dimasukkan di transaksi detail'}


# Ini adalah endpoint untuk melihat semua data transaksi detail
@app.get('/transaksi_detail')
def get_all_transaksi_detail():
    """
    Mengambil semua data transaksi detail dari database dan mengembalikannya sebagai respons.

    Returns:
    - Response: Objek respons HTTP yang berisi data transaksi detail.

    Note:
    - Fungsi ini memanfaatkan fungsi `get_all_transaksi_detail` dari modul 'transaksi_detail'.
    """
    # Memanggil fungsi dari modul 'transaksi_detail' untuk mendapatkan semua data transaksi detail
    return transaksi_detail.get_all_transaksi_detail()


# Ini adalah endpoint untuk menghapus data transaksi detail berdasarkan ID
@app.delete("/transaksi_detail/<int:id>")
def delete_transaksi_detail_by_id(id):
    """
    Menghapus data transaksi detail berdasarkan ID.

    Parameters:
    - id (int): ID transaksi detail yang akan dihapus.

    Returns:
    - dict: Pesan keberhasilan atau pesan kesalahan beserta kode status.

    Note:
    - Fungsi ini memanfaatkan fungsi `get_transaksi_detail_by_id` dan `delete_transaksi_detail_by_id`
      dari modul 'transaksi_detail'.
    """
    # Memeriksa apakah data transaksi detail dengan ID yang diberikan ditemukan atau tidak
    if transaksi_detail.get_transaksi_detail_by_id(id) is None:
        return {'message': 'Data transaksi detail tidak ditemukan'}

    # Memanggil fungsi dari modul 'transaksi_detail' untuk menghapus data transaksi detail berdasarkan ID
    transaksi_detail.delete_transaksi_detail_by_id(id)

    # Memberikan respons bahwa data transaksi detail berhasil dihapus
    return {'message': 'Data transaksi detail berhasil dihapus'}, 200


if __name__==('main'):
    app.run(debug=True, use_reloader=True, host="0.0.0.0")