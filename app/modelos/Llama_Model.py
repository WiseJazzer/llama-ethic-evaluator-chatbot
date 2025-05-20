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
            f"Eres un experto en auditoría ambiental en México. Asesora al cliente basándote en la norma mexicana nmx-aa-162-scfi-2012 y en la LGEEPA "
            f"La consulta del clinete es:\n\n{text}\n\n"
            "Proporciona una retroalimentación detallada, acerca de los incentivos fiscales y el cumplimiento con la norma mexicana de auditoría ambiental\n"
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