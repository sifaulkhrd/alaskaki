from db import conn

def get_transaksi_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT id, user_id, fullname, alamat, email, tanggal, status FROM transaksi WHERE id = %s', (id,))
    transaksi = cur.fetchone()

    conn.commit()
    cur.close()

    if transaksi is None:
        return None
    
    return {
        "id": transaksi[0],
        "user_id": transaksi[1],
        "fullname": transaksi[2],
        "alamat": transaksi[3],
        "email": transaksi[4],
        "tanggal": transaksi[5],
        "status": transaksi[6],
    }

def create_new_transaksi(user_id,fullname,alamat,email):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO transaksi (user_id,fullname,alamat,email) VALUES (%s,%s,%s,%s)', (user_id,fullname,alamat,email,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def get_all_transaksi():
    cur = conn.cursor()

    try:
        cur.execute('SELECT id, user_id, fullname, alamat, email, tanggal, status FROM transaksi ORDER BY id')
        transaksi = cur.fetchall()

        # meng convert tuple ke dictionary
        new_transaksi = []
        for item in transaksi:
            new_item = {
                "id": item[0],
                "user_id": item[1],
                "fullname": item[2],
                "alamat": item[3],
                "email": item[4],
                "tanggal": item[5],
                "status": item[6],
            }
            new_transaksi.append(new_item)
        conn.commit
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
    return new_transaksi

def delete_transaksi_by_id(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM transaksi WHERE id = %s", (id,))
    conn.commit()
    cur.close()