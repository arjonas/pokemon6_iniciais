import random
from Constantes import  *

from flask import  Flask, render_template,request,redirect,url_for,session
import requests
from random import randint,sample

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_login import LoginManager, UserMixin,current_user,login_user



#classe do flask_login
login_manager = LoginManager()







endpoint = 'https://pokeapi.co/api/v2/pokemon/'

app = Flask(__name__)
# app.app_context().push()
app.config['SECRET_KEY'] = 'key'
login_manager.init_app(app)




#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemons.db'
# engine='sqlite://'
#
#
# db = sqlite3.connect('pokemons_iniciais.db')
#
# cursor = db.cursor()
# cursor.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY,"
#                " nome varchar(250) NOT NULL ,email varchar(30) NOT NULL , senha varchar(80) NOT NULL)")
#
#
#
#
# cursor = db.cursor()
# cursor.execute("CREATE TABLE pokemons (id INTEGER PRIMARY KEY,"
#                " nome varchar(250) NOT NULL UNIQUE, imagem varchar(250) NOT NULL, tipo varchar(250) NOT NULL,"
#                "FOREIGN KEY (Treinador) references usuarios(id) )")











#
#
# #Classe Usuario para o tabela do banco de dados
# class Usuario(db.Model):
#     __tablename__ ='usuarios'
#     id = Column(Integer,primary_key=True)
#     nome = Column(String(1000))


#Flask login classes e configurações

class User(UserMixin):

    def __init__(self,id , nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.authenticated = False

        def is_authenticated(self):
            return self.authenticated

        def get_id(self):
            return self.id







@login_manager.user_loader
def load_user(user_id):
    db = sqlite3.connect('pokemons_iniciais.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from usuarios where id = {int(user_id[0])}")

    lista_de_resultados = cursor.fetchone()

    if lista_de_resultados is None:
        return None
    else:

        return  User(int(lista_de_resultados[0]), lista_de_resultados[1], lista_de_resultados[2]
                    ,lista_de_resultados[3])
@app.route('/',methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        email= request.form.get('email')
        senha = request.form.get('pass')



        db = sqlite3.connect('pokemons_iniciais.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from usuarios where email='{email}'")
        user = cursor.fetchall()
        print(user)
        usuario = load_user(user[0])

        if email == usuario.email and senha == usuario.senha:
            print('chegou')
            login_user(usuario)
            print('chegou')
            return redirect(url_for('home'))



    if current_user.is_authenticated:
        return redirect(url_for('home'))


    return render_template('login.html')



@app.route('/registrar', methods=['GET','POST'])
def registrar():


    if request.method == 'POST':

        nome  = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        print('oi')
        db = sqlite3.connect('pokemons_iniciais.db')
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO usuarios (nome, email, senha) VALUES('{nome}','{email}', '{senha}')")
        db.commit()
        db.close()


    return render_template('registrar.html')




@app.route('/home',methods=['POST','GET'])
def home():

    #escolher pokemon inicial
    if request.method == "POST":

        escolha = request.form.get('city')

        return redirect(url_for('inicial_pokemon',escolha=escolha))

    #CIDADE INICIAL
    if request.method == "GET":

        return render_template('Start.html')



@app.route('/pokemon',methods=['GET','POST'])
def inicial_pokemon():

    escolha = request.args.get('escolha')

    regiao = regioes[int(escolha)]

    pokemons_iniciais = [item[0] for item in regiao]

    iniciais_nome =[]
    iniciais_img = []
    for pokemon in pokemons_iniciais:

        dados = requests.get(endpoint+pokemon)
        dados.raise_for_status()  # raises exception when not a 2xx response
        if dados.status_code != 204:
            dados =dados.json()



            img = dados['sprites']['front_default']
            nome = dados['name']

            iniciais_img.append(img)
            iniciais_nome.append(nome)




    return render_template('pokemonchoice.html',inicial_img=iniciais_img,inicial_nome=iniciais_nome)







@app.route('/jornada',methods=['GET','POST'])
def jornada():



#POST
    # if request.method ==  'POST':
    #
    #     dados = request.form.get('city')
    #     return redirect(url_for('final',dados = dados))

#  GET pega dados recebidos na rota inicial_pokemon tra e adiciona ao banco de dados.. retorna
#pagina para escolher cidades por onde passou
    data = request.form.get('pokemon')

    inicial = random.choice(pk_iniciais[data])




    dados = requests.get(endpoint + inicial)
    dados = dados.json()




    img = dados['sprites']['front_default']
    nome = dados['name']
    tipo = dados['types'][0]['type']['name'].title()




    db = sqlite3.connect('pokemons_iniciais.db')
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO pokemons VALUES(1,'{nome}','{img}', '{tipo}')")
    db.commit()
    db.close()


    return render_template('choice.html')


@app.route('/oi',methods=['GET','POST'])
def final():

    if request.method == 'POST':
        # Pega cidades escolhidas na pagina anterior
        dados = request.form.getlist('city')

        for id in range(2, 7):
            #randoniza valores de uma das cidades escolhidas exemplo :[0,150]
            cidade_da_capitura = random.choice(dados)

            # trata valores que estão em string para poder transforma-los em inteiroe
            # então os transformam
            pk_id1 = cidade_da_capitura[1:4]

            pk_id1 = int(pk_id1.replace(",",""))


            pk_id2 = int(cidade_da_capitura[4:9].strip("],"))



            #randoniza um numero no range entre  numeros fornecidos
            pokemon_number = str(random.randint(pk_id1,pk_id2))

            resposta = requests.get(endpoint+pokemon_number)

            resposta  = resposta.json()

            img = resposta['sprites']['front_default']
            nome = resposta['name']
            tipo = resposta['types'][0]['type']['name'].title()
            #
            #

            #
            db = sqlite3.connect('pokemons_iniciais.db')
            cursor = db.cursor()
            cursor.execute(f"INSERT INTO pokemons VALUES({id},'{nome}','{img}', '{tipo}')")
            db.commit()
            db.close()


        return redirect(url_for('get_all'))




@app.route('/todos')
def get_all():
    #criando listas vazias para inserir dados extraido do banco
    imagens = []
    nomes = []
    tipos = []

    #conexão com o banco
    db = sqlite3.connect('pokemons_iniciais.db')
    cursor = db.cursor()

    dados_banco = cursor.execute("SELECT nome FROM pokemons ORDER BY id ASC")
    nome = dados_banco.fetchall()



    for  tupla in  nome:
        print(tupla[0])
        nomes.append(tupla[0])


    dados_banco = cursor.execute("SELECT imagem FROM pokemons")
    imagem = dados_banco.fetchall()

    for tupla in imagem:
        imagens.append(tupla[0])



    dados_banco = cursor.execute("SELECT tipo FROM pokemons")
    tipo = dados_banco.fetchall()

    for tupla in tipo:
        tipos.append(tupla[0])



    return render_template('pokemons.html', imgs = imagens , tipos=tipos, nomes=nomes)



if __name__ == '__main__':
    app.run(debug=True)