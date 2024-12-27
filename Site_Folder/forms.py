"""
Nesse arquivo python é onde vamos colocar o código de nossos formulários.

Todos os formulários de site são objetos dele e quando trabalhamos com objetos no python, trabalhamos com classes.
Tudo que não for textos dentro do site são tratados como objetos, assim, precisam ser inseridos nos sites usando classes do python.

No flask, nós já temos boa parte dos formulários já prontos, só precisamos dizer quais campos queremos colocar dentro dele e fazer
validações.

Para trabalhar com formulários, importamos a biblioteca flask-wtf. Fazemos a instalação dela a parte do flask, não vem junto com ele. Importamos o FlaskForm dela para trabalhar com os formulários.

O FlaskForm já cria a lógica do formulário, basta a gente criar classes para cada formulário que vamos usar. Vamos criar os formulários de login e criar conta.

As classes que vamos criar para os formulários vão ser subclasses do FlaskForm, vão receber os valores definidos na classes FlaskForm como herança. Para isso, não precisamos definir um __init__
para as classes que criamos para os formulários, porque vai usar o do FlaskForm.
Só precisamos passar os campos dos formulários e o botão submit caso necessário.

Quando instalamos a lib flask_wtf, veio junto com ela a lib wtforms, é essa lib que puxamos os campos do nosso formulário, basta passar o tipo de dados que queremos pegar dessa lib. Fica

from wtforms import StringField,PasswordField,SubmitField

SubmitField representa botão.

Aí, passamos os campos que queremos ter no nosso formulário, o tipo de dado dele e o que terá escrito nessa campo como default

#Criar form de criar conta
class FormCriarConta(FlaskForm):

    username = StringField('Nome do Usuário')
    email = StringField('E-mail do Usuário')
    senha = PasswordField('Senha')
    confirmacao_senha = PasswordField('Confirmação da Senha')
    botao_submit_criarconta = SubmitField('Criar Conta')


#Criar form de login
class FormCriarConta(FlaskForm):

    email = StringField('E-mail do Usuário')
    senha = PasswordField('Senha')
    botao_submit_criarconta = SubmitField('Fazer Login')

Podemos fazer validações desses campos também com a lib wtrforms. Por exemplo, o campo de email deve ser um email válido, tendo @ e outra coisas. Usamos os validators do wtforms

As validações é a ultima coisa que fazemos no nosso código de forms.

Para usar esses validator, importamos eles do wtform fazendo from wtforms.validators import DataRequired,length,Email,EqualTo

DataRequired: para validar se é campo obrigatório
length: para validar o tamanho do campo
Email: para validar se é email
EqualTo: para validar se um campo é igual a outro, usamos para senha e confirmação de senha, que precisam ser iguais.

Nós passamos uma lista de validators para cada campo dentro de nossas classes

class FormCriarConta(FlaskForm):

    username = StringField('Nome do Usuário',validators=[DataRequired()])
    email = StringField('E-mail do Usuário',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),length(6,20)])
    confirmacao_senha = PasswordField('Confirmação da Senha',validators=[DataRequired(),EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')


#Criar form de login
class FormCriarConta(FlaskForm):

    email = StringField('E-mail do Usuário',validators=[DataRequired()])
    senha = PasswordField('Senha',validators=[DataRequired(),Email()])
    botao_submit_criarconta = SubmitField('Fazer Login')


#--------------------------------------------------------------------------------------------------------------------------------#
## Segurança para formulário

Vamos aplicar o csrf token. Todo formulário precisa desse mecanismo para garantir sua segurança.
    


"""

#Importando libs
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from Site_Folder.models import Usuarios
from flask_login import current_user

#Criar form de criar conta
class FormCriarConta(FlaskForm):

    username = StringField('Usuário',validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    confirmacao_senha = PasswordField('Confirmação da Senha',validators=[DataRequired(),EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')
    
    def validate_email(self,email):
        usuario = Usuarios.query.filter_by(email=email.data).first()
        
        if usuario:
            raise ValidationError("Email já cadastrado. Cadastra-se com outro email ou faça login para continuar")
                    

#Criar form de login
class FormLogin(FlaskForm):

    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    botao_submit_login = SubmitField('Fazer Login')
    
#Criar form de editar perfil
class FormEditarPerfil(FlaskForm):

    username = StringField('Usuário',validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil',validators=[FileAllowed(['jpg','jpeg','png'])])
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sql = BooleanField('SQL Impressionador')
    botao_submit_editarperfil = SubmitField('Confirma Edição')
    
    
    def validate_email(self,email):

        #Verficando se o usuário colocou email no campo do forms do que ele usou para iniciar a sessão no site
        if current_user.email != email.data:
            usuario = Usuarios.query.filter_by(email=email.data).first()
            #se tiver um usuário no banco já com o email que ele preencheu no forms, retornar erro
            if usuario:
                raise ValidationError("Já existe um usuário com esse email. Escolha outro email para o seu perfil")
            
            
class FormCriarPost(FlaskForm):
    titulo_post = StringField('Titulo do Post',validators=[DataRequired(),Length(2,140)])
    corpo = TextAreaField('Escreva Seu Post Aqui',validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')
                
            
    