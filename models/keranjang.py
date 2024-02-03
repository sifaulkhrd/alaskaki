from db import conn

def create_new_keranjang(user_id, produk_id, kuantitas):
    """
    Menambahkan produk ke dalam keranjang pengguna.

    Args:
    - user_id (int): ID pengguna.
    - produk_id (int): ID produk.
    - kuantitas (int): Kuantitas produk yang akan ditambahkan ke keranjang.

    Returns:
    None

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query atau saat rollback.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk menambahkan data ke tabel 'keranjang'
        cur.execute('INSERT INTO keranjang (user_id, produk_id, kuantitas) VALUES (%s, %s, %s)',
                    (user_id, produk_id, kuantitas,))
        
        # Melakukan commit untuk menyimpan perubahan ke database
        conn.commit()

    except Exception as e:
        # Jika terjadi kesalahan, melakukan rollback untuk membatalkan perubahan
        conn.rollback()
        
        # Mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e

    finally:
        # Menutup cursor untuk membersihkan sumber daya
        cur.close()



def get_all_keranjang(user_id):
    """
    Mendapatkan semua data keranjang pengguna berdasarkan ID pengguna.

    Args:
    - user_id (int): ID pengguna.

    Returns:
    - list: List berisi data keranjang dalam bentuk dictionary.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query atau saat rollback.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk mendapatkan semua data keranjang dari tabel
        cur.execute('SELECT id, user_id, produk_id, kuantitas FROM keranjang WHERE user_id = %s  ORDER BY id', (user_id,))
        keranjang = cur.fetchall()

        # Mengkonversi tuple ke dalam bentuk dictionary
        new_keranjang = []
        for item in keranjang:
            new_item = {
                "id": item[0],
                "user_id": item[1],
                "produk_id": item[2],
                "kuantitas": item[3],
            }
            new_keranjang.append(new_item)
        
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

    return new_keranjang


def get_keranjang_by_id(id):
    """
    Mengambil data pesanan berdasarkan ID.

    Parameters:
    - id (int): ID pesanan yang akan dicari.

    Returns:
    - dict or None: Jika pesanan ditemukan, kembalikan data pesanan dalam bentuk dictionary.
                    Jika tidak ditemukan, kembalikan None.

    Raises:
    - Exception: Menangkap dan mengelemparkan exception jika terjadi kesalahan.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk mendapatkan pesanan berdasarkan ID
        cur.execute('SELECT id, user_id, produk_id, kuantitas FROM keranjang WHERE id = %s', (id,))
        keranjang = cur.fetchone()

    except Exception as e:
        # Jika terjadi kesalahan, mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e

    finally:
        # Menutup cursor untuk membersihkan sumber daya
        cur.close()

    # Mengembalikan data pesanan jika ditemukan, jika tidak, kembalikan None
    if keranjang is None:
        return None
    
    # untuk meng convert tuple ke dictionary
    return {
        "id": keranjang[0],
        "user_id": keranjang[1],
        "produk_id": keranjang[2],
        "kuantitas": keranjang[3],
    }

def get_keranjang_by_id_dan_user_id(keranjang_id: int, user_id: int):
    """
    Mendapatkan data keranjang berdasarkan ID keranjang dan ID pengguna.

    Args:
    - keranjang_id (int): ID keranjang.
    - user_id (int): ID pengguna.

    Returns:
    - dict or None: Dictionary berisi data keranjang atau None jika tidak ditemukan.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query atau saat rollback.
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, user_id, produk_id, kuantitas FROM keranjang WHERE id = %s AND user_id = %s", (keranjang_id, user_id))
        data = cur.fetchone()
        if data is not None:
            new_data = {
                "id": data[0],
                "user_id": data[1],
                "produk_id": data[2],
                "kuantitas": data[3],
            }
            return new_data
        else:
            return None
    
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_keranjang_by_id(id, user_id):
    """
    Menghapus pesanan dari keranjang berdasarkan ID pesanan dan ID pengguna.

    Args:
    - id (int): ID pesanan.
    - user_id (int): ID pengguna.

    Returns:
    None

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query atau saat rollback.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk menghapus pesanan berdasarkan ID
        cur.execute("DELETE FROM keranjang WHERE id = %s AND user_id = %s", (id, user_id))

        # Melakukan commit untuk menyimpan perubahan ke database
        conn.commit()

    except Exception as e:
        # Jika terjadi kesalahan, mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e

    finally:
        # Menutup cursor untuk membersihkan sumber daya
        cur.close()
