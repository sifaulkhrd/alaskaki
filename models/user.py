from db import conn

def get_users_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT id, username, password, fullname FROM users WHERE id = %s', (id,))
    users = cur.fetchone()

    conn.commit()
    cur.close()

    if users is None:
        return None
    
    return {
        "id": users[0],
        "username": users[1],
        "password": users[2],
        "fullname": users[3],
    }