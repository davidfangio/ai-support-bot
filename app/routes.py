from flask import Blueprint, request 
from app.chatbot import responder 

main = Blueprint("main", __name__)

@main.route("/")
def home ():
    return "AI Support Bot Online."

@main.route("/chat", methods=["POST"])
def chat():
    dados = request.json

    if not dados or "mensagem" not in dados:
        return "Robbie precisa de uma mensagem para responder.", 400

    mensagem = dados["mensagem"]

    if not isinstance(mensagem, str) or not mensagem.strip():
        return "Robbie precisa de uma mensagem válida para responder.", 400

    if len(mensagem) > 4000:
        return "A mensagem excede o limite de 4000 caracteres.", 400
    
    resposta = responder(mensagem)

    return resposta




    



            
