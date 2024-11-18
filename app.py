## export FLASK_APP=app.py
## old export DATABASE_URL=postgresql://tarefas:7odhP4yn7ZT8YWWd5KiR6bXoLgxdBe7v@dpg-co6337m3e1ms73bet640-a.frankfurt-postgres.render.com/tarefas_tbhr
## new export DATABASE_URL=postgresql://tarefas_skl3_user:uWr9zLvm119Qo4SAJSOxmLuHmFqq5m8j@dpg-cstf0k8gph6c739dd940-a.oregon-postgres.render.com/tarefas_skl3
## flask run


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy import or_

from doadiar import adiar
from criar import criar
from editar import editar
from eliminar import eliminar
from feita import feita
from filtro import exibirFiltroCustom
from models import criar_bd



app = Flask(__name__)
app.secret_key = 'chave'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
    feita = db.Column(db.Boolean)
    data_primeira_vez = db.Column(db.DateTime)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_alteracao = db.Column(db.DateTime, onupdate=datetime.utcnow)
    intervalo_repeticao_mode = db.Column(db.String(50))
    intervalo_repeticao_value = db.Column(db.String(50))
    proximo_domingo = db.Column(db.Boolean)
    data_proxima = db.Column(db.DateTime)
    data_proxima_seguinte = db.Column(db.DateTime)
    classe = db.Column(db.Integer)
    notas = db.Column(db.String(200))
    ordem = db.Column(db.Integer)
    owner = db.Column(db.String(50))

# Criar as tabelas antes de processar a primeira requisição
@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def go_home():
    return exibirFiltroCustom(Tarefa, db, owner=None, filtrar_data_mais_proxima=True)



@app.route('/exibir_filtro', methods=['GET'])
def do_filter():
    return exibirFiltroCustom(Tarefa, db, owner=None, filtrar_data_mais_proxima=True)


@app.route('/exibir_todas', methods=['GET'])
def exibir_todas():
    return exibirFiltroCustom(Tarefa, db)

# edit tarefa
@app.route('/tarefa-feita/<id>')
def tarefa_feita(id):
    return feita(Tarefa,db,id)

@app.route('/tarefa-adiar/<id>')
def tarefa_adiar(id):
    return adiar(Tarefa,db,id)


@app.route('/atualizar_tarefa/<int:id>', methods=['POST'])
def atualizar_tarefa(id):
    return editar(Tarefa,db,id)


@app.route('/editar_tarefa/<int:id>', methods=['GET'])
def editar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    return render_template('editar_tarefa.html', tarefa=tarefa)

# eliminar tarefa

@app.route('/eliminar-tarefa/<id>')
def eliminar_tarefa(id):
    return eliminar(Tarefa,db,id)

# criar tarefas
    
@app.route('/criar-tarefa', methods=['POST'])
def criar_tarefa():
    return criar(Tarefa,db)


if __name__ == "__main__":
    app.run(debug=True)
