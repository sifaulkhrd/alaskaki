from flask import Flask, request
from models.login import get_username
from models.register import validator_register_username, validator_register_password,validator_register_fullname, register_data
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "ini token nya"


@app.post('/register')
def register_new_data():
    username = request.form.get('username')
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    try:
        if validator_register_username(username):
            return {'message': 'Username sudah digunakan oleh pengguna lain'}, 402
        if not username:
            return {'message': 'username harus diisi'}, 402

        if validator_register_password(password):
            return {'message': 'Password sudah digunakan oleh pengguna lain'}, 402
        elif not password:
            return {'message': 'password harus diisi'}, 402
        elif len(password) < 8:
            return {'message': 'Password harus 8 karakter atau lebih'}, 402

        if validator_register_fullname(fullname):
            return {'message': 'Fullname sudah di gunakan orang lain'}, 402
        elif not fullname:
            return {'message': 'Fullname harus diisi'}, 402
        
        register_data(username,password,fullname)
        return {'message': 'selamat registrasi telah berhasil'},200
    except Exception as e:
        raise e

@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    check_user_data = get_username(username,password)
    
    if check_user_data:
        token = create_access_token(identity=username)
        return {'token':token}
    else:
       return {'message':'password atau username salah'}

@app.get('/protected')
@jwt_required()
def protected():
    currend_user = get_jwt_identity()
    return {'logged as': currend_user},200


if __name__==('main'):
    app.run(debug=True, use_reloader=True, host="0.0.0.0")