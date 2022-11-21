import random
import time

import flask

from Constantes import  *

from flask import  Flask, render_template,request,redirect,url_for,session ,jsonify, make_response
import requests

from werkzeug.security import generate_password_hash, check_password_hash

from json import JSONDecodeError
import sqlite3
from flask_login import LoginManager, UserMixin,current_user,login_user, logout_user
from sqlite3 import IntegrityError
import re

#classe do flask_login
login_manager = LoginManager()







endpoint = 'https://pokeapi.co/api/v2/pokemon/'


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

app = Flask(__name__)
# app.app_context().push()
app.config['SECRET_KEY'] = 'key'
login_manager.init_app(app)


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






def valida_email(email):


    if re.search(regex,email):

        return True
    else:
        return False







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
        # Trata erro caso usuario tecle email não existente
        try:
            usuario = load_user(user[0])

        except IndexError:
            error =" Email não cadastrado"
            flask.flash(error)
            return render_template('login.html')





        try:
            logou = check_password_hash(pwhash=usuario.senha, password=senha)

        except AttributeError:

            error = 'Email não cadastrado'
            flask.flash(error)
            return render_template('login.html')



        if logou:
                print('chegou')
                login_user(usuario)
                print('chegou')
                # recupera nome do usuario
                treinador_email = current_user.email
                #query para subir pokemons do usuario
                dados_banco = cursor.execute(f"SELECT nome FROM pokemons WHERE treinador_email = '{treinador_email}'")
                nome = dados_banco.fetchone()
                print(nome)

                if  nome != None:
                    return redirect(url_for('get_all'))
                else:
                    return redirect(url_for('home'))

        else:

                error = 'Senha errada , tente novamente'
                flask.flash(error)
                return render_template('login.html')




    if current_user.is_authenticated:
        return redirect(url_for('home'))


    return render_template('login.html')



@app.route('/registrar', methods=['GET','POST'])
def registrar():


    if request.method == 'POST':

        nome  = request.form.get('nome')
        email = request.form.get('email')

        # função valida_email() verifica se o email digitado esta em um formato valido
        if valida_email(email) == True:
            senha =generate_password_hash(request.form.get('senha'),salt_length=8)

            db = sqlite3.connect('pokemons_iniciais.db')
            cursor = db.cursor()
            try:
                cursor.execute(f"INSERT INTO usuarios (nome, email, senha) VALUES('{nome}','{email}', '{senha}')")
                db.commit()
                db.close()
                return redirect(url_for('login'))

            # erro causado caso já exista o email digitado pelo usuario
            except IntegrityError:

                error = 'Email já cadastrado para um usuario'
                flask.flash(error)
                return render_template('registrar.html')

       #caso o usuario insira um formato de email incomum
        else:
            error = 'Insira um formato de email válido'
            flask.flash(error)
            return render_template('registrar.html')

    return render_template('registrar.html')


@app.route('/logout')
def logout():

    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))


@app.route('/home',methods=['POST','GET'])
def home():

    #escolher pokemon inicial
    if request.method == "POST":

        escolha = request.form.get('city')

        return redirect(url_for('inicial_pokemon',escolha=escolha))

    #CIDADE INICIAL
    if request.method == "GET":
        usuario = current_user.nome
        return render_template('Start.html',user = usuario)



@app.route('/pokemon',methods=['GET','POST'])
def inicial_pokemon():

    escolha = request.args.get('escolha')

    regiao = regioes[int(escolha)]
    #pega pokemons iniciais através de item[0] (primeiro item da tupla item que está em regioes
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


    usuario = current_user.nome

    return render_template('pokemonchoice.html',inicial_img=iniciais_img,inicial_nome=iniciais_nome,
                           user=usuario)







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
    print(data)

    #escolha o pokemon inicial atraves das escolhas e sua evolução .. utilizando dicionario
# 'pk_iniciais'
    inicial = random.choice(pk_iniciais[data])

    Resposta = False

    while Resposta == False:
        try:
            dados = requests.get(endpoint + inicial)
            time.sleep(0.7)
            dados = dados.json()
            print(1)
            Resposta = True

        except JSONDecodeError:


             response = make_response(jsonify({"Error":"Erro de resposta do Servidor da API , tente denovo"}))

             return  response





    treinador_email = current_user.email

    img = dados['sprites']['front_default']
    nome = dados['name']
    tipo = dados['types'][0]['type']['name'].title()




    db = sqlite3.connect('pokemons_iniciais.db')
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO pokemons VALUES('{treinador_email}','{nome}','{img}', '{tipo}')")
    db.commit()
    db.close()



    return render_template('choice.html',user=current_user.nome)


@app.route('/oi',methods=['GET','POST'])
def final():
    # lista criada para evitar pokemons repetidos
    lista_de_numeros = []
    pokemon_number = ''



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
            while len(lista_de_numeros) < 5:
                pokemon_number = random.randint(pk_id1,pk_id2)
                if pokemon_number not in lista_de_numeros:
                    lista_de_numeros.append(pokemon_number)
                    print(lista_de_numeros)

                    pokemon_number = str(pokemon_number)

                    resposta = requests.get(endpoint+pokemon_number)

                    resposta  = resposta.json()


                    treinador_email = current_user.email
                    img = resposta['sprites']['front_default']
                    nome = resposta['name']
                    tipo = resposta['types'][0]['type']['name'].title()
            #
            #

            #
                    db = sqlite3.connect('pokemons_iniciais.db')
                    cursor = db.cursor()
                    cursor.execute(f"INSERT INTO pokemons VALUES('{treinador_email}','{nome}','{img}', '{tipo}')")
                    db.commit()
                    db.close()


        return redirect(url_for('get_all'))




@app.route('/todos')
def get_all():

    treinador_email = current_user.email

    #criando listas vazias para inserir dados extraido do banco
    imagens = []
    nomes = []
    tipos = []

    #conexão com o banco
    db = sqlite3.connect('pokemons_iniciais.db')
    cursor = db.cursor()

    dados_banco = cursor.execute(f"SELECT nome FROM pokemons WHERE treinador_email = '{treinador_email}'")
    nome = dados_banco.fetchall()



    for  tupla in  nome:

        nomes.append(tupla[0])
        print(nomes)

    dados_banco = cursor.execute(f"SELECT imagem FROM pokemons WHERE treinador_email = '{treinador_email}'")
    imagem = dados_banco.fetchall()

    for tupla in imagem:
        imagens.append(tupla[0])



    dados_banco = cursor.execute(f"SELECT tipo FROM pokemons WHERE treinador_email = "
                                 f"'{treinador_email}'")
    tipo = dados_banco.fetchall()

    for tupla in tipo:
        tipos.append(tupla[0])


    return render_template('pokemons.html', imgs = imagens , tipos=tipos, nomes=nomes ,
                           user=current_user.nome)



if __name__ == '__main__':
    app.run(debug=True)