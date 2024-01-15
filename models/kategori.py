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