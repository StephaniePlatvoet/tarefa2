#extentions.py
from .app_files.adiar import adiar
from .app_files.criar import criar
from .app_files.editar import editar
from .app_files.eliminar import eliminar
from .app_files.feita import feita
from .app_files.filtro import exibirFiltroCustom
from .app_files.importCSV import criar_tarefas
from .app_files.refresh import refresh
from datetime import datetime



from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

