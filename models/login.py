from db import conn

def get_username(username, password):
    """
    Mendapatkan data pengguna berdasarkan username dan password.

    Args:
    - username (str): Nama pengguna.
    - password (str): Kata sandi.

    Returns:
    - list: List berisi dictionary data pengguna (id dan fullname) jika ditemukan, None jika tidak ditemukan.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query.
    """
    cur = conn.cursor()
    try:
        cur.execute('SELECT id, username, password, fullname from users where username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        if user:
            return [{"id": user[0]}, {"fullname": user[3]}]
    except Exception as e:
        raise e
    finally:
        cur.close()



