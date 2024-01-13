from db import conn

def get_all_produk():
    cur = conn.cursor()

    try:
        cur.execute('SELECT id, nama, cover, stok, harga, kategori_id FROM produk ORDER BY id')
        produk = cur.fetchall()

        # meng convert tuple ke dictionary
        new_produk = []
        for item in produk:
            new_item = {
                "id": item[0],
                "nama": item[1],
                "cover": item[2],
                "stok": item[3],
                "harga": item[4],
                "kategori_id": item[5],
            }
            new_produk.append(new_item)
        conn.commit
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
    return new_produk

def get_produk_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT id, nama, cover, stok, harga, kategori_id FROM produk WHERE id = %s', (id,))
    produk = cur.fetchone()

    conn.commit()
    cur.close()

    if produk is None:
        return {'message':'produk tidak di temukan'}
    
    # untuk meng convert tuple ke dictionary
    return {
        "id": produk[0],
        "nama": produk[1],
        "cover": produk[2],
        "stok": produk[3],
        "harga": produk[4],
        "kategori_id": produk[5],
    }

def create_new_produk(nama,cover,stok,harga,kategori_id):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO produk (nama, cover, stok, harga, kategori_id) VALUES (%s,%s,%s,%s,%s)', (nama,cover,stok,harga,kategori_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cur.close()

def update_produk_by_id(id,nama,cover,stok,harga,kategori_id):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE produk SET (id,nama, cover, stok, harga, kategori_id) VALUES (%s,%s,%s,%s,%s,%s) WHERE id = %s",(id))
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cur.close()