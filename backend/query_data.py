from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Voici un extrait de documents techniques. Réponds uniquement à la question si tu trouves l'information dans ce contexte.

{context}

---

Si tu ne trouves pas de réponse claire, réponds : "Je ne trouve pas d'information fiable à ce sujet dans les documents fournis."

Question : {question}
"""

def query_rag(query_text: str) -> str:
    # Préparation de la base vectorielle
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    # Recherche de similarité
    results = db.similarity_search_with_score(query_text, k=10)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    for doc, score in results:
        print(f"🔍 [score={score:.3f}] {doc.metadata.get('source', '')} - {doc.page_content[:80]}...")

    # Préparation du prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Lancement du modèle
    model = Ollama(model="MISTRALCHATBOT")
    response_text = model.invoke(prompt)

    return response_text
