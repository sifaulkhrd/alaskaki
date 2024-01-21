from db import conn

def get_kategori_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT id, nama FROM kategori WHERE id = %s', (id,))
    kategori = cur.fetchone()

    conn.commit()
    cur.close()

    if kategori is None:
        return None
    
    return {
        "id": kategori[0],
        "nama": kategori[1],
    }

def get_all_kategori():
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, nama FROM kategori")
        produk = cur.fetchall()

        # convert tuple to dictionary
        new_kategori = []
        for item in produk:
            new_item = {
                "id": item[0],
                "nama": item[1],
            }
            new_kategori.append(new_item)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    return new_kategori

