from tkinter import messagebox
from PIL import Image, ImageTk
import ollama  # Add this import statement

class LlamaModel:
    def __init__(self):
        # No se necesita una clave API para Ollama
        pass

    def evaluate_ethical_judgment(self, text, theories, keywords):
        # Prepara el prompt para Llama 3.2:1b
        prompt = (
            f"Eres un experto en ética. Evalúa el siguiente juicio ético basado en la teoría {', '.join(theories)} "
            f"y las palabras clave {', '.join(keywords)}. El texto del estudiante es:\n\n{text}\n\n"
            "Proporciona una retroalimentación detallada, incluyendo:\n"
            "1. Revisa si el juicio ético incluye, ya sea de manera literal o parafraseada, las palabras clave de la teoría ética que está usando.\n"
            "2. Si es congruente su fundamentación con el juicio de valor que hace de la acción.\n"
            "3. Retroalimentación acerca de si su juicio ético cumple con estos 2 criterios."
        )

        # Envía el prompt a Llama 3.2:1b
        try:
            response = ollama.generate(
                model="llama3.2:1b",  # Usa el modelo Llama 3.2:1b
                prompt=prompt,
                options={
                    "temperature": 0.3,  # Controla la creatividad (0 = preciso, 1 = creativo)
                    "max_tokens": 500    # Limita la longitud de la respuesta
                }
            )
            feedback = response["response"]
            return feedback
        except Exception as e:
            return f"Error al conectar con Llama 3.2:1b: {e}"