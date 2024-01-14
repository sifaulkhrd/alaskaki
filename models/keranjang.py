from db import conn

def create_new_keranjang(user_id,produk_id,kuantitas):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO produk (user_id,produk_id,kuantitas) VALUES (%s,%s,%s)', (user_id,produk_id,kuantitas))
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cur.close()

def delete_keranjang_by_id(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM keranjang WHERE id = %s", (id,))
    conn.commit()
    cur.close()