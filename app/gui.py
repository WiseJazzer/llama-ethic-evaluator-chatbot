import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os

class GreenAuditChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot de GreenAudit")
        self.root.configure(bg="#316f86")  # Fondo azul marino oscuro para la ventana principal

        # Definir la ruta de la carpeta de assets
        assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')

        # Cargar y redimensionar el nuevo logo
        logo_path = os.path.join(assets_path, "Green_Audit_logo.png")
        self.logo = Image.open(logo_path)
        self.logo = self.logo.resize((100, 100), Image.LANCZOS)  # Ajusta las dimensiones según sea necesario
        self.logo = ImageTk.PhotoImage(self.logo)

        # Crear un marco para el logo con fondo blanco
        logo_frame = tk.Frame(root, bg="#cfd3da") # Fondo gris claro
        logo_frame.pack(fill="x", anchor="w")  # Alinea el marco a la izquierda

        # Añadir el logo al marco
        self.logo_label = tk.Label(logo_frame, image=self.logo, bg="#cfd3da")
        self.logo_label.pack(side="left", padx=10, pady=10)  # Posiciona el logo en la esquina superior izquierda

        # Crear un marco para la entrada de datos con fondo azul marino oscuro
        input_frame = tk.Frame(root, bg="#316f86")
        input_frame.pack(pady=10, fill="both", expand=True)

        # Etiqueta y cuadro de texto para la consulta
        self.text_label = tk.Label(input_frame, text="Consulta:", bg="#316f86", fg="white")
        self.text_label.pack(anchor="w", padx=10, pady=(0, 5))
        self.text_entry = tk.Text(input_frame, height=10, bg="black", fg="white")
        self.text_entry.pack(fill="both", expand=True, padx=10)

        # Crear un marco para los botones con fondo azul marino oscuro
        button_frame = tk.Frame(root, bg="#316f86")
        button_frame.pack(pady=10)

        self.evaluate_button = tk.Button(
            button_frame,
            text="Enviar",
            command=self.evaluate_text,
            bg="white",
            fg="black",
            highlightbackground="white"
        )
        self.evaluate_button.grid(row=0, column=0, padx=5)

        self.clear_button = tk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear_fields,
            bg="white",
            fg="black",
            highlightbackground="white"
        )
        self.clear_button.grid(row=0, column=1, padx=5)

        # Área de texto para mostrar la retroalimentación
        self.feedback_label = tk.Label(root, text="Asesoría de Green Audit:", bg="#316f86", fg="white")
        self.feedback_label.pack(anchor="w", padx=10)

        self.feedback_text = tk.Text(root, height=15, state=tk.DISABLED, bg="black", fg="white")
        self.feedback_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def evaluate_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()

        if not text:
            messagebox.showerror("Error", "El texto de la consulta es requerido.")
            return

        # Enviar datos al servidor Flask
        try:
            response = requests.post(
                'http://127.0.0.1:5000/evaluate',
                json={'text': text,}
            )
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            feedback = response.json().get('feedback', 'No se recibió la asesoría.')
            self.display_feedback(feedback)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
        except ValueError:
            messagebox.showerror("Error", "La respuesta del servidor no es un JSON válido.")

    def display_feedback(self, feedback):
        """Muestra la asesoría en el área de texto."""
        self.feedback_text.config(state=tk.NORMAL)  # Habilitar edición temporalmente
        self.feedback_text.delete("1.0", tk.END)  # Limpiar el área de texto
        self.feedback_text.insert(tk.END, feedback)  # Insertar la retroalimentación
        self.feedback_text.config(state=tk.DISABLED)  # Deshabilitar edición nuevamente

    def clear_fields(self):
        self.text_entry.delete("1.0", tk.END)
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = GreenAuditChatbotGUI(root)
    root.mainloop()