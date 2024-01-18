from db import conn

def get_transaksi_detail_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT id, produk_id, harga, kuantitas, transaksi_id FROM transaksi_detail WHERE id = %s', (id,))
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
    }


def create_new_transaksi_detail(produk_id,harga,kuantitas,transaksi_id):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO transaksi_detail (produk_id,harga,kuantitas,transaksi_id) VALUES (%s,%s,%s,%s)', (produk_id,harga,kuantitas,transaksi_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def get_all_transaksi_detail():
    cur = conn.cursor()

    try:
        cur.execute('SELECT id, produk_id, harga, kuantitas, transaksi_id FROM transaksi_detail ORDER BY id')
        transaksi_detail = cur.fetchall()

        # meng convert tuple ke dictionary
        new_transaksi_detail = []
        for item in transaksi_detail:
            new_item = {
                "id": item[0],
                "produk_id": item[1],
                "harga": item[2],
                "kuantitas": item[3],
                "transaksi_id": item[4],
            }
            new_transaksi_detail.append(new_item)
        conn.commit
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
    return new_transaksi_detail


def delete_transaksi_detail_by_id(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM transaksi_detail WHERE id = %s", (id,))
    conn.commit()
    cur.close()
