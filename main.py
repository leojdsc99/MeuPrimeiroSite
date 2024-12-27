"""
Arquivo main que vou usar apenas para rodar a aplicação do site.

"""

#Importando libs
from Site_Folder import app,database
from Site_Folder.models import Usuarios,Post

#Rodar esse comando só uma vez para criar o banco de dados
# with app.app_context():
#     database.drop_all()
#     database.create_all()

#Testar agora se tenho usuário criado
# with app.app_context():
#     posts = Post.query.all()
#     post = posts[0]
#     print('### Usuário que fez o post ###')
#     print(post.id_usuario)
    
#     usuarios = Usuarios.query.all()
#     usuario = posts[0]
#     print('### ID do Usuário ###')
#     print(usuario.id)
# #Rodando site
if __name__ == '__main__':
    app.run(debug=True)
    