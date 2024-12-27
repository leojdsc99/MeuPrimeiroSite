""""
O arquivo que vamos usar para criar as tabelas do banco de dados.
Para nosso arquivo funcionar, precisamos importar o banco de dados, isso aqui: database = SQLAlchemy(app).

Esse database que estamos importando é o que usa o banco de dados.

Agora, podemos criar as colunas de nosso banco de dados, nas tabelas deles.

Cada tabela é uma classe, que tem como herança outra classe chamada de database.Model. ASsim, não precisamos definir o __init__ dela, só precisamos passar as colunas que nossas tabelas terão.

A classe de usuário vai ser

class Usuarios(database.Model):
    id = database.Column(database.Integer,primary_key = True)
    username = database.Column(database.String,nullable = False)
    email = database.Column(database.String, nullable = False, unique = True)
    senha = database.Column(database.String,nullable = False)
    foto_perfil = database.Column(database.String,default = 'default.jpg') 

Na foto de perfil, é string porque no banco vai ser armazenado o nome do arquivo da foto e no site aparecerá a foto. O default também é o que irá aparecer na foto caso o usuário não coloque uma,
como default, vamos colocar aquelas avatares mesmo

A classe de post vai ser

class Post(database.Model):
    id = database.Column(database.Integer,primary_key = True)
    titulo = database.Column(database.String,nullable = False)
    corpo = database.Column(database.Text,nullable = False)
    data_criacao = database.Column(database.DateTime,nullable = False, default = datetime.now(timezone.utc))

Precisamos relacionar a tabela de usuários com a de post para descobrir o autor de um post. Cada usuário pode ter vários posts, 1 para n. 
Nós colocamos o relacionamento dentro da definição da classe da tabela.

A classe de Usuarios fica então

class Usuarios(database.Model):
    id = database.Column(database.Integer,primary_key = True)
    username = database.Column(database.String,nullable = False)
    email = database.Column(database.String, nullable = False, unique = True)
    senha = database.Column(database.String,nullable = False)
    foto_perfil = database.Column(database.String,default = 'default.jpg') 
    posts = database.relationship('Post',backref = 'autor',lazy = True)

O posts é a relação que vamos fazer com a tabela de Post. 

posts = database.relationship('Post',backref = 'autor',lazy = True)

O primeiro parâmetro que está como 'Post' é o nome da tabela que estamos fazendo a relação.
O segundo parâmetro backref = 'autor' significa como que o usuário estará sendo referenciado dentro da tabela de Post.
O parâmetro lazy = True força a quando chamarmos o autor do post na tabela de Post, vai retornar todas as informações desse autor, não só o nome dele. Por exemplo, quando definirmos uma instância
do post: post = Post() e chamarmos post.autor, vai retornar várias informações do autor, não só o nome dele.


Na tabela de Post, precisamos passar a coluna que vai identificar o usuário que fez o post. Ela precisa ser uma informações única que conseguimos puxar da tabela de usuário, nesse caso, iremos usar
o id do usuário.
A classe Post ficará
class Post(database.Model):
    id = database.Column(database.Integer,primary_key = True)
    titulo = database.Column(database.String,nullable = False)
    corpo = database.Column(database.Text,nullable = False)
    data_criacao = database.Column(database.DateTime,nullable = False, default = datetime.now(timezone.utc))
    id_usuario = database.Column(database.Integer,database.ForeignKey('usuario.id'), nullable = False)

database.ForeignKey('usuario.id') aqui indicamos qual coluna da tabela de usuarios estamos usando para ser nossa chave estrangeira aqui na tabela de Post. Sempre passar o nome da classe em minusculo
aqui, mesmo tendo definido a classe como maiusculo.

"""
from Site_Folder import database,login_manager
from datetime import datetime,timezone
from flask_login import UserMixin

#Função para indicar que um usuário pode fazer login
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuarios.query.get(int(id_usuario))

#Tabela usuário
class Usuarios(database.Model,UserMixin):
    id = database.Column(database.Integer,primary_key = True)
    username = database.Column(database.String,nullable = False)
    email = database.Column(database.String, nullable = False, unique = True)
    senha = database.Column(database.String,nullable = False)
    foto_perfil = database.Column(database.String,default = 'default.jpg') 
    posts = database.relationship('Post',backref = 'autor',lazy = True)
    cursos = database.Column(database.String,nullable = False, default = 'Não Informado')
    
    def contar_posts(self):
        return len(self.posts)
        
    
#Tabela de Posts
class Post(database.Model):
    id = database.Column(database.Integer,primary_key = True)
    titulo = database.Column(database.String,nullable = False)
    corpo = database.Column(database.Text,nullable = False)
    data_criacao = database.Column(database.DateTime,nullable = False, default = datetime.now(timezone.utc))
    id_usuario = database.Column(database.Integer,database.ForeignKey('usuarios.id'), nullable = False)

