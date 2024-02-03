from db import conn

def get_transaksi_by_id(user_id, id):
    """
    Mengambil data transaksi berdasarkan ID.

    Parameters:
    - id (int): ID transaksi yang akan dicari.

    Returns:
    - dict or None: Jika transaksi ditemukan, kembalikan data transaksi dalam bentuk dictionary.
                    Jika tidak ditemukan, kembalikan None.

    Raises:
    - Exception: Menangkap dan mengelemparkan exception jika terjadi kesalahan.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk mendapatkan transaksi berdasarkan ID
        cur.execute('SELECT id, user_id, fullname, alamat, email, tanggal FROM transaksi WHERE user_id = %s AND id = %s', (user_id, id))
        transaksi = cur.fetchone()
        if transaksi:
            return {
            "id": transaksi[0],
            "user_id": transaksi[1],
            "fullname": transaksi[2],
            "alamat": transaksi[3],
            "email": transaksi[4],
            "tanggal": transaksi[5],
            }
        else:
            return None

        # Melakukan commit untuk menyimpan perubahan ke database (tidak perlu di sini)
        # conn.commit()
        return transaksi
    except Exception as e:
        # Jika terjadi kesalahan, mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e

    finally:
        # Menutup cursor untuk membersihkan sumber daya
        cur.close()

    # Mengembalikan data transaksi jika ditemukan, jika tidak, kembalikan None
    if transaksi is None:
        return None
    
    return {
        "id": transaksi[0],
        "user_id": transaksi[1],
        "fullname": transaksi[2],
        "alamat": transaksi[3],
        "email": transaksi[4],
        "tanggal": transaksi[5],
    }


def create_new_transaksi(user_id, fullname, alamat, email):
    """
    Menambahkan data transaksi baru ke database.

    Parameters:
    - user_id (int): ID pengguna yang melakukan transaksi.
    - fullname (str): Nama lengkap pengguna.
    - alamat (str): Alamat pengguna.
    - email (str): Alamat email pengguna.

    Raises:
    - Exception: Menangkap dan mengelemparkan exception jika terjadi kesalahan.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk menambahkan data transaksi ke tabel 'transaksi'
        cur.execute('INSERT INTO transaksi (user_id, fullname, alamat, email) VALUES (%s, %s, %s, %s) RETURNING id',
                    (user_id, fullname, alamat, email,))
       
        data = cur.fetchone()[0]
        return data


    except Exception as e:
        # Jika terjadi kesalahan, melakukan rollback untuk membatalkan perubahan
        
        # Mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e
    finally:
        cur.close()

def get_all_transaksi():
    """
    Mengambil semua data transaksi dari database.

    Returns:
    - list: Daftar transaksi dalam bentuk dictionary, masing-masing merepresentasikan satu transaksi.

    Raises:
    - Exception: Menangkap dan mengelemparkan exception jika terjadi kesalahan.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk mendapatkan semua data transaksi dari tabel
        cur.execute('SELECT id, user_id, fullname, alamat, email, tanggal FROM transaksi ORDER BY id')
        transaksi = cur.fetchall()

        # Mengkonversi tuple ke dalam bentuk dictionary
        new_transaksi = []
        for item in transaksi:
            new_item = {
                "id": item[0],
                "user_id": item[1],
                "fullname": item[2],
                "alamat": item[3],
                "email": item[4],
                "tanggal": item[5],
            }
            new_transaksi.append(new_item)
        
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

    return new_transaksi


def delete_transaksi_by_id(user_id, id):
    """
    Menghapus data transaksi berdasarkan ID.

    Parameters:
    - id (int): ID transaksi yang akan dihapus.

    Raises:
    - Exception: Menangkap dan mengelemparkan exception jika terjadi kesalahan.
    """
    # Membuat objek cursor untuk berinteraksi dengan database
    cur = conn.cursor()

    try:
        # Mengeksekusi perintah SQL untuk menghapus transaksi berdasarkan ID
        cur.execute("DELETE FROM transaksi WHERE user_id = %s AND id = %s", (user_id, id))


    except Exception as e:
        # Jika terjadi kesalahan, mengelemparkan exception agar dapat ditangkap oleh pemanggil fungsi
        raise e

    
