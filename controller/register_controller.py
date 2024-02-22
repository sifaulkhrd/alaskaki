from flask import Flask, request
from models.register import validator_register_username, validator_register_password,validator_register_fullname, register_data
from models.user import get_users_by_id,edit_data_user
from flask_bcrypt import Bcrypt


def register_new_data_controller():
    """
    Kontroler untuk registrasi data baru dari permintaan formulir.

    Returns:
    - tuple: Tuple berisi pesan respons dan kode status HTTP.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    try:
        # Validasi username
        if validator_register_username(username):
            return {'message': 'Username sudah digunakan oleh pengguna lain'}, 402
        if not username:
            return {'message': 'Username harus diisi'}, 402
        
        # Validasi password
        if validator_register_password(password):
            return {'message': 'Password tidak valid'}, 402
        elif not password:
            return {'message': 'Password harus diisi'}, 402
        elif len(password) < 8:
            return {'message': 'Password harus 8 karakter atau lebih'}, 402


        # Validasi fullname
        if validator_register_fullname(fullname):
            return {'message': 'Fullname sudah digunakan oleh orang lain'}, 402
        elif not fullname:
            return {'message': 'Fullname harus diisi'}, 402
        

        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Proses registrasi
        register_data(username, hashed_password, fullname)
        return {'message': 'Selamat, registrasi berhasil'}, 200
    except Exception as e:
        raise e


def edit_user_controller(current_user_id):
    """
    Fungsi ini mengontrol proses pengeditan data pengguna.

    Parameters:
        current_user_id (str): ID pengguna yang sedang masuk.

    Returns:
        tuple: Tuple berisi dictionary pesan respons dan kode status HTTP.
    """
    try:
        # Pastikan bahwa current_user_id adalah string yang valid
        current_user_id = str(current_user_id)
    except ValueError:
        return {'message': 'ID pengguna tidak valid'}, 400

    username = request.form.get('username')
    password = request.form.get('password')
    fullname = request.form.get('fullname')

    if not username or not password or not fullname:
        return {'message': 'Semua input harus diisi'}, 400
    bcrypt = Bcrypt()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Memperbarui data pengguna
    edit_data_user(
        current_user_id,  # Menggunakan ID pengguna dari token JWT
        username,
        hashed_password,
        fullname,
    )
    return {'message': 'Pembaruan data pengguna berhasil'}, 200


