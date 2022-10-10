from flask import  Flask, render_template,request,redirect,url_for
import requests
from random import randint

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


Galar = [('grookey' ,'scorbunny','sobble')]

regioes = [Kanto,Johto,Hoenn,Sinnoh,Unova,Kalos,Alola,Galar]













endpoint = 'https://pokeapi.co/api/v2/pokemon/'
app = Flask('__name__')







@app.route('/data')
def get_pokemons():

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


        data_pokemon[contador] = {'imagem':img,'nome':nome,'tipo':tipo}
        contador = contador + 1




    return render_template('pokemons.html',dados=data_pokemon)


@app.route('/home')
def logar():

   return render_template('index.html')




@app.route('/',methods=('GET','POST'))
def choice():\

    if request.method == 'POST':


        #coletando dados de formulario e gerando imagens dos pokemons iniciais
        data = request.form.get('city')


        city = regioes[int(data)]

        iniciais = [item[0] for item in city ]

        init_img = []
        for pokemon in iniciais :

            resposta = requests.get(endpoint+pokemon)

            info = resposta.json()

            img = info['sprites']['front_default']

            init_img.append(img)

        return render_template('pokemonchoice.html' , imgs = init_img)





    return render_template('Start.html')


@app.route('/pk',methods=('GET','POST'))
def inicio():

    if request.method == "POST":

        return  redirect(url_for('jornada'))



    return render_template('pokemonchoice.html')




@app.route('/jorney',methods=('GET','POST'))
def jornada():

    if request.method == 'POST':

        return redirect(url_for('get_pokemons'))


    return render_template('choice.html')





if __name__ == '__main__':
    app.run(debug=True)