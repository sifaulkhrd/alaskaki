from db import conn

def get_username(username, password): 
    cur = conn.cursor()
    try:
        cur.execute('SELECT username from users where username = %s AND password = %s',(username,password))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e
    finally:
        cur.close()

