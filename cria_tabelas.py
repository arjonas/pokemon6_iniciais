import sqlite3


from app import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemons.db'
engine='sqlite://'


db = sqlite3.connect('pokemons_iniciais.db')

cursor = db.cursor()
cursor.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY,"
               " nome varchar(250) NOT NULL ,email varchar(30) NOT NULL UNIQUE , senha varchar(80) NOT NULL)")




cursor = db.cursor()
cursor.execute("CREATE TABLE pokemons (treinador_email varchar(30),"
               " nome varchar(250) NOT NULL , imagem varchar(250) NOT NULL, tipo varchar(250) NOT NULL,"
               "FOREIGN KEY (treinador_email) references usuarios(email) )")



