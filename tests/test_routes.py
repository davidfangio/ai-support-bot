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
        chamada = {}

        class responder_teste:
            def __call__(self, mensagem, historico):
                chamada["mensagem"] = mensagem
                chamada["historico"] = historico.copy()
                return "Olá! Sou o Robbie."

        mock_responder.side_effect = responder_teste()

        resposta = client.post(
            "/chat",
            json={"mensagem": "Olá, Robbie!"}
        )

    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados["resposta"] == "Olá! Sou o Robbie."
    
    assert chamada["mensagem"] == "Olá, Robbie!"
    assert chamada["historico"] == []

def test_home():
    app = create_app()
    client = app.test_client()

    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.text == "AI Support Bot Online."

def test_conversa_nova_cria_conversation_id():
    app = create_app()
    client = app.test_client()

    with patch("app.routes.responder") as mock_responder:
        mock_responder.return_value = "Olá! Sou o Robbie."

        resposta = client.post(
            "/chat",
            json={"mensagem": "Olá, Robbie!"}
        )

        assert resposta.status_code == 200
        dados = resposta.get_json()
        assert "conversation_id" in dados
        assert dados["conversation_id"] 

def test_conversa_reutiliza_historico():
    app = create_app()
    client = app.test_client()

    with patch("app.routes.responder") as mock_responder:
        chamadas = []

        def responder_teste(mensagem, historico):
            chamadas.append({
                "mensagem": mensagem,
                "historico": historico.copy()
            })
            return "Resposta do Robbie."

        mock_responder.side_effect = responder_teste

        primeira = client.post(
            "/chat",
            json={
                "conversation_id": "teste-memoria",
                "mensagem": "Olá!"
            }
        )

        segunda = client.post(
            "/chat",
            json={
                "conversation_id": "teste-memoria",
                "mensagem": "Você lembra de mim?"
            }
        )

    assert chamadas[0]["historico"] == []

    assert chamadas[1]["historico"] == [
        "Cliente: Olá!",
        "Robbie: Resposta do Robbie."
    ]

def test_conversas_sao_isoladas():
    app = create_app()
    client = app.test_client()

    with patch("app.routes.responder") as mock_responder:
        chamadas = []

        def responder_teste(mensagem, historico):
            chamadas.append({
                "mensagem": mensagem,
                "historico": historico.copy()
            })
            return "Resposta do Robbie."

        mock_responder.side_effect = responder_teste

        client.post(
            "/chat",
            json={
                "conversation_id": "conversa-a",
                "mensagem": "Olá, sou o João."
            }
        )

        client.post(
            "/chat",
            json={
                "conversation_id": "conversa-b",
                "mensagem": "Olá, sou a Maria."
            }
        )

        client.post(
            "/chat",
            json={
                "conversation_id": "conversa-a",
                "mensagem": "Você lembra de mim?"
            }
        )

        client.post(
            "/chat",
            json={
                "conversation_id": "conversa-b",
                "mensagem": "E você lembra de mim?"
            }
        )

    assert chamadas[2]["historico"] == [
        "Cliente: Olá, sou o João.",
        "Robbie: Resposta do Robbie."
    ]

    assert chamadas[3]["historico"] == [
        "Cliente: Olá, sou a Maria.",
        "Robbie: Resposta do Robbie."
    ]

def test_historico_respeita_limite_de_10_entradas():
    app = create_app()
    client = app.test_client()

    with patch("app.routes.responder") as mock_responder:
        chamadas = []

        def responder_teste(mensagem, historico):
            chamadas.append(historico.copy())
            return f"Resposta para: {mensagem}"

        mock_responder.side_effect = responder_teste

        for i in range(6):
            client.post(
                "/chat",
                json={
                    "conversation_id": "teste-limite",
                    "mensagem": f"Mensagem {i}"
                }
            )

    assert len(chamadas[-1]) == 10