from db import conn


def get_all_produk(page: int, limit: int, keyword: str = None, min_harga: int = None, max_harga: int = None):
    """
    Mendapatkan semua produk dengan batasan halaman, limit, dan filter opsional.

    Args:
    - page (int): Halaman yang diinginkan.
    - limit (int): Jumlah produk per halaman.
    - keyword (str): Kata kunci pencarian produk (opsional).
    - min_harga (int): Harga minimum produk (opsional).
    - max_harga (int): Harga maksimum produk (opsional).

    Returns:
    - list: List berisi dictionary informasi produk.
    """
    cur = conn.cursor()

    try:
        page = (page - 1) * limit
        where = []
        values = {"limit": limit, "offset": page}

        if keyword is not None:
            where.append("nama ILIKE %(keyword)s")
            values['keyword'] = '%' + keyword + '%'

        if max_harga is not None and min_harga is not None:
            where.append("harga BETWEEN %(min_harga)s AND %(max_harga)s")
            values['min_harga'] = min_harga
            values['max_harga'] = max_harga

        elif max_harga is not None:
            where.append("harga <= %(max_harga)s")
            values['max_harga'] = max_harga

        elif min_harga is not None:
            where.append("harga >= %(min_harga)s")
            values['min_harga'] = min_harga

        if where:
            where_clause = "WHERE " + " AND ".join(where)
        else:
            where_clause = ""

        query = f"""
            SELECT id, nama, stok, harga, kategori_id 
            FROM produk
            {where_clause}
            ORDER BY harga ASC
            LIMIT %(limit)s
            OFFSET %(offset)s
        """
        cur.execute(query, values)
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

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    return list_products



def get_produk_by_id(id):
    """
    Mendapatkan informasi satu produk beserta gambar berdasarkan ID.

    Args:
    - id (int): ID produk yang dicari.

    Returns:
    - dict or None: Dictionary berisi informasi produk (id, nama, stok, harga, kategori_id) jika ditemukan,
      atau None jika tidak ditemukan.
    """
    cur = conn.cursor()
    cur.execute('SELECT id, nama, stok, harga, kategori_id FROM produk WHERE id = %s', (id,))
    produk = cur.fetchone()

    if produk:
        new_item = {
            "id": produk[0],
            "nama": produk[1],
            "stok": produk[2],
            "harga": produk[3],
            "kategori_id": produk[4]
        }
        return new_item
    else:
        return None

    

def get_produk_by_kategori(kategori_id: int):
    """
    Mendapatkan semua produk berdasarkan ID kategori.

    Args:
    - kategori_id (int): ID kategori yang dicari.

    Returns:
    - list or None: List berisi dictionary informasi produk (id, nama, stok, harga, kategori_id) jika ditemukan,
      atau None jika tidak ditemukan.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id, nama, stok, harga, kategori_id
            FROM produk
            WHERE kategori_id=%(kategori_id)s
            ORDER BY id ASC
        """,
            {"kategori_id": kategori_id}
        )
        result_set = cur.fetchall()
        if result_set:
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


def create_new_produk(nama, stok, harga, kategori_id):
    """
    Menambahkan produk baru ke dalam database.

    Args:
    - nama (str): Nama produk.
    - stok (int): Jumlah stok produk.
    - harga (int): Harga produk.
    - kategori_id (int): ID kategori produk.

    Returns:
    - int: ID produk yang baru ditambahkan.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query atau saat rollback.
    """
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO produk (nama, stok, harga, kategori_id) VALUES (%s, %s, %s, %s) RETURNING id', (nama, stok, harga, kategori_id))
        conn.commit()
        return cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def update_produk_by_id(id, nama, stok, harga, kategori_id):
    """
    Mengedit data produk berdasarkan ID.

    Args:
    - id (int): ID produk yang akan diubah.
    - nama (str): Nama baru produk.
    - stok (int): Stok baru produk.
    - harga (int): Harga baru produk.
    - kategori_id (int): ID kategori baru produk.

    Raises:
    - Exception: Jika terjadi kesalahan saat eksekusi query atau saat rollback.
    """
    cur = conn.cursor()
    try:
        cur.execute("UPDATE produk SET nama = %s, stok = %s, harga = %s, kategori_id = %s WHERE id = %s;", (nama, stok, harga, kategori_id, id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()


def delete_produk_by_id(id):
    """
    Menghapus produk berdasarkan ID dari database.

    Args:
    - id (int): ID produk yang akan dihapus.

    Returns:
    None
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM produk WHERE id = %s", (id,))
    conn.commit()
    cur.close()


# melihat semua image
def get_all_images(produk_id):
    """
    Retrieve all images associated with a specific product.

    Parameters:
    - produk_id (int): The ID of the product.

    Returns:
    list: A list of dictionaries containing information about each image associated with the product.
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM produk_image WHERE produk_id = %s", (produk_id,))
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

# fungsi untuk menambahkan image di create produk
def upload_images(lokasi, produk_id):
    """
    Upload an image associated with a specific product to the database.

    Parameters:
    - lokasi (str): The file path or location of the image.
    - produk_id (int): The ID of the product to which the image belongs.

    Returns:
    None
    """
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO produk_image (lokasi, produk_id) VALUES (%s, %s)', (lokasi, produk_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

# fungsi untuk menghapus gambar bersama data produk
def delete_images_by_produk_id(produk_id):
    """
    Delete all images associated with a specific product from the database.

    Parameters:
    - produk_id (int): The ID of the product whose images will be deleted.

    Returns:
    None
    """
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM produk_image WHERE produk_id = %s", (produk_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

# Fungsi untuk mengurangi stok produk
def update_produk_stok(produk_id, kuantitas):
    cur = conn.cursor()
    try:
        # Mendapatkan stok produk saat ini
        cur.execute("SELECT stok FROM produk WHERE id = %s", (produk_id,))
        current_stok = cur.fetchone()


        # Mengurangi stok produk
        new_stok = int(current_stok[0]) - int(kuantitas)

        # Memperbarui stok produk di database
        cur.execute("UPDATE produk SET stok = %s WHERE id = %s", (new_stok, produk_id))

    except Exception as e:
        # Handle kesalahan sesuai kebutuhan Anda
        raise e
    finally:
        cur.close()