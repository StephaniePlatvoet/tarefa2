from flask import request, url_for, redirect, flash
from datetime import datetime

def editar(Tarefa, db, id):
    tarefa = Tarefa.query.get_or_404(id)
    if tarefa:
        # Atualizar os campos da tarefa com os valores recebidos do formulário
        tarefa.descricao = request.form.get('descricao')
        tarefa.feita = 'feita' in request.form
        tarefa.notas = request.form.get('notas')
        tarefa.classe = request.form.get('classe')
        tarefa.ordem = request.form.get('ordem', type=int)
        tarefa.data_alteracao = datetime.utcnow()

        # Atualizar campos adicionais conforme necessário
        intervalo_repeticao_mode = request.form.get('intervalo_repeticao_mode')
        intervalo_repeticao_value = request.form.get('intervalo_repeticao_value')
        intervalo_repeticao_next_sunday = request.form.get('intervalo_repeticao_next_sunday')
        data_primeira_vez_str = request.form.get('data_primeira_vez')
        data_primeira_vez = datetime.strptime(data_primeira_vez_str, '%Y-%m-%d') if data_primeira_vez_str else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        tarefa.intervalo_repeticao_mode = intervalo_repeticao_mode
        tarefa.intervalo_repeticao_value = intervalo_repeticao_value
        tarefa.proximo_domingo = bool(intervalo_repeticao_next_sunday)
        tarefa.data_primeira_vez = data_primeira_vez

        # Recalcular as datas de repetição, se necessário
        tarefa.data_proxima = calcular_proxima_data(data_primeira_vez, intervalo_repeticao_next_sunday, intervalo_repeticao_value, intervalo_repeticao_mode, primeiraVez=True)
        tarefa.data_proxima_seguinte = calcular_proxima_data(data_primeira_vez, intervalo_repeticao_next_sunday, intervalo_repeticao_value, intervalo_repeticao_mode, primeiraVez=False)

        try:
            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar tarefa: {e}', 'error')

        return redirect(url_for('editar_tarefa', id=id))
    else:
        flash('Tarefa não encontrada.', 'error')
        return redirect(url_for('index'))  # Assumindo que você tem uma rota 'index'
