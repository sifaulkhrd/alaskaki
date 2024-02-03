from flask import Flask, request
from models import produk
from models import kategori
import time
import os

def get_all_produk_controller():
    """
    Kontroler untuk mendapatkan semua produk dengan batasan halaman, limit, dan filter opsional.

    Returns:
    - list: List berisi dictionary informasi produk.
    """
    keyword = request.args.get('keyword')
    limit = int(request.args.get("limit", 5))
    page = int(request.args.get("page", 1))
    max_harga = request.args.get("max_harga")
    min_harga = request.args.get("min_harga")

    return produk.get_all_produk(limit=limit, page=page, keyword=keyword, max_harga=max_harga, min_harga=min_harga)


def get_produk_id(id):
    """
    Kontroler untuk mendapatkan satu produk bersama gambar berdasarkan ID.

    Args:
    - id (int): ID produk yang dicari.

    Returns:
    - dict or HTTP Response: Dictionary berisi informasi produk (id, nama, stok, harga, kategori_id, dan image) jika ditemukan,
      atau respons dengan pesan kesalahan jika tidak ditemukan.
    """
    item = produk.get_produk_by_id(id)
    if item is None:
        return {'message': 'Produk tidak ditemukan'}, 402

    images = produk.get_all_images(id)
    item["image"] = images

    return item


def buat_produk_baru():
    """
    Kontroler untuk menambahkan produk baru dengan gambar.

    Returns:
    - dict: Dictionary berisi pesan sukses atau pesan kesalahan.
    """
    nama = request.form.get("nama")
    stok = request.form.get("stok")
    harga = request.form.get("harga")
    kategori_id = request.form.get("kategori_id")
    files = request.files.getlist('files')

    if not nama or not stok or not harga or not kategori_id or not files:
        return {'message': 'Semua inputan harus diisi'}
    
    if not stok.isdigit() or int(stok) <= 0:
        return {'message': 'Stok harus berupa angka dan lebih besar dari 0'}
    
    if not harga.isdigit() or int(harga) <= 0:
        return {'message': 'Harga harus berupa angka dan lebih besar dari 0'}
    
    if not kategori_id.isdigit() or int(kategori_id) <= 0:
        return {'message': 'Kategori_id harus berupa angka dan lebih besar dari 0'}

    if kategori.get_kategori_by_id(kategori_id) is None:
        return {'message': 'Kategori tidak ditemukan'}
    
    # untuk mengijinkan tipe file yg akan dimasukkan
    allowed_files = ["image/jpeg", "image/jpg"]
    for file in files:
        if file.content_type not in allowed_files:
            return {'message': 'Tipe gambar harus jpeg atau jpg'}

    # untuk menyimpan lokasi gambar
    locations = []
    for file in files:
        tempat = "static/uploads/" + str(time.time()) + "_" + file.filename
        file.save(tempat)
        locations.append(tempat)
    
    try:
        id_terakhir = produk.create_new_produk(nama, stok, harga, kategori_id)

        for lokasi in locations:
            produk.upload_images(lokasi, id_terakhir)
    except Exception as e:
        for file in locations:
            if os.path.exists(tempat):
                os.remove(tempat)
        raise e
    
    return {'message': 'Produk berhasil dimasukkan'}


def edit_produk(id):
    """
    Kontroler untuk mengedit data produk berdasarkan ID.

    Args:
    - id (int): ID produk yang akan diubah.

    Returns:
    - dict: Dictionary berisi pesan sukses atau pesan kesalahan.
    """
    if produk.get_produk_by_id(id) is None:
        return {'message': 'Produk tidak ditemukan'}, 404
    
    nama = request.form.get("nama")
    stok = request.form.get("stok")
    harga = request.form.get("harga")
    kategori_id = request.form.get("kategori_id")

    if not nama or not stok or not harga or not kategori_id:
        return {'message': 'Semua inputan harus diisi'}
    
    if not stok.isdigit() or int(stok) <= 0:
        return {'message': 'Stok harus berupa angka dan lebih besar dari 0'}
    
    if not harga.isdigit() or int(harga) <= 0:
        return {'message': 'Harga harus berupa angka dan lebih besar dari 0'}
    
    if not kategori_id.isdigit() or int(kategori_id) <= 0:
        return {'message': 'Kategori_id harus berupa angka dan lebih besar dari 0'}

    if kategori.get_kategori_by_id(kategori_id) is None:
        return {'message': 'Kategori tidak ditemukan'}

    produk.update_produk_by_id(
        id,
        nama,
        stok,
        harga,
        kategori_id,
    )
    return {'message': 'Produk berhasil di edit'}


def hapus_produk(id):
    """
    Kontroler untuk menghapus produk berdasarkan ID.

    Args:
    - id (int): ID produk yang akan dihapus.

    Returns:
    - dict: Dictionary berisi pesan sukses atau pesan kesalahan.
    """
    if produk.get_produk_by_id(id) is None:
        return {'message': 'Produk tidak ditemukan'}
    
    images = produk.get_all_images(id)
    produk.delete_produk_by_id(id)

    for image in images:
        if os.path.exists(image['lokasi']):
            os.remove(image["lokasi"])
    
    return {'message': 'Produk berhasil dihapus'}, 200
