from db import conn

def validator_register_username(username):
    cur = conn.cursor()
    try:
        cur.execute('SELECT username from users where username = %s',(username,))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e 
    finally:
        cur.close()

def validator_register_password(password):
    cur = conn.cursor()
    try:
        cur.execute('SELECT password from users where password = %s',(password,))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e 
    finally:
        cur.close()

def validator_register_fullname(fullname):
    cur = conn.cursor()
    try:
        cur.execute('SELECT fullname from users where fullname = %s',(fullname,))
        if cur.fetchone():
            return True
    except Exception as e:
        raise e 
    finally:
        cur.close()

def register_data(username,password,fullname):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (username,password,fullname) VALUES (%s,%s,%s)',(username,password,fullname))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()