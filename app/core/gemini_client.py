from dotenv import load_dotenv
import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.services.model_service.pagers import ListModelsPager

# 🔹 Load environment variables
load_dotenv()

# 🔹 Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def list_available_models():
    models = genai.list_models()

    for m in models:
        print(m.name)
list_available_models()
# 🔹 Load model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_response(query: str, context: str) -> str:
    """
    Generate answer using Gemini based on retrieved context

    Args:
        query (str): user question
        context (str): formatted retrieved chunks

    Returns:
        str: final answer
    """

    prompt = f"""
You are a helpful study assistant.

Use ONLY the provided context to answer the question.

If the answer is not in the context, say:
"I don't know based on the provided documents."

If the context is messy or broken, intelligently reconstruct the meaning.

---------------------
Context:
{context}
---------------------

Question:
{query}

Answer:
"""

    try:
        response = model.generate_content(prompt)

        if response.text:
            return response.text.strip()
        else:
            return "No response generated."

    except Exception as e:
        return f"Error generating response: {str(e)}"