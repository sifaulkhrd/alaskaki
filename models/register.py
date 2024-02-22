from db import conn
from flask_bcrypt import Bcrypt

def validator_register_username(username):
    """
    Validasi username saat mendaftar.

    Args:
    - username (str): Nama pengguna yang akan divalidasi.

    Returns:
    - bool: True jika username sudah digunakan, False jika belum.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query.
    """
    cur = conn.cursor()
    try:
        cur.execute('SELECT username from users where username = %s', (username,))
        if cur.fetchone():
            return True
        return False
    except Exception as e:
        raise e 
    finally:
        cur.close()


def validator_register_password(password):
    """
    Validasi password saat mendaftar.

    Args:
    - password (str): Password yang akan divalidasi.

    Returns:
    - bool: True jika password sudah digunakan, False jika belum.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query.
    """
    cur = conn.cursor()
    try:
        cur.execute('SELECT password from users where password = %s', (password,))
        if cur.fetchone():
            return True
        return False
    except Exception as e:
        raise e 
    finally:
        cur.close()


def validator_register_fullname(fullname):
    """
    Validasi nama lengkap saat mendaftar.

    Args:
    - fullname (str): Nama lengkap yang akan divalidasi.

    Returns:
    - bool: True jika nama lengkap sudah digunakan, False jika belum.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query.
    """
    cur = conn.cursor()
    try:
        cur.execute('SELECT fullname from users where fullname = %s', (fullname,))
        if cur.fetchone():
            return True
        return False
    except Exception as e:
        raise e 
    finally:
        cur.close()


def register_data(username, password, fullname):
    """
    Registrasi data pengguna baru.

    Args:
    - username (str): Nama pengguna untuk registrasi.
    - password (str): Kata sandi untuk registrasi.
    - fullname (str): Nama lengkap untuk registrasi.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query atau saat rollback.
    """
    cur = conn.cursor()
    try:
        # bcrypt = Bcrypt()
        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute('INSERT INTO users (username, password, fullname) VALUES (%s, %s, %s)', (username, password, fullname))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

