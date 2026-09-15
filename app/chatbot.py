from dotenv import load_dotenv
from openai import OpenAI
from app.brain import carregar_cerebro

from app.knowledge_loader import carregar_documentos, dividir_documentos
from app.embeddings import gerar_embeddings
from app.vector_store import criar_indice
from app.retriever import criar_retriever, buscar

load_dotenv()

cliente = OpenAI()

documentos = carregar_documentos()
chunks = dividir_documentos(documentos)

embeddings = gerar_embeddings(chunks)

indice = criar_indice(embeddings)

retriever = criar_retriever(indice, chunks)
cerebro = carregar_cerebro()

def montar_contexto(mensagem, resultados):
    contexto = []

    contexto.append("=== CÉREBRO DO ROBBIE ===")
    contexto.append(cerebro)

    contexto.append("\n=== INFORMAÇÕES DA NOVASHOP ===")

    for resultado in resultados:
        contexto.append(resultado["chunk"].page_content)

    contexto.append("\n=== PERGUNTA DO CLIENTE ===")
    contexto.append(mensagem)

    return "\n\n".join(contexto)

def montar_prompt(mensagem, resultados):
    contexto = montar_contexto(mensagem, resultados)

    prompt = f"""
Você é Robbie, assistente virtual oficial da NovaShop.

Siga rigorosamente as regras do seu cérebro e utilize apenas as informações disponíveis no contexto fornecido.

NA base de conhecimento da NovaShop é sua única fonte de verdade.
Seu conhecimento prévio ou conhecimento geral do mundo não deve ser usado para responder ao cliente.
Responda somente quando a informação necessária estiver sustentada pelo contexto da NovaShop fornecido neste prompt.
Se a resposta não estiver presente ou não puder ser sustentada pelo contexto, não tente completar a resposta usando conhecimento externo. Informe que não possui informação suficiente e siga as regras de escalonamento do seu cérebro.
Nunca invente informações.
Nunca afirme que uma ação foi realizada se ela não tiver sido executada por uma ferramenta.
Se as informações disponíveis não forem suficientes para responder com segurança, seja transparente e siga as regras de escalonamento para atendimento humano.

Responda diretamente à pergunta do cliente, de forma clara, cordial, objetiva e humana.

Quando falar sobre garantia, nunca generalize o prazo. Identifique primeiro a categoria do produto e aplique exatamente o prazo correspondente definido no cérebro do Robbie. Nunca diga que todos os eletrônicos possuem 12 meses de garantia. Acessórios possuem 6 meses, enquanto smartphones, notebooks, headphones, teclados e monitores possuem 12 meses de garantia contratual.

=== CONTEXTO ===

{contexto}

=== FIM DO CONTEXTO ===
"""

    return prompt


def responder(mensagem):
    resultados = buscar(retriever, mensagem, k=3)
    prompt = montar_prompt(mensagem, resultados)

    resposta = cliente.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return resposta.output_text
