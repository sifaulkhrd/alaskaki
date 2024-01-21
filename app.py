from flask import Flask, request
from models.login import get_username
from models.register import validator_register_username, validator_register_password,validator_register_fullname, register_data
from models import produk
from models import keranjang
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

    if not username or not password:
        return {'message': 'semua inputan harus diisi'}
    
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


# ========================================CRUD=KATEGORI====================================================
# melihat semua kategori
@app.get("/kategori")
def get_all_kategori():
    return kategori.get_all_kategori()

# melihat kategori menggunkan id
@app.get("/kategori/<int:id>")
def get_all_kategori_by_id(id):
    item = kategori.get_kategori_by_id(id)
    if item is None:
        return {'message':'kategori tidak di temukan'},402
    # nama = produk.get_all_produk  (id)
    # item["produk"]=nama
    return item

# melihat produk yg ada di kategori
@app.get('/kategori/<int:kategori_id>/produk')
def get_all_produk_by_kategori(kategori_id):
    if produk.get_produk_by_kategori(kategori_id) is None:
        return {'message':'kategori tidak di temukan'},
    list_produk = produk.get_produk_by_kategori(kategori_id)
    list_kategori = kategori.get_kategori_by_id(kategori_id)
    if list_produk is None:
        list_kategori["produk"] = "belum ada produk di kategori ini"
    else:
        list_kategori["produk"] = list_produk
    print("ihfaahdfad",list_kategori)
    return list_kategori
# ========================================CRUD=PRODUK======================================================

# melihat semua produk tampa limit
@app.get("/produk")
def get_all_produk():
    return produk.get_all_produk()

# ini untuk melihat semua produck menggunakan limit
@app.get('/produk_limit')
def get_all_produk_limit():
    keyword = request.args.get('keyword')
    limit = int(request.args.get("limit", 5))
    page = int(request.args.get("page", 1))
    max_harga = request.args.get("max_harga")
    min_harga = request.args.get("min_harga")

    return produk.get_all_produk_limit(limit=limit, page=page, keyword=keyword, max_harga=max_harga, min_harga=min_harga)

# ini untuk melihat produk menggunakan id
@app.get("/produk/<int:id>")
def get_produk_by_id(id):
    item = produk.get_produk_by_id(id)
    if item is None:
        return {'message':'produk tidak di temukan'},402
    images = produk.get_all_images(id)
    item["image"]=images
    return item

# ini untuk menambahkan produk 
@app.post("/produk")
def create_new_produk():
    nama = request.form.get("nama")
    stok = request.form.get("stok")
    harga = request.form.get("harga")
    kategori_id = request.form.get("kategori_id")
    files = request.files.getlist('files')

    if not nama or not stok or not harga or not kategori_id or not files:
        return {'message': 'semua inputan harus diisi'}

    if kategori.get_kategori_by_id(kategori_id) is None:
        return {'message':'kategori tidak di temukan'}
    
    # untuk mengijinkan tipe file yg akan di masukan
    allowed_files = ["image/jpeg", "image/jpg"]
    for file in files:
        if file.content_type not in allowed_files:
            return {'message':'tipe gambar harus jpeg atau jpg'}


    # untuk menyimpan lokasi gambar 
    locations = []
    for file in files:
        tempat = "static/uploads/" + str(time.time()) + "_" + file.filename
        file.save(tempat)
        locations.append(tempat)
    try:
        id_terakhir = produk.create_new_produk(nama,stok,harga,kategori_id)
        print(id_terakhir)

        for lokasi in locations:
            produk.upload_images(lokasi, id_terakhir)
    except Exception as e:
        for file in locations:
            if os.path.exists(tempat):
                os.remove(tempat)
        raise e
    return {'message':'produk berhasil di masukan'}

