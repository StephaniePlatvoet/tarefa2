from flask import request, url_for, redirect, flash
from datetime import datetime

def editar(Tarefa, db, id):
    tarefa = Tarefa.query.get_or_404(id)
    if tarefa:
        # Lista de campos a serem atualizados
        campos = ['descricao', 'feita', 'notas', 'classe', 'ordem', 'data_primeira_vez', 'data_proxima', 'data_proxima_seguinte', 'intervalo_repeticao_mode', 'intervalo_repeticao_value', 'proximo_domingo', 'owner']
        
        # Mapeamento de campos booleanos e datetime
        campos_booleanos = ['feita', 'proximo_domingo']
        campos_datetime = ['data_primeira_vez', 'data_proxima', 'data_proxima_seguinte']
        
        for campo in campos:
            valor_formulario = request.form.get(campo)
            if campo in campos_booleanos:
                valor_formulario = campo in request.form
            elif campo in campos_datetime and valor_formulario:
                valor_formulario = datetime.strptime(valor_formulario, '%Y-%m-%d')
            
            valor_atual = getattr(tarefa, campo)
            if valor_formulario != valor_atual:
                setattr(tarefa, campo, valor_formulario)

        tarefa.data_alteracao = datetime.utcnow()

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


        return redirect(url_for('editar_tarefa', id=id))
    else:
        flash('Tarefa não encontrada.', 'error')
        return redirect(url_for('index'))  # Assumindo que você tem uma rota 'index'
