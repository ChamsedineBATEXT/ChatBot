import pytest
from query_data import query_rag
from langchain_community.llms.ollama import Ollama


# Prompt d'évaluation LLM
EVAL_PROMPT = """
Tu es un évaluateur rigoureux. On te donne une réponse attendue et une réponse réelle à une même question.

Ta mission est de dire si la réponse réelle fournit bien l'information demandée, même si elle est formulée différemment.

Expected Response: {expected_response}
Actual Response: {actual_response}
---
Réponds uniquement par 'true' ou 'false'. Est-ce que la réponse réelle correspond bien à ce qui était attendu ?
"""

# Initialisation du modèle LLM via Ollama
llm = Ollama(model="MISTRALCHATBOT")

# Fonction d'évaluation avec LLM
def validate_with_llm(expected, actual):
    prompt = EVAL_PROMPT.format(expected_response=expected, actual_response=actual)
    result = llm.invoke(prompt).strip().lower()
    print(f"\n🧪 Prompt LLM :\n{prompt}\n📤 Résultat LLM : {result}")
    if "true" in result:
        return True
    elif "false" in result:
        return False
    raise ValueError("Réponse LLM invalide (ni true ni false)")

# --------- ✅ TESTS POSITIFS ---------

@pytest.mark.parametrize("question, expected_response", [
    (
        "Quel type d’extincteur faut-il pour une station-service avec carburant liquide ?", 
        "Un extincteur de 9kg à poudre est requis pour chaque ilot de distribution."
    ),
    (
        "Quelle est la portée d’un jet droit avec un RIA DN25-30 ?", 
        "Le jet droit atteint 13,5 mètres pour un RIA DN25-30."
    ),
    (
        "Quels additifs ne peuvent pas éteindre un feu de solvant polaire ?", 
        "SC-6, VALEXT, ECOPOL, FFX Compact et FFX Booster A ne sont pas efficaces contre les feux de solvant polaire."
    ),
])
def test_llm_response_true(question, expected_response):
    actual_response = query_rag(question)
    assert validate_with_llm(expected_response, actual_response)


# --------- ❌ TESTS NÉGATIFS ---------

@pytest.mark.parametrize("question, wrong_expectation", [
    (
        "Un extincteur à mousse est-il suffisant pour le carburant GPL ?", 
        "Oui, un extincteur à mousse suffit pour le carburant GPL."
    ),
    (
        "Quelle est la portée d’un jet droit avec un RIA DN10-90 ?", 
        "Il atteint 25 mètres."
    ),
    (
        "Peut-on utiliser les additifs SC-6 pour éteindre un feu d’essence ?", 
        "Oui, ils sont parfaitement efficaces sur les feux de solvants polaires."
    ),
])
def test_llm_response_false(question, wrong_expectation):
    actual_response = query_rag(question)
    assert not validate_with_llm(wrong_expectation, actual_response)
