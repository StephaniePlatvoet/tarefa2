from flask import request, redirect, url_for
from datetime import datetime
from dateutil.rrule import SU
from funcoes import calcular_proxima_data, criarImport

def criar(task_class,db):

    data_primeira_vez_str = datetime.strptime(request.form['data_primeira_vez'])
    
    nova_tarefa = task_class(
    descricao=request.form['descricao_tarefa'],
    feita=False,
    data_primeira_vez = datetime.strptime(data_primeira_vez_str, '%Y-%m-%d') if data_primeira_vez_str else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
    intervalo_repeticao_mode=request.form.get('intervalo_repeticao_mode'),
    intervalo_repeticao_value=request.form.get('intervalo_repeticao_value'),
    proximo_domingo=bool(request.form.get('intervalo_repeticao_next_sunday')),
    data_proxima=calcular_proxima_data(request.form['data_primeira_vez'],intervalo_repeticao_next_sunday,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = True),
    data_proxima_seguinte=calcular_proxima_data(data_primeira_vez,intervalo_repeticao_next_sunday,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = False),
    classe=request.form.get('classe'),
    notas=request.form['notas'],
    ordem=custom_order(request.form['ordem']),
    owner=request.form['owner']
    )

    db.session.add(nova_tarefa)
    db.session.commit()
    return redirect(url_for('go_home') + '#content')
