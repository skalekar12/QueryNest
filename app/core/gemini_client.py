from dotenv import load_dotenv
import os
import google.generativeai as genai

# 🔹 Load environment variables
load_dotenv()

# 🔹 Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 🔹 Load model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_response(prompt: str) -> str:
    """
    Generate response from Gemini using a prepared prompt

    Args:
        prompt (str): fully formatted prompt (from RAG pipeline)

    Returns:
        str: generated answer
    """

    try:
        response = model.generate_content(prompt)

        # ✅ Safe extraction
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        # fallback if structure changes
        if hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            return "".join([p.text for p in parts if hasattr(p, "text")]).strip()

        return "No response generated."

    except Exception as e:
        print("❌ Gemini Error:", str(e))
        return "Error generating response."