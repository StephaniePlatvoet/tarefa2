#routes.py

from flask import render_template, Blueprint
from sqlalchemy import or_

from .models import Tarefa
from .extentions import db, adiar, criar, editar, eliminar, feita, exibirFiltroCustom, criar_tarefas, refresh, datetime




main = Blueprint('main',__name__)

caminho_pasta_database = '/Users/stephanietrabalho/Desktop/proj/database'

@main.route('/')
def go_home():
    return exibirFiltroCustom(Tarefa, db)

# refresh

@main.route('/refresh')
def call_refresh():
    return refresh(Tarefa,db)

@main.route('/refresh0')
def call_refresh0():
    return refresh(Tarefa,db,classe_filter=0)

@main.route('/refreshAniversarios')
def call_refreshAniversarios():
    return refresh(Tarefa,db,classe_filter='aniversarios')


# filtros date
@main.route('/exibir_filtro_steph_min', methods=['GET'])
def exibirFiltroStephmin():
    return exibirFiltroCustom(Tarefa, db, owner='steph', filtrar_data_mais_proxima=True)


@main.route('/exibir_filtro_steph', methods=['GET'])
def exibirFiltroSteph():
    return exibirFiltroCustom(Tarefa, db, owner='steph')

@main.route('/exibir_filtro', methods=['GET'])
def do_filter():
    return exibirFiltroCustom(Tarefa, db, owner=None, filtrar_data_mais_proxima=True)


@main.route('/exibir_todas', methods=['GET'])
def exibir_todas():
    return exibirFiltroCustom(Tarefa, db)

# edit tarefa
@main.route('/tarefa-feita/<id>')
def tarefa_feita(id):
    return feita(Tarefa,db,id)

@main.route('/tarefa-adiar/<id>')
def tarefa_adiar(id):
    return adiar(Tarefa,db,id)


@main.route('/atualizar_tarefa/<int:id>', methods=['POST'])
def atualizar_tarefa(id):
    return editar(Tarefa,db,id)


@main.route('/editar_tarefa/<int:id>', methods=['GET'])
def editar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    return render_template('editar_tarefa.html', tarefa=tarefa)

# calendario
@main.route('/calendario', methods=['GET'])
def calendario():
    # Número total de tarefas a mostrar no calendário
    total_tarefas = 35
    hoje = datetime.utcnow().date()

    # Query das tarefas ordenadas por data_proxima
    tarefas_query = Tarefa.query.filter(or_(Tarefa.owner == 'steph', Tarefa.owner == 'ambos'),Tarefa.classe == 0).order_by(Tarefa.data_proxima.asc()).limit(total_tarefas).all()

    # Inicializar estrutura dos dias da semana
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    calendario_semanal = {dia: [] for dia in dias_da_semana}

    # Distribuir tarefas pelos dias da semana
    for i, tarefa in enumerate(tarefas_query):
        dia_index = i % 7  # Isso garante a distribuição uniforme
        dia_nome = dias_da_semana[dia_index]
        calendario_semanal[dia_nome].append(tarefa)

    # Passa o calendário_semanal para o template
    return render_template('calendario.html', calendario_semanal=calendario_semanal, datetime=datetime)

# eliminar tarefa

@main.route('/eliminar-tarefa/<id>')
def eliminar_tarefa(id):
    return eliminar(Tarefa,db,id)

# criar tarefas
    
@main.route('/criar-tarefa', methods=['POST'])
def criar_tarefa():
    return criar(Tarefa,db)

@main.cli.command("import-csv-birthdays") #flask import-csv-birthdays
def import_csv():
    name_csv_file = caminho_pasta_database + '/Livro6.csv'
    criar_tarefas(Tarefa, db,name_csv_file)

@main.cli.command("import-csv") #flask import-csv
def import_csv():
    name_csv_file = caminho_pasta_database + '/Livro4.csv'
    criar_tarefas(Tarefa, db,name_csv_file)
