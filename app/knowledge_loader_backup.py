from pathlib import Path
import re

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def limpar_texto(texto):
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def carregar_documentos():
    arquivos = [
        KNOWLEDGE_DIR / "NovaShop_Base.txt",
    ]

    documentos = []

    for arquivo in arquivos:
        loader = TextLoader(
            str(arquivo),
            encoding="utf-8",
        )
        documentos.extend(loader.load())

    for documento in documentos:
        documento.page_content = limpar_texto(documento.page_content)

    return documentos


def dividir_documentos(documentos):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
        keep_separator=True,
    )

    return splitter.split_documents(documentos)