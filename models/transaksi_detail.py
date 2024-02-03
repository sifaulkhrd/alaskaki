from db import conn



def get_transaksi_detail_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT id, produk_id, harga, kuantitas, transaksi_id,total FROM transaksi_detail WHERE transaksi_id = %s', (id,))
    transaksi_detail = cur.fetchone()

    conn.commit()
    cur.close()

    if transaksi_detail is None:
        return None
    
    return {
        "id": transaksi_detail[0],
        "produk_id": transaksi_detail[1],
        "harga": transaksi_detail[2],
        "kuantitas": transaksi_detail[3],
        "transaksi_id": transaksi_detail[4],
        "total":transaksi_detail[5],
    }


def create_new_transaksi_detail(produk_id, harga, kuantitas, transaksi_id, total):
    """
    Menambahkan data transaksi detail baru ke database.

    Parameters:
    - produk_id (int): ID produk yang terkait dengan transaksi detail.
    - harga (int): Harga per unit produk.
    - kuantitas (int): Jumlah produk yang dibeli.
    - transaksi_id (int): ID transaksi yang terkait dengan transaksi detail.

    Raises:
    - Exception: Menangkap dan mengelemparkan exception jika terjadi kesalahan.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk menambahkan data transaksi detail ke tabel 'transaksi_detail'
        cur.execute('INSERT INTO transaksi_detail (produk_id, harga, kuantitas, transaksi_id, total) VALUES (%s, %s, %s, %s, %s)',
                    (produk_id, harga, kuantitas, transaksi_id, total))

    except Exception as e: 
        # Mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e




def get_all_transaksi_detail():
    """
    Mengambil semua data transaksi detail dari database.

    Returns:
    - list: Daftar transaksi detail dalam bentuk dictionary, masing-masing merepresentasikan satu transaksi detail.

    Raises:
    - Exception: Menangkap dan mengelemparkan exception jika terjadi kesalahan.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk mendapatkan semua data transaksi detail dari tabel
        cur.execute('SELECT id, produk_id, harga, kuantitas, transaksi_id, total FROM transaksi_detail ORDER BY id')
        transaksi_detail = cur.fetchall()

        # Mengkonversi tuple ke dalam bentuk dictionary
        new_transaksi_detail = []
        for item in transaksi_detail:
            new_item = {
                "id": item[0],
                "produk_id": item[1],
                "harga": item[2],
                "kuantitas": item[3],
                "transaksi_id": item[4],
                "total": item[5],
            }
            new_transaksi_detail.append(new_item)
        
        # Melakukan commit untuk menyimpan perubahan ke database (tidak perlu di sini)
        # conn.commit()

    except Exception as e:
        # Jika terjadi kesalahan, melakukan rollback untuk membatalkan perubahan
        conn.rollback()

        # Mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e

    finally:
        # Menutup cursor untuk membersihkan sumber daya
        cur.close()

    return new_transaksi_detail



def delete_transaksi_detail_by_id(id):
    """
    Menghapus data transaksi detail berdasarkan ID.

    Parameters:
    - id (int): ID transaksi detail yang akan dihapus.

    Raises:
    - Exception: Menangkap dan mengelemparkan exception jika terjadi kesalahan.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk menghapus transaksi detail berdasarkan ID
        cur.execute("DELETE FROM transaksi_detail WHERE id = %s", (id,))

        # Melakukan commit untuk menyimpan perubahan ke database
        conn.commit()

    except Exception as e:
        # Jika terjadi kesalahan, mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e

    finally:
        # Menutup cursor untuk membersihkan sumber daya
        cur.close()

# Fungsi untuk menghapus transaksi_detail berdasarkan transaksi_id
def delete_transaksi_detail_by_transaksi_id(transaksi_id):
    cur = conn.cursor()
    try:
        # Menghapus data transaksi_detail berdasarkan transaksi_id
        cur.execute("DELETE FROM transaksi_detail WHERE transaksi_id = %s", (transaksi_id,))
    except Exception as e:
        # Handle kesalahan sesuai kebutuhan Anda
        raise e
    
