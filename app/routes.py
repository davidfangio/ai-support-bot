from flask import Blueprint, request 

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

    return f"Robbie recebeu: {mensagem}"

    



            
