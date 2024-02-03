from flask import Flask, request
from models.register import validator_register_username, validator_register_password,validator_register_fullname, register_data



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
            return {'message': 'Password sudah digunakan oleh pengguna lain'}, 402
        elif not password:
            return {'message': 'Password harus diisi'}, 402
        elif len(password) < 8:
            return {'message': 'Password harus 8 karakter atau lebih'}, 402

        # Validasi fullname
        if validator_register_fullname(fullname):
            return {'message': 'Fullname sudah digunakan oleh orang lain'}, 402
        elif not fullname:
            return {'message': 'Fullname harus diisi'}, 402
        
        # Proses registrasi
        register_data(username, password, fullname)
        return {'message': 'Selamat, registrasi berhasil'}, 200
    except Exception as e:
        raise e
