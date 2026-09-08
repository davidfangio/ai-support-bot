from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


pdf = Path("knowledge/NovaShop_Base.pdf")

loader = PyPDFLoader(str(pdf))
documentos = loader.load()

print("=== TEXTO BRUTO DA PRIMEIRA PÁGINA ===\n")
print(documentos[0].page_content)