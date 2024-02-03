from flask import Flask, request
from models import user
from models import produk
from models import transaksi
from models import keranjang
from models import transaksi_detail
from errors import DatabaseError

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from db import conn

def masukan_data_transaksi():
    """
    controller untuk membuat data transaksi baru.

    Returns:
    - dict: Dictionary berisi pesan sukses atau pesan kesalahan jika transaksi tidak berhasil.
    - HTTP Response: Respons dari fungsi masukan_data_transaksi.
    """
    # Mengambil data input dari formulir atau payload
    user = get_jwt_identity()
    user_id = user['id']
    fullname = request.form.get("fullname")
    alamat = request.form.get("alamat")
    email = request.form.get("email")
    produk_id = request.form.get("produk_id")
    kuantitas = request.form.get("kuantitas")
   
    # Memeriksa apakah semua input telah diisi
    if not user_id or not fullname or not alamat or not email or not produk_id or not kuantitas:
        return {'message': 'Semua inputan harus diisi'}, 404

    if not produk_id.isdigit() or int(produk_id) <= 0:
        return {'message':'produk_id harus berupa angka dan lebih besar dari 0'}
    
    # Memeriksa apakah produk dengan ID yang diberikan ditemukan atau tidak
    data_produk = produk.get_produk_by_id(produk_id)
    if data_produk is None:
        return {"message": "produk tidak ditemukan"}, 404
    
    cur = conn.cursor()
    try:
        # Menghitung jumlah harga berdasarkan kuantitas dan harga produk
        total = int(kuantitas) * int(data_produk['harga'])

        # Memanggil fungsi dari modul 'transaksi' untuk membuat data transaksi baru
        transaksi_id = transaksi.create_new_transaksi(user_id, fullname, alamat, email)

        # Menambahkan entri transaksi detail dengan jumlah harga
        transaksi_detail.create_new_transaksi_detail(produk_id, data_produk['harga'], kuantitas, transaksi_id, total)

        # Mengurangi stok produk setelah transaksi berhasil ditambahkan
        produk.update_produk_stok(produk_id, kuantitas)

        conn.commit()

        return {"message": "Transaksi berhasil ditambahkan"}, 200
    except Exception as e:
        conn.rollback()
        return str(e), 404
    finally:
        cur.close()



def transaksi_dari_keranjang():
    """
    Melakukan transaksi dari keranjang belanja.

    Parameters:
    - user_id: ID pengguna yang melakukan transaksi
    - fullname: Nama lengkap penerima transaksi
    - alamat: Alamat pengiriman transaksi
    - email: Alamat email penerima transaksi
    - keranjang_id: ID keranjang yang akan dijadikan transaksi
    - kuantitas: Jumlah barang yang akan dibeli

    Returns:
    - Jika transaksi berhasil: {'message': 'transaksi berhasil ditambahkan'}
    - Jika terdapat kesalahan: {'message': 'pesan kesalahan', 'data': []}
    """

    cur = conn.cursor()
    try:
        # Mendapatkan identitas pengguna dari token JWT
        user = get_jwt_identity()
        user_id = user['id']
        fullname = request.form.get("fullname")
        alamat = request.form.get("alamat")
        email = request.form.get("email")
        keranjang_id = request.form.get("keranjang_id")
        kuantitas = request.form.get("kuantitas")

        # Memeriksa apakah semua input telah diisi
        if not user_id or not fullname or not alamat or not email or not keranjang_id or not kuantitas:
            return {'message': 'Semua inputan harus diisi'}, 404

        # Membuat transaksi baru dan mendapatkan ID transaksi
        transaksi_id = transaksi.create_new_transaksi(user_id, fullname, alamat, email)

        # Mendapatkan informasi pesanan dari keranjang
        pesanan = keranjang.get_keranjang_by_id_dan_user_id(keranjang_id, user_id)
        if pesanan is None:
            raise DatabaseError("keranjang masih kosong")

        # Mendapatkan informasi produk dari pesanan
        barang = produk.get_produk_by_id(pesanan["produk_id"])
        kuantitas_pesanan = int(pesanan["kuantitas"])

        # Menghitung total harga transaksi
        total = int(kuantitas) * int(barang["harga"])

        # Memeriksa stok produk sebelum menambahkan transaksi
        if int(barang["stok"]) < int(kuantitas):
            raise Exception({"message": f"stok dari produk id {barang['produk_id']} hanya tersisa {barang['stok']} barang"})

        # Membuat detail transaksi baru
        transaksi_detail.create_new_transaksi_detail(barang["id"], barang["harga"], kuantitas, transaksi_id, total)

        # Mengurangi stok produk setelah transaksi berhasil ditambahkan
        produk.update_produk_stok(barang["id"], kuantitas_pesanan)

        # Menghapus barang dari keranjang setelah transaksi berhasil
        keranjang.delete_keranjang_by_id(keranjang_id, user_id)

        # Commit transaksi ke database
        conn.commit()

        return {"message": "transaksi berhasil ditambahkan"}
    except DatabaseError as e:
        # Rollback jika terjadi kesalahan database
        conn.rollback()
        return {"message": str(e), "data": []}
    except Exception as e:
        # Rollback dan lempar kembali kesalahan jika terjadi kesalahan lainnya
        conn.rollback()
        raise e
    finally:
        # Menutup kursor setelah transaksi selesai
        cur.close()