# ini untuk mengedit data produk
@app.put("/produk/<int:id>")
def update_produk_by_id(id):
    if produk.get_produk_by_id(id) is None:
        return {'message':'produk tidak di temukan'},404
    
    nama = request.form.get("nama")
    stok = request.form.get("stok")
    harga = request.form.get("harga")
    kategori_id = request.form.get("kategori_id")

    if not nama or not stok or not harga or not kategori_id:
        return {'message': 'semua inputan harus diisi'}
    
    if not stok.isdigit() or int(stok) <= 0:
        return {'message':'stok harus berupa angka dan lebih besar dari 0'}
    
    if not harga.isdigit() or int(harga) <= 0:
        return {'message':'harga harus berupa angka dan lebih besar dari 0'}
    
    if not kategori_id.isdigit() or int(kategori_id) <= 0:
        return {'message':'kategori_id harus berupa angka dan lebih besar dari 0'}

    if kategori.get_kategori_by_id(kategori_id) is None:
        return {'message':'kategori tidak di temukan'}

    produk.update_produk_by_id(
        id,
        nama,
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
    images = produk.get_all_images(id)
    produk.delete_produk_by_id(id)
    for image in images:
        if os.path.exists(image['lokasi']):
            os.remove(image["lokasi"])
    return {'message':'produk berhasil di hapus'},200

# ========================================CRUD=KERANJANG======================================================

# ini untuk menambah pesanan
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

# ini untuk melihat semua pesanan
@app.get('/keranjang')
def get_all_keranjang():
    return keranjang.get_all_keranjang()

# ini untuk melihat pesanan menggunakan id
@app.get("/keranjang/<int:id>")
def get_keranjang_by_id(id):
    pesanan = keranjang.get_keranjang_by_id(id)
    if pesanan is None:
        return {'message':'pesanan tidak di temukan'},402
    return pesanan

# ini untuk menghapus pesanan
@app.delete("/keranjang/<int:id>")
def delete_keranjang_by_id(id):
    if keranjang.get_keranjang_by_id(id) is None:
        return {'message':'pesanan tidak di temukan'}
    keranjang.delete_keranjang_by_id(id)
    return {'message':'pesanan berhasil di hapus'},200

# ========================================CRUD=TRANSAKSI======================================================
# ini untuk menambah kan data transaksi
@app.post("/transaksi")
def create_new_transaksi():
    user_id = request.form.get("user_id")
    fullname = request.form.get("fullname")
    alamat = request.form.get("alamat")
    email = request.form.get("email")


    if not user_id or not fullname or not alamat or not email:
        return {'message': 'semua inputan harus diisi'}
    if user.get_users_by_id(user_id) is None:
        return {'message':'user tidak di temukan'}

     
    transaksi.create_new_transaksi(user_id,fullname,alamat,email)
    return {'message':'data berhasil di masukkan di transaksi'}

@app.get('/transaksi')
def get_all_transaksi():
    return transaksi.get_all_transaksi()

@app.delete("/transaksi/<int:id>")
def delete_transaksi_by_id(id):
    if transaksi.get_transaksi_by_id(id) is None:
        return {'message':'data transaksi tidak di temukan'}
    transaksi.delete_transaksi_by_id(id)
    return {'message':'data transaksi berhasil di hapus'},200

# ========================================CRUD=TRANSAKSI=DETAIL=============================================

@app.post("/transaksi_detail")
def create_new_transaksi_detail():
    produk_id = request.form.get("produk_id")
    harga = request.form.get("harga")
    kuantitas = request.form.get("kuantitas")
    transaksi_id = request.form.get("transaksi_id")


    if not produk_id or not harga or not kuantitas or not transaksi_id:
        return {'message': 'semua inputan harus diisi'}
    if produk.get_produk_by_id(produk_id) is None:
        return {'message':'produk tidak di temukan'}
    if transaksi.get_transaksi_by_id(transaksi_id) is None:
        return {'message':'transaksi tidak di temukan'}
    if not kuantitas.isdigit() or int(kuantitas) <= 0:
        return {'message':'kuantitas harus berupa angka dan lebih besar dari 0'}
    if not harga.isdigit() or int(harga) <= 0:
        return {'message':'harga harus berupa angka dan lebih besar dari 0'}

     
    transaksi_detail.create_new_transaksi_detail(produk_id,harga,kuantitas,transaksi_id)
    return {'message':'data berhasil di masukkan di transaksi detail'}

@app.get('/transaksi_detail')
def get_all_transaksi_detail():
    return transaksi_detail.get_all_transaksi_detail()

@app.delete("/transaksi_detail/<int:id>")
def delete_transaksi_detail_by_id(id):
    if transaksi_detail.get_transaksi_detail_by_id(id) is None:
        return {'message':'data transaksi detail tidak di temukan'}
    transaksi_detail.delete_transaksi_detail_by_id(id)
    return {'message':'data transaksi detail berhasil di hapus'},200

if __name__==('main'):
    app.run(debug=True, use_reloader=True, host="0.0.0.0")