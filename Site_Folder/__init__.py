"""
O comando app.config['SQLALCHEMY_DATABASE_URI'] é o caminho onde nosso banco de dados vai ser criado, então passamos
o caminho para ele como:

'sqlite:///C:/Users/LeonardoConceição/Desktop/Leonardo/Estudos/Hashtag/Python/flask_estudo/flask_sites/Site_Folder/comunidade.db'
Aqui será criado dentro da pasta Site_Folder

Ou passamos 
'sqlite:///comunidade.db'
Que criará o banco dentro da pasta onde rodo o main.py
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,current_user


#Definindo App
app = Flask(__name__, template_folder="templates")

#Criando token de segurança
app.config['SECRET_KEY'] = '11b9f716748dabe0fcfdfd06f75cd0bd'

#Configurando banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/LeonardoConceição/Desktop/Leonardo/Estudos/Hashtag/Python/flask_estudo/flask_sites/Site_Folder/comunidade.db'

#Criando banco de dados
database = SQLAlchemy(app)

#instância para criptografar a senha
bcrypt = Bcrypt(app)

#Instância de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.context_processor
def inject_current_user():
    print(f"Injetando current_user: {current_user.is_authenticated}")
    return {'current_user': current_user}

from Site_Folder import routes