from flask import Flask, request
from models import user
from models import produk
from models import keranjang

from flask_jwt_extended import (
    get_jwt_identity,
)

def masukan_pesanan():
    """
    Kontroler untuk menambahkan produk ke dalam keranjang pengguna.

    Returns:
    - dict: Dictionary berisi pesan sukses atau pesan kesalahan.
    """
    user = get_jwt_identity()
    user_id = user["id"]
    produk_id = request.form.get("produk_id")
    kuantitas = request.form.get("kuantitas")
    
    if not produk_id or not kuantitas:
        return {'message': 'Semua inputan harus diisi'}
    
    if not produk_id.isdigit() or int(produk_id) <= 0:
        return {'message': 'Produk_id harus berupa angka dan lebih besar dari 0'}
    
    data_produk = produk.get_produk_by_id(produk_id)
    if data_produk is None:
        return {"message": "Produk tidak ditemukan"}, 404
    
    if int(kuantitas) > int(data_produk['stok']):
        return {"message": f"Stok dari produk ID {produk_id} hanya tersisa {data_produk['stok']} barang"}
    
    if not kuantitas.isdigit() or int(kuantitas) <= 0:
        return {'message': 'Kuantitas harus berupa angka dan lebih besar dari 0'}
    
    keranjang.create_new_keranjang(user_id, produk_id, kuantitas)
    
    return {'message': 'Produk berhasil dimasukkan di keranjang'}


def get_all_keranjang_by_user():
    """
    Kontroler untuk mendapatkan semua data keranjang berdasarkan ID pengguna.

    Returns:
    - dict or list: Dictionary berisi pesan sukses atau list data keranjang.

    Raises:
    - Exception: Jika terjadi kesalahan saat memanggil fungsi get_all_keranjang.
    """
    user = get_jwt_identity()
    user_id = user["id"]

    pesanan = keranjang.get_all_keranjang(user_id)

    if pesanan is None:
        return {'message': 'Keranjang anda masih kosong'}

    return pesanan



def lihat_pesanan_by_id(id):
    """
    Kontroler untuk melihat detail pesanan berdasarkan ID pesanan.

    Args:
    - id (int): ID pesanan.

    Returns:
    - dict or HTTP Response: Dictionary berisi data pesanan atau pesan kesalahan jika tidak ditemukan.
    """
    user = get_jwt_identity()
    user_id = user["id"]

    pesanan = keranjang.get_keranjang_by_id_dan_user_id(id, user_id)

    # Memeriksa apakah pesanan ditemukan atau tidak
    if pesanan is None:
        return {'message': 'Pesanan tidak ditemukan'}, 402
    
    nama = produk.get_produk_by_id(pesanan["produk_id"])
    pesanan["produk_id"] = nama

    # Mengembalikan data pesanan jika ditemukan
    return pesanan




def hapus_pesanan(id, user_id):
    """
    Menghapus pesanan berdasarkan ID pesanan dan ID pengguna.

    Args:
    - id (int): ID pesanan.
    - user_id (int): ID pengguna.

    Returns:
    - dict: Dictionary berisi pesan sukses atau pesan kesalahan jika pesanan tidak ditemukan.
    """
    user = get_jwt_identity()
    user_id = user["id"]

    # Memeriksa apakah pesanan dengan ID yang diberikan ditemukan atau tidak
    if not keranjang.get_keranjang_by_id_dan_user_id(id, user_id):
        return {'message': 'Pesanan tidak ditemukan'}

    # Memanggil fungsi dari modul 'keranjang' untuk menghapus pesanan berdasarkan ID
    keranjang.delete_keranjang_by_id(id, user_id)

    # Memberikan respons bahwa pesanan berhasil dihapus
    return {'message': 'Pesanan berhasil dihapus'}, 200

