from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def responder(mensagem):
    return f"Robbie recebeu: {mensagem}"