def lihat_transaksi_detail(id):
    """
    Melihat detail transaksi berdasarkan ID.

    Parameters:
    - id: ID transaksi yang akan dilihat detailnya.

    Returns:
    - Jika transaksi ditemukan: Informasi lengkap transaksi beserta detailnya.
    - Jika transaksi tidak ditemukan: {'message': 'transaksi tidak ditemukan'}
    """
    # Mendapatkan identitas pengguna dari token JWT
    user = get_jwt_identity()
    user_id = user['id']

    # Mendapatkan informasi transaksi berdasarkan ID
    item = transaksi.get_transaksi_by_id(user_id, id)
    
    # Jika transaksi tidak ditemukan, kirim pesan kesalahan
    if item is None:
        return {'message': 'transaksi tidak ditemukan',}
    
    # Mendapatkan detail transaksi berdasarkan ID
    details = transaksi_detail.get_transaksi_detail_by_id(id)

    # Menambahkan informasi detail ke dalam data transaksi
    item['details'] = details

    return item


def hapus_data_transaksi(transaksi_id):
    """
    Menghapus data transaksi berdasarkan ID.

    Parameters:
    - transaksi_id: ID transaksi yang akan dihapus.

    Returns:
    - Jika transaksi berhasil dihapus: {'message': 'Transaksi berhasil dihapus'}
    - Jika transaksi tidak ditemukan: {'message': 'Transaksi tidak ditemukan'}
    - Jika terjadi kesalahan lainnya: {'message': 'pesan kesalahan'}
    """
    cur = conn.cursor()
    try:
        # Mendapatkan identitas pengguna dari token JWT
        user = get_jwt_identity()
        user_id = user['id']

        # Memeriksa apakah transaksi dengan ID yang diberikan ditemukan
        if transaksi.get_transaksi_by_id(user_id, transaksi_id) is None:
            raise Exception("Transaksi tidak ditemukan")

        # Menghapus data transaksi berdasarkan ID
        transaksi.delete_transaksi_by_id(user_id, transaksi_id)

        # Menghapus data transaksi_detail berdasarkan transaksi_id
        transaksi_detail.delete_transaksi_detail_by_transaksi_id(transaksi_id)

        # Commit perubahan ke database
        conn.commit()

        return {"message": f"Transaksi dengan ID {transaksi_id} berhasil dihapus"}

    except Exception as e:
        # Rollback jika terjadi kesalahan
        conn.rollback()
        return {"message": str(e)}
    finally:
        # Menutup kursor setelah operasi selesai
        cur.close()
