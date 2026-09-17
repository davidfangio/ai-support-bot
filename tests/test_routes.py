from app import create_app
from unittest.mock import patch


def test_chat_sem_mensagem():
    app = create_app()
    client = app.test_client()

    resposta = client.post("/chat", json={})

    assert resposta.status_code == 400
    assert resposta.text == "Robbie precisa de uma mensagem para responder."

def test_chat_mensagem_vazia():
    app = create_app()
    client = app.test_client()

    resposta = client.post("/chat", json={"mensagem": ""})

    assert resposta.status_code == 400
    assert resposta.text == "Robbie precisa de uma mensagem válida para responder."

def test_chat_mensagem_nao_e_string():
    app = create_app()
    client = app.test_client()

    resposta = client.post("/chat", json={"mensagem": 123})

    assert resposta.status_code == 400
    assert resposta.text == "Robbie precisa de uma mensagem válida para responder."

def test_chat_mensagem_muito_longa():
    app = create_app()
    client = app.test_client()

    mensagem = "a" * 4001

    resposta = client.post("/chat", json={"mensagem": mensagem})

    assert resposta.status_code == 400
    assert resposta.text == "A mensagem excede o limite de 4000 caracteres."

def test_chat_mensagem_valida():
    app = create_app()
    client = app.test_client()

    with patch("app.routes.responder") as mock_responder:
        mock_responder.return_value = "Olá! Sou o Robbie."

        resposta = client.post(
            "/chat",
            json={"mensagem": "Olá, Robbie!"}
        )

    assert resposta.status_code == 200
    assert resposta.text == "Olá! Sou o Robbie."
    mock_responder.assert_called_once_with("Olá, Robbie!")

def test_home():
    app = create_app()
    client = app.test_client()

    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.text == "AI Support Bot Online."