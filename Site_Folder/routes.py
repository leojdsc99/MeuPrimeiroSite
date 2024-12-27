from Site_Folder import app,database,bcrypt
from flask import render_template, url_for,request,redirect,flash,abort
from Site_Folder.forms import FormCriarConta,FormLogin,FormEditarPerfil,FormCriarPost
from Site_Folder.models import Usuarios,Post
from flask_login import login_user,logout_user,current_user,login_required
import secrets
import os
from PIL import Image

#Criando Páginas
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html',posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuarios.query.all()
    return render_template('usuarios.html',user_list = lista_usuarios)

@app.route('/login',methods = ['GET','POST'])
def login():

    #criado form login
    form_login = FormLogin()

    #criado form criar conta
    form_criarconta = FormCriarConta()

    #validando login
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        #Vendo se email existe no banco e senha está correta
        usuario = Usuarios.query.filter_by(email = form_login.email.data).first()
        
        if usuario and bcrypt.check_password_hash(usuario.senha,form_login.senha.data):       
            login_user(usuario)
            flash(f'Login feito com sucesso para o email {form_login.email.data}!','alert-success')
            
            param_next = request.args.get('next')
            if param_next:
                return redirect(param_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos','alert-danger')
    
    #validando criar conta
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #Criar Usuário
        senha_cripto = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuarios(username=form_criarconta.username.data,email=form_criarconta.email.data,senha=senha_cripto)
        
        #Adicionar Usuário na sessão do banco de dados
        database.session.add(usuario)
        
        #Fazer commit das alterações
        database.session.commit()
        
        #Mostrando imagem de conta criada
        flash(f'Conta criada com sucesso com o email {form_criarconta.email.data}!','alert-success')
        return redirect(url_for('home'))

    return render_template('login.html',form_login=form_login,form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso','alert-success')
    return redirect(url_for('home'))
    

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static',filename=f"fotos_perfil/{current_user.foto_perfil}")
    return render_template('perfil.html',foto_perfil = foto_perfil)



def salvar_imagem(imagem):
    #adicionar código aleatório no nome da imagem    
    codigo = secrets.token_hex(8) #gerar token de 8bytes
    nome,extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    nome_completo = os.path.join(app.root_path,'static/fotos_perfil',nome_arquivo)
    tamanho = (200,200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(nome_completo)
    
    return nome_arquivo

def atualizar_cursos(form):
    #criando lista auxiliar que vai guardar os cursos do usuário
    lista_curso = []
    for campo in form:
        #vendo se o nome do campo do formulário de editar perfil começa com curso_
        if 'curso_' in campo.name:
            if campo.data:
                lista_curso.append(campo.label.text) #colocamos .text porque queremos o texto do label do botão, se não tiver, mostra o objeto, não texto
        #transformando a lista em string
    return ";".join(lista_curso)
            
@app.route('/perfil/editar',methods = ['GET','POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    foto_perfil = url_for('static',filename=f"fotos_perfil/{current_user.foto_perfil}")
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        #se for True, usuário adicionou nova foto para ser enviada para o site
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'Perfil Atualizado com sucesso!','alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('editarperfil.html',foto_perfil = foto_perfil,form=form)


@app.route('/post/criar',methods=['GET','POST'])
@login_required
def criar_post():
    form_post = FormCriarPost()
    
    if form_post.validate_on_submit():
        print('Post')
        post = Post(titulo=form_post.titulo_post.data,corpo = form_post.corpo.data,autor = current_user)
        database.session.add(post)        
        database.session.commit()
        flash('Post Criado com Sucesso','alert-success')
        return (redirect(url_for('home')))
    
    return render_template('criarpost.html',form_post=form_post)


@app.route('/post/<post_id>',methods = ['GET','POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    
    if current_user == post.autor:
        form_post = FormCriarPost()
        form_post.botao_submit.label.text = 'Editar Post'
        if request.method == 'GET':
            form_post.titulo_post.data = post.titulo
            form_post.corpo.data = post.corpo
        elif form_post.validate_on_submit():
            post.titulo = form_post.titulo_post.data
            post.corpo = form_post.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso!','alert-success')
            redirect(url_for('home'))
    else:
        form_post = None
    
    return render_template('post.html',post=post,form_post=form_post)

@app.route('/post/<post_id>/excluir',methods=['GET','POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso','alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)