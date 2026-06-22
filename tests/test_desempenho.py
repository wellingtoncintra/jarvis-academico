"""
Testes da persistência de desempenho do Active Recall (src.storage.desempenho).

Isolamento idêntico ao test_storage: DB_PATH aponta para um arquivo temporário
definido ANTES de importar os módulos de storage.
"""

import importlib
import sys

import pytest


@pytest.fixture
def desempenho(tmp_path, monkeypatch):
    db_file = tmp_path / "test_jarvis.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    for mod in ["src.storage.database", "src.storage.desempenho"]:
        sys.modules.pop(mod, None)

    database = importlib.import_module("src.storage.database")
    desempenho = importlib.import_module("src.storage.desempenho")
    database.criar_tabelas()
    return desempenho


def test_registrar_tentativa_retorna_registro(desempenho):
    reg = desempenho.registrar_tentativa("Autômatos", "correta")
    assert reg["id"] > 0
    assert reg["topico"] == "Autômatos"
    assert reg["classificacao"] == "correta"


def test_topico_vazio_vira_geral(desempenho):
    reg = desempenho.registrar_tentativa("", "incorreta")
    assert reg["topico"] == "geral"


def test_classificacao_invalida_vira_incorreta(desempenho):
    reg = desempenho.registrar_tentativa("X", "qualquer-coisa")
    assert reg["classificacao"] == "incorreta"


def test_total_tentativas(desempenho):
    assert desempenho.total_tentativas() == 0
    desempenho.registrar_tentativa("A", "correta")
    desempenho.registrar_tentativa("B", "parcial")
    assert desempenho.total_tentativas() == 2


def test_resumo_agrega_e_calcula_aproveitamento(desempenho):
    # Tópico "Gramáticas": 1 correta + 1 parcial + 0 incorreta → (1 + 0.5)/2 = 75%
    desempenho.registrar_tentativa("Gramáticas", "correta")
    desempenho.registrar_tentativa("Gramáticas", "parcial")
    resumo = desempenho.resumo_por_topico()
    gram = next(r for r in resumo if r["topico"] == "Gramáticas")
    assert gram["total"] == 2
    assert gram["corretas"] == 1
    assert gram["parciais"] == 1
    assert gram["aproveitamento"] == 75.0


def test_resumo_ordena_mais_dificeis_primeiro(desempenho):
    # "Facil": 100%; "Dificil": 0% → Dificil deve vir primeiro
    desempenho.registrar_tentativa("Facil", "correta")
    desempenho.registrar_tentativa("Dificil", "incorreta")
    resumo = desempenho.resumo_por_topico()
    assert resumo[0]["topico"] == "Dificil"
    assert resumo[-1]["topico"] == "Facil"


def test_limpar_desempenho(desempenho):
    desempenho.registrar_tentativa("A", "correta")
    assert desempenho.total_tentativas() == 1
    desempenho.limpar_desempenho()
    assert desempenho.total_tentativas() == 0
