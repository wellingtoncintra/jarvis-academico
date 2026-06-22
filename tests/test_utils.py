"""
Testes do utilitário de extração de JSON (src.utils.extrair_json).

Cobre os formatos que o Gemma costuma produzir: JSON puro, JSON dentro de
cercas markdown, JSON embutido em texto, e respostas sem JSON válido.
"""

from src.utils import extrair_json


def test_json_puro():
    out = extrair_json('{"tool": "consultar_agenda", "args": {"periodo": "hoje"}}')
    assert out == {"tool": "consultar_agenda", "args": {"periodo": "hoje"}}


def test_json_com_cerca_markdown():
    texto = '```json\n{"pergunta": "O que é AFD?", "gabarito": "Autômato Finito Determinístico"}\n```'
    out = extrair_json(texto)
    assert out["pergunta"] == "O que é AFD?"
    assert out["gabarito"] == "Autômato Finito Determinístico"


def test_json_com_cerca_sem_label():
    texto = '```\n{"x": 1}\n```'
    assert extrair_json(texto) == {"x": 1}


def test_json_embutido_em_texto():
    texto = 'Claro! Aqui está o resultado: {"tool": "listar", "args": {}} — espero ter ajudado.'
    out = extrair_json(texto)
    assert out == {"tool": "listar", "args": {}}


def test_texto_sem_json_retorna_none():
    assert extrair_json("Não consegui gerar uma resposta estruturada.") is None


def test_texto_vazio_retorna_none():
    assert extrair_json("") is None
    assert extrair_json(None) is None


def test_json_invalido_retorna_none():
    # Chaves presentes mas conteúdo malformado
    assert extrair_json('{"tool": "x", "args": }') is None


def test_retorna_none_para_json_que_nao_e_objeto():
    # Uma lista é JSON válido, mas extrair_json só retorna dict
    assert extrair_json("[1, 2, 3]") is None
