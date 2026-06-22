"""
Testes de CRUD do storage (SQLite).

Isolamento: o módulo `src.storage.database` lê DB_PATH na importação e cria as
tabelas nesse momento. Por isso a fixture define DB_PATH para um arquivo
temporário (tmp_path do pytest) ANTES de importar os módulos de storage, e os
importa de forma controlada dentro da própria fixture. Cada teste recebe um
banco limpo, sem tocar o data/jarvis.db real.
"""

import importlib
import sys

import pytest


@pytest.fixture
def storage(tmp_path, monkeypatch):
    """
    Prepara um storage isolado num banco temporário e devolve os módulos
    (agenda, tarefas) já apontando para esse banco.
    """
    db_file = tmp_path / "test_jarvis.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    # Remove módulos já carregados para forçar releitura de DB_PATH na importação
    for mod in ["src.storage.database", "src.storage.agenda", "src.storage.tarefas"]:
        sys.modules.pop(mod, None)

    database = importlib.import_module("src.storage.database")
    agenda   = importlib.import_module("src.storage.agenda")
    tarefas  = importlib.import_module("src.storage.tarefas")

    # Garante o esquema no banco temporário
    database.criar_tabelas()

    return agenda, tarefas


# ── Agenda ────────────────────────────────────────────────────────────────────

def test_adicionar_evento_retorna_dict_completo(storage):
    agenda, _ = storage
    evento = agenda.adicionar_evento(
        titulo="Prova de Cálculo", data="2026-06-20", hora="14:00", tipo="prova"
    )
    assert evento["id"] > 0
    assert evento["titulo"] == "Prova de Cálculo"
    assert evento["data"] == "2026-06-20"
    assert evento["tipo"] == "prova"


def test_buscar_evento_por_id(storage):
    agenda, _ = storage
    criado = agenda.adicionar_evento(titulo="Aula de IA", data="2026-06-15", tipo="aula")
    encontrado = agenda.buscar_evento_por_id(criado["id"])
    assert encontrado is not None
    assert encontrado["titulo"] == "Aula de IA"


def test_listar_eventos_por_data_filtra_corretamente(storage):
    agenda, _ = storage
    agenda.adicionar_evento(titulo="Evento A", data="2026-06-10")
    agenda.adicionar_evento(titulo="Evento B", data="2026-06-11")
    do_dia = agenda.listar_eventos_por_data("2026-06-10")
    titulos = [e["titulo"] for e in do_dia]
    assert "Evento A" in titulos
    assert "Evento B" not in titulos


def test_remover_evento(storage):
    agenda, _ = storage
    criado = agenda.adicionar_evento(titulo="Temporário", data="2026-06-12")
    assert agenda.remover_evento(criado["id"]) is True
    assert agenda.buscar_evento_por_id(criado["id"]) is None


# ── Tarefas ───────────────────────────────────────────────────────────────────

def test_adicionar_tarefa_com_prioridade(storage):
    _, tarefas = storage
    tarefa = tarefas.adicionar_tarefa(descricao="Estudar grafos", prioridade="alta")
    assert tarefa["id"] > 0
    assert tarefa["descricao"] == "Estudar grafos"
    assert tarefa["prioridade"] == "alta"
    assert tarefa["concluida"] == 0


def test_listar_pendentes_traz_tarefa_nova(storage):
    _, tarefas = storage
    tarefas.adicionar_tarefa(descricao="Ler capítulo 3")
    pendentes = tarefas.listar_tarefas_pendentes()
    assert any(t["descricao"] == "Ler capítulo 3" for t in pendentes)


def test_concluir_tarefa_muda_estado(storage):
    _, tarefas = storage
    t = tarefas.adicionar_tarefa(descricao="Entregar relatório")
    tarefas.concluir_tarefa(t["id"])

    pendentes = [x["descricao"] for x in tarefas.listar_tarefas_pendentes()]
    concluidas = [x["descricao"] for x in tarefas.listar_tarefas_concluidas()]

    assert "Entregar relatório" not in pendentes
    assert "Entregar relatório" in concluidas


def test_remover_tarefa(storage):
    _, tarefas = storage
    t = tarefas.adicionar_tarefa(descricao="Tarefa descartável")
    assert tarefas.remover_tarefa(t["id"]) is True
    assert tarefas.buscar_tarefa_por_id(t["id"]) is None
