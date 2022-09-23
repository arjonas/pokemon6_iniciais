from flask import  Flask, render_template
import requests
from random import randint
from jinja2 import escape


endpoint = 'https://pokeapi.co/api/v2/pokemon/'
app = Flask('__name__')







@app.route('/')
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
        nome = dados['name']



        data_pokemon[contador] = {'imagem':img,'nome':nome}
        contador = contador + 1




    return render_template('pokemons.html',dados=data_pokemon)






if __name__ == '__main__':
    app.run(debug=True)