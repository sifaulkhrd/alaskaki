from flask import Flask, request
from models.login import get_username
from models.register import validator_register_username, validator_register_password,validator_register_fullname, register_data
from models import produk
from models import keranjang
from models import user
from models import kategori


from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "ini token nya"

# ini untuk registrasi
@app.post('/register')
def register_new_data():
    username = request.form.get('username')
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    try:
        # ini untuk username
        if validator_register_username(username):
            return {'message': 'Username sudah digunakan oleh pengguna lain'}, 402
        if not username:
            return {'message': 'username harus diisi'}, 402
        
        # ini untuk password
        if validator_register_password(password):
            return {'message': 'Password sudah digunakan oleh pengguna lain'}, 402
        elif not password:
            return {'message': 'password harus diisi'}, 402
        elif len(password) < 8:
            return {'message': 'Password harus 8 karakter atau lebih'}, 402

        # ini untuk fullname
        if validator_register_fullname(fullname):
            return {'message': 'Fullname sudah di gunakan orang lain'}, 402
        elif not fullname:
            return {'message': 'Fullname harus diisi'}, 402
        
        # ini untuk registrasi
        register_data(username,password,fullname)
        return {'message': 'selamat registrasi telah berhasil'},200
    except Exception as e:
        raise e

# ini untuk login
@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    check_user_data = get_username(username,password)
    
    if check_user_data:
        token = create_access_token(identity=check_user_data['fullname'])
        return {'token':token}
    else:
       return {'message':'password atau username salah'}


# ini untuk token
@app.get('/protected')
@jwt_required()
def protected():
    currend_user = get_jwt_identity()
    return {'logged as': currend_user}, 200

# ========================================CRUD=PRODUK======================================================

# ini untuk melihat semua produck
@app.get('/produk')
def get_all_produk():
    return produk.get_all_produk()

# ini untuk melihat satu produk menggunakan id
@app.get("/produk/<int:id>")
def get_produk_by_id(id):
    item = produk.get_produk_by_id(id)
    if item is None:
        return {'message':'produck tidak di temukan'},402
    return item

# ini untuk menambahkan produk 
@app.post("/produk")
def create_new_produk():
    nama = request.form.get("nama")
    cover = request.form.get("cover")
    stok = request.form.get("stok")
    harga = request.form.get("harga")
    kategori_id = request.form.get("kategori_id")

    if not nama or not cover or not stok or not harga or not kategori_id:
        return {'message': 'semua inputan harus diisi'}

    if kategori.get_kategori_by_id(kategori_id) is None:
        return {'message':'kategori tidak di temukan'}

    produk.create_new_produk(nama,cover,stok,harga,kategori_id)
    return {'message':'produk berhasil di masukan'}

# ini untuk mengedit data produk
@app.put("/produk/<int:id>")
def update_produk_by_id(id):
    if produk.get_produk_by_id(id) is None:
        return {'message':'produk tidak di temukan'},404
    
    nama = request.form.get("nama")
    cover = request.form.get("cover")
    stok = request.form.get("stok")
    harga = request.form.get("harga")
    kategori_id = request.form.get("kategori_id")

    if not nama or not cover or not stok or not harga or not kategori_id:
        return {'message': 'semua inputan harus diisi'}

    if kategori.get_kategori_by_id(kategori_id) is None:
        return {'message':'kategori tidak di temukan'}

    produk.update_produk_by_id(
        id,
        nama,
        cover,
        stok,
        harga,
        kategori_id,
    )
    return {'message':'produk berhasil di edit'}

# ini untuk menghapus produk
@app.delete("/produk/<int:id>")
def delete_produk_by_id(id):
    if produk.get_produk_by_id(id) is None:
        return {'message':'produk tidak di temukan'}
    produk.delete_produk_by_id(id)
    return {'message':'produk berhasil di hapus'},200

# ========================================CRUD=KERANJANG======================================================

@app.post("/keranjang")
def create_new_keranjang():
    user_id = request.form.get("user_id")
    produk_id = request.form.get("produk_id")
    kuantitas = request.form.get("kuantitas")

    if not user_id or not produk_id or not kuantitas:
        return {'message': 'semua inputan harus diisi'}
    if user.get_users_by_id(user_id) is None:
        return {'message':'user tidak di temukan'}
    if produk.get_produk_by_id(produk_id) is None:
        return {'message':'produk tidak di temukan'}
    if not kuantitas.isdigit() or int(kuantitas) <= 0:
        return {'message':'kuantitas harus berupa angka dan lebih besar dari 0'}
    
    
    keranjang.create_new_keranjang(user_id,produk_id,kuantitas)
    return {'message':'produk berhasil di masukkan di keranjang'}

@app.get('/keranjang')
def get_all_keranjang():
    return keranjang.get_all_keranjang()

@app.get("/keranjang/<int:id>")
def get_keranjang_by_id(id):
    pesanan = keranjang.get_keranjang_by_id(id)
    if pesanan is None:
        return {'message':'pesanan tidak di temukan'},402
    return pesanan

@app.delete("/keranjang/<int:id>")
def delete_keranjang_by_id(id):
    if keranjang.get_keranjang_by_id(id) is None:
        return {'message':'pesanan tidak di temukan'}
    keranjang.delete_keranjang_by_id(id)
    return {'message':'pesanan berhasil di hapus'},200




if __name__==('main'):
    app.run(debug=True, use_reloader=True, host="0.0.0.0")