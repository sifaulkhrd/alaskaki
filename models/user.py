from db import conn
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)


def get_users_by_id(id):
    """
    Fungsi ini mengambil data pengguna berdasarkan ID pengguna dari database.

    Parameters:
        id (int): ID pengguna yang akan dicari.

    Returns:
        dict or None: Data pengguna dalam bentuk dictionary jika ditemukan, atau None jika tidak ditemukan.
    """
    cur = conn.cursor()
    cur.execute('SELECT id, username, password, fullname FROM users WHERE id = %s', (id,))
    users = cur.fetchone()

    conn.commit()
    cur.close()

    if users is None:
        return None
    
    return {
        "id": users[0],
        "username": users[1],
        "password": users[2],
        "fullname": users[3],
    }


def edit_data_user(user_id, username, password, fullname):
    """
    Fungsi ini mengedit data pengguna dalam database berdasarkan ID pengguna.

    Parameters:
        user_id (int): ID pengguna yang akan diubah datanya.
        username (str): Username baru untuk pengguna.
        password (str): Password baru untuk pengguna.
        fullname (str): Nama lengkap baru untuk pengguna.

    Returns:
        None
    """
    cur = conn.cursor()
    try:
        # Mendapatkan identitas pengguna dari token JWT
        user = get_jwt_identity()
        user_id = user['id']
        
        # Melakukan query untuk memperbarui data pengguna
        cur.execute("UPDATE users SET username = %s, password = %s, fullname = %s WHERE id = %s;", (username, password, fullname, user_id))
        conn.commit()
    except Exception as e:
        # Jika terjadi kesalahan, rollback transaksi
        conn.rollback()
        raise e
    finally:
        # Menutup cursor setelah selesai
        cur.close()
