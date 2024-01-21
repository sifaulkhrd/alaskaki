from db import conn

# untuk melihat semua produk tanpa limit
def get_all_produk():
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, nama, stok, harga, kategori_id FROM produk")
        produk = cur.fetchall()

        # convert tuple to dictionary
        new_produk = []
        for item in produk:
            new_item = {
                "id": item[0],
                "nama": item[1],
                "stok": item[2],
                "harga": item[3],
                "kategori_id": item[4],
            }
            new_produk.append(new_item)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    return new_produk

# ini untuk untuk melihat semua produk limit
def get_all_produk_limit(page:int, limit:int, keyword:str = None, min_harga:int=None, max_harga:int=None):
    cur = conn.cursor()

    try:
        page = (page - 1) * limit
        where = []
        wherekeyword = ""
        values = {"limit": limit, "offset": page}

        if keyword is not None:
            wherekeyword = " WHERE nama ilike %(keyword)s "
            values['keyword'] = '%'+keyword+'%'

        if max_harga is not None and min_harga is not None:
            where.append("harga BETWEEN %(min_harga)s AND %(max_harga)s")
            values['min_harga'] = min_harga
            values['max_harga'] = max_harga

        elif max_harga is not None:
            where.append("harga <= %(max_harga)s")
            values['max_harga'] =  max_harga

        elif min_harga is not None:
            where.append("harga >= %(min_harga)s")
            values['min_harga'] =  min_harga

        if len(where) > 0:
            where = "WHERE " + " AND ".join(where)
        else:
            where = ""

        query = f"""
            SELECT id, nama, stok, harga, kategori_id 
            FROM produk
            {wherekeyword}
            {where}
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

def get_produk_by_kategori(kategori_id: int):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id, nama, stok, harga, kategori_id
            FROM produk
            WHERE kategori_id=%(kategori_id)s
            order by id asc
        """,
            {"kategori_id":kategori_id}
        )
        result_set = cur.fetchall()
        if result_set is not None:
            produk = []
            for row in result_set:
                new_produk = {
                    "id": row[0],
                    "nama": row[1],
                    "stok": row[2],
                    "harga": row[3],
                    "kategori_id": row[4],
                }
                produk.append(new_produk)
            return produk
        else:
            return None
    except Exception as e:
        raise e
    finally:
        cur.close()


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