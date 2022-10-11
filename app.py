from flask import  Flask, render_template,request,redirect,url_for
import requests
from random import randint,sample

from flask_login import LoginManager


endpoint = 'https://pokeapi.co/api/v2/pokemon/'


Kanto =  [('bulbasaur' ,'ivysaur','venusaur'), ('charmander','charmeleon','charizard') ,
          ('squirtle','wartortle','blastoise')]


Johto = [('chikorita','bayleef','meganium'), ('cyndaquil','quilava','typhlosion')
                                              ,('totodile','croconaw','feraligatr')]

Hoenn = [('treecko','grovyle','sceptile'), ('torchic','combusken','blaziken'),
         ('mudkip','marshtomp','swampert')]




Sinnoh = [('turtwig','grotle','torterra') ,('chimchar','monferno','infernape'),
          ('piplup','prinplup','empoleon')]

Unova = [('snivy','servine','serperior'), ('tepig','pignite','emboar'),
         ('oshawott','dewott','samurott')]
#
Kalos = [('chespin','quilladin','chesnaught'), ('fennekin','braixen','delphox') ,
         ('froakie','frogadier','greninja')]

Alola =  [('rowlet','dartrix','decidueye') ,('litten','torracat','incineroar') ,
          ('popplio','brionne','primarina')]


Galar = [('grookey' ,'scorbunny','sobble'),('scorbunny','encherliguiça'),('sobble','encherlinguiça')]

regioes = [Kanto,Johto,Hoenn,Sinnoh,Unova,Kalos,Alola,Galar]


pk_iniciais = {'charmander':['charmander','charizard','charmeleon'],
               'squirtle':['wartortle','squirtle','blastoide'],
               'bulbasaur':['bulbasaur','ivysaur','venusaur'],
               'cyndaquil':['cyndaquil','quilava','typhlosin'],'chikorita':['bayleef','chickorita',
                'meganium'],'totodile':['croconaw','totodile','feraligatr'],'treecko':['treecko',
                'grovyle','sceptile'],'torchic':['torchic','combusken','blaziken'],
               'mudkip':['mudkip','marshtomp','swampert'],'turtwig':['turtwwig','grotle',
                'torterra'],'chimchar':['chimchar','monferno','infernape'],
               'piplup':['prinplup','piplup', 'empoleon'],'snivy':['snivy','servine','serperior'],
               'tepig':['tepig','pignite','emboar'],'oshawott':['oshawott','dewott','samurott'],
               'chespin':['chespin','quilladin','chesnaught'],'fennekin':['braixen',
                'fennekin','delphox'],'froakie':['froakin','frogadier','greninja'],
               'rowlet':['rowlet','dartrix''decidueye'],'litten':['litten','torracat','inceneroar'],
               'popplio':['popplio','brionne','primarina'],
               'grookey':['grookey','thwackey','rillaboom'],
               'scorbunny':['scorbunny','raboot','cinderace'],
               'sobble':['sobble','dizzile','inteleon']
                 }




pokemons_user = []





endpoint = 'https://pokeapi.co/api/v2/pokemon/'
app = Flask('__name__')







# @app.route('/data')
# def get_pokemons():
#
#     lista = []
#
#     for n in range(0, 6):
#
#         sorted = randint(1, 252)
#
#         while sorted in lista:
#             sorted = randint(1, 905)
#
#         lista.append(sorted)
#
#     data_pokemon = {}
#
#     contador = 1
#
#     for n in lista:
#         resposta = requests.get(endpoint + str(n))
#         dados = resposta.json()
#
#         img = dados['sprites']['front_default']
#         nome = dados['name'].title()
#         tipo = dados['types'][0]['type']['name'].title()
#
#
#         data_pokemon[contador] = {'imagem':img,'nome':nome,'tipo':tipo}
#         contador = contador + 1
#
#
#
#
#     return render_template('pokemons.html',dados=data_pokemon, pokemons_user= pokemons_user)


@app.route('/home')
def logar():

   return render_template('index.html')




@app.route('/',methods=('GET','POST'))
def choice():\

    if request.method == 'POST':

        data = request.form.get('city')
        try:
            # coletando dados de formulario e gerando imagens dos pokemons iniciais


            city = regioes[int(data)]

            iniciais = [item[0] for item in city ]

            init_names =[]
            init_img = []
            for pokemon in iniciais :

                resposta = requests.get(endpoint+pokemon)

                info = resposta.json()

                img = info['sprites']['front_default']
                nome = info['name']

                init_names.append(nome)
                init_img.append(img)
            return render_template('pokemonchoice.html', imgs=init_img, names=init_names)
        except :

            #pegando escolha de pokemon inicial
            pokemon_user = {}
            choice = request.form.get('pokemon')

            pk = pk_iniciais[choice]

            pk_inicial = sample(pk,1)
            i= pk_inicial[0]
            dados = requests.get(endpoint+i)
            dados = dados.json()

            img = dados['sprites']['front_default']
            nome = dados['name']



            pokemon_user['nome'] = nome
            pokemon_user['img'] = img


            #gerando outros 5 pokemons

            lista = []

            for n in range(0, 6):

                sorted = randint(1, 252)

                while sorted in lista:
                    sorted = randint(1, 905)

                lista.append(sorted)

            data_pokemon = {}

            contador = 1

            for n in lista:
                resposta = requests.get(endpoint + str(n))
                dados = resposta.json()

                img = dados['sprites']['front_default']
                nome = dados['name'].title()
                tipo = dados['types'][0]['type']['name'].title()

                data_pokemon[contador] = {'imagem': img, 'nome': nome, 'tipo': tipo}
                contador = contador + 1

            return render_template('pokemons.html', dados=data_pokemon,pokemon_user=pokemon_user)






    return render_template('Start.html')


@app.route('/pk',methods=('GET','POST'))
def inicio():
    global pokemons_user
    if request.method == "POST":




        return render_template('pokemonchoice.html')




@app.route('/jorney',methods=('GET','POST'))
def jornada():

    if request.method == 'POST':

        return redirect(url_for('get_pokemons'))


    return render_template('choice.html')





if __name__ == '__main__':
    app.run(debug=True)