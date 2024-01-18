from db import conn

def get_all_produk(page:int, limit:int, keyword:str = None):
    cur = conn.cursor()

    try:
        page = (page - 1) * limit
        wherekeyword = ""
        values = {"limit": limit, "offset": page}
        if keyword is not None:
            wherekeyword = " WHERE nama ilike %(keyword)s "
            values['keyword'] = '%'+keyword+'%'
        
        query = f"""
            SELECT id, nama, stok, harga, kategori_id 
            FROM produk
            {wherekeyword}
            ORDER BY id
            limit %(limit)s
            offset %(offset)s
        """
        print(query,values)
        cur.execute(query,values)
        products = cur.fetchall()
        list_products = []
        for item in products:
            new_product = {
                "id": item[0],
                "nama": item[1],
                "stok": item[2],
                "harga": item[3],
                "kategori_id": item[4],
            }
            list_products.append(new_product)
        # return list_products

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
    return list_products


def get_produk_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT id, nama, stok, harga, kategori_id FROM produk WHERE id = %s', (id,))
    produk = cur.fetchone()

    conn.commit()
    cur.close()

    if produk is None:
        return None
    
    # untuk meng convert tuple ke dictionary
    return {
        "id": produk[0],
        "nama": produk[1],
        "stok": produk[2],
        "harga": produk[3],
        "kategori_id": produk[4],
    }

def create_new_produk(nama,stok,harga,kategori_id):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO produk (nama, stok, harga, kategori_id) VALUES (%s,%s,%s,%s) RETURNING id', (nama,stok,harga,kategori_id))
        conn.commit()
        return cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
    finally:
        cur.close()

def update_produk_by_id(id,nama,stok,harga,kategori_id):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE produk SET nama = %s, stok = %s, harga = %s, kategori_id = %s WHERE id = %s;",(nama, stok, harga, kategori_id, id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_produk_by_id(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM produk WHERE id = %s", (id,))
    conn.commit()
    cur.close()

    # uploads gambar
def get_all_images(produk_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * from produk_image WHERE produk_id = %s", (produk_id,))
        hasil = cur.fetchall()
        gambar_produk = []
        for item in hasil:
            gambar = {
                "id": item[0],
                "lokasi": item[1],
                "produk_id": item[2],
            }
            gambar_produk.append(gambar)
        return gambar_produk
    except Exception as e:
        raise e
    finally:
        cur.close()

        
def upload_images(lokasi, produk_id):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO produk_image (lokasi, produk_id) VALUES (%s,%s)', (lokasi, produk_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_image(produk_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM produk WHERE produk_id = %s", (produk_id,))
    conn.commit()
    cur.close()