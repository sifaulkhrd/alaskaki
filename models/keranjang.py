from db import conn

def create_new_keranjang(user_id,produk_id,kuantitas):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO keranjang (user_id,produk_id,kuantitas) VALUES (%s,%s,%s)', (user_id,produk_id,kuantitas))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def get_all_keranjang():
    cur = conn.cursor()

    try:
        cur.execute('SELECT id, user_id, produk_id, kuantitas FROM keranjang ORDER BY id')
        keranjang = cur.fetchall()

        # meng convert tuple ke dictionary
        new_keranjang = []
        for item in keranjang:
            new_item = {
                "id": item[0],
                "user_id": item[1],
                "produk_id": item[2],
                "kuantitas": item[3],
            }
            new_keranjang.append(new_item)
        conn.commit
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
    return new_keranjang

def get_keranjang_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT id, user_id, produk_id, kuantitas FROM keranjang WHERE id = %s', (id,))
    keranjang = cur.fetchone()

    conn.commit()
    cur.close()

    if keranjang is None:
        return None
    
    # untuk meng convert tuple ke dictionary
    return {
        "id": keranjang[0],
        "user_id": keranjang[1],
        "produk_id": keranjang[2],
        "kuantitas": keranjang[3],
    }

def delete_keranjang_by_id(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM keranjang WHERE id = %s", (id,))
    conn.commit()
    cur.close()