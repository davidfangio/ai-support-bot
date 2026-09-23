from flask import Blueprint, request, render_template
from app.chatbot import responder 
import uuid 

conversas = {}

main = Blueprint("main", __name__)

@main.route("/")
def home ():
    return render_template("chat.html")

@main.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json(silent=True)

    if not dados or "mensagem" not in dados:
        return "Robbie precisa de uma mensagem para responder.", 400

    mensagem = dados["mensagem"]

    if not isinstance(mensagem, str) or not mensagem.strip():
        return "Robbie precisa de uma mensagem válida para responder.", 400

    if len(mensagem) > 4000:
        return "A mensagem excede o limite de 4000 caracteres.", 400

    conversation_id = dados.get("conversation_id") or str(uuid.uuid4())

    try:
        uuid.UUID(conversation_id)
    except (ValueError, AttributeError, TypeError):
        return "conversation_id inválido.", 400

    if conversation_id not in conversas:
        conversas[conversation_id] = []

    historico = conversas[conversation_id]

    resposta = responder(mensagem, historico=historico)

    historico.append(f"Cliente: {mensagem}")
    historico.append(f"Robbie: {resposta}")

    historico[:] = historico[-10:]

    return {
        "conversation_id": conversation_id,
        "resposta": resposta,
    }




    



            
