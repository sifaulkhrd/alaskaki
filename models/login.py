from db import conn

def get_username(username, password): 
    cur = conn.cursor()
    try:
        cur.execute('SELECT username,password,fullname from users where username = %s AND password = %s',(username,password))
        user = cur.fetchone()
        print(user)
        if user :
            return {"fullname": user[2]}
    except Exception as e:
        raise e
    finally:
        cur.close()

