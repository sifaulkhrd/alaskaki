from flask import Flask, request
from models.login import get_username
from datetime import timedelta
from flask_bcrypt import Bcrypt

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

def login_user_controller():
    """
    Kontroler untuk proses login pengguna.

    Returns:
    - dict: Dictionary berisi token akses jika login berhasil, atau pesan kesalahan jika login gagal.
    """
    username = request.form.get('username')
    password = request.form.get('password')

    # Memeriksa apakah username atau password kosong
    if not username or not password:
        return {'message': 'Semua inputan harus diisi'}
    
        # Memeriksa data pengguna
    check_user = get_username(username)
    
    if check_user:

        hashed_password = check_user['password']

        bcrypt = Bcrypt()

        if bcrypt.check_password_hash(hashed_password, password):
            # Jika data pengguna ditemukan, membuat token akses
            token = create_access_token(identity={"id": check_user["id"], "fullname": check_user["fullname"]}, expires_delta=timedelta(hours=1))
            
            return {'token': token}
    
    return {'message': 'Password atau username salah'}
    
    # # Memeriksa data pengguna
    # check_user_data = get_username(username, password)

    # hashed_password = check_user_data['password']

    # bcrypt = Bcrypt()

    # if bcrypt.check_password_hash(hashed_password, password):
    
    # # Jika data pengguna ditemukan, membuat token akses
    # # if check_user_data:
    #     token = create_access_token(identity={"id": check_user_data[0]["id"], "fullname": check_user_data[1]["fullname"]}, expires_delta=timedelta(hours=1))
        
    #     return {'token': token}
    # else:
    #     return {'message': 'Password atau username salah'}
