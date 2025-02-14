import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os

class EthicsChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot de Ética")
        self.root.configure(bg="#001f3f")  # Fondo azul marino oscuro para la ventana principal

        # Definir la ruta de la carpeta de assets
        assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')

        # Cargar y redimensionar imágenes
        logo1_path = os.path.join(assets_path, "logo-tecnm.png")
        logo2_path = os.path.join(assets_path, "logo-ittlahuac.png")
        logo3_path = os.path.join(assets_path, "logo-guardian.png")  # Añade la ruta del nuevo logo

        self.logo1 = Image.open(logo1_path)
        self.logo1 = self.logo1.resize((100, 100), Image.LANCZOS)  # Ajusta las dimensiones según sea necesario
        self.logo1 = ImageTk.PhotoImage(self.logo1)

        self.logo2 = Image.open(logo2_path)
        self.logo2 = self.logo2.resize((100, 100), Image.LANCZOS)  # Ajusta las dimensiones según sea necesario
        self.logo2 = ImageTk.PhotoImage(self.logo2)

        self.logo3 = Image.open(logo3_path)
        self.logo3 = self.logo3.resize((100, 100), Image.LANCZOS)  # Ajusta las dimensiones según sea necesario
        self.logo3 = ImageTk.PhotoImage(self.logo3)

        # Crear un marco para los logos con fondo blanco
        logo_frame = tk.Frame(root, bg="white")
        logo_frame.pack(fill="x")

        # Configurar las columnas del marco
        logo_frame.columnconfigure(0, weight=1)
        logo_frame.columnconfigure(1, weight=1)
        logo_frame.columnconfigure(2, weight=1)
        logo_frame.columnconfigure(3, weight=1)
        logo_frame.columnconfigure(4, weight=1)

        # Añadir logos al marco con fondo blanco
        self.logo1_label = tk.Label(logo_frame, image=self.logo1, bg="white")
        self.logo1_label.grid(row=0, column=0, padx=10, sticky="w")
        self.logo3_label = tk.Label(logo_frame, image=self.logo3, bg="white")
        self.logo3_label.grid(row=0, column=2, padx=10, sticky="n")  # Centra el nuevo logo
        self.logo2_label = tk.Label(logo_frame, image=self.logo2, bg="white")
        self.logo2_label.grid(row=0, column=4, padx=10, sticky="e")

        # Crear un marco para la entrada de datos con fondo azul marino oscuro
        input_frame = tk.Frame(root, bg="#001f3f")
        input_frame.pack(pady=10)

        # Lista de teorías éticas y palabras clave
        self.theories_list = ["Justo Medio", "Utilitarismo", "Imperativo Categórico", "Ética de la Liberación", "Sumak Kawsay"]
        self.keywords_dict = {
            "Justo Medio aristotélico": ["punto intermedio", "dos extremos viciosos", "entre los extremos viciosos"],
            "Utilitarismo": ["mayor felicidad", "mayor beneficio", "más beneficio", "a la mayoría"],
            "Imperativo Categórico kantiano": ["me gustaría que", "todos siempre hagan", "se vuelva ley universal", "es deseable"],
            "Ética de la Liberación de Dussel": ["vida digna", "sur global", "liberación de los oprimidos", "dignidad"],
            "Sumak Kawsay": ["equilibrio", "armonía", "buen vivir", "personas y el mundo"]
        }
        self.selected_theory = tk.StringVar()
        self.selected_theory.set(self.theories_list[0])  # Valor por defecto
        self.selected_theory.trace("w", self.update_keywords)

        # Crear widgets con fondo azul marino oscuro
        self.theories_label = tk.Label(input_frame, text="Teorías Éticas:", bg="#001f3f", fg="white")
        self.theories_label.grid(row=0, column=0, sticky="w")
        self.theories_menu = tk.OptionMenu(input_frame, self.selected_theory, *self.theories_list)
        self.theories_menu.config(bg="#001f3f", fg="white")
        self.theories_menu.grid(row=0, column=1)

        self.keywords_label = tk.Label(input_frame, text="Palabras Clave:", bg="#001f3f", fg="white")
        self.keywords_label.grid(row=1, column=0, sticky="w")
        self.keywords_entry = tk.Entry(input_frame, width=50, bg="black", fg="white")  # Fondo negro
        self.keywords_entry.grid(row=1, column=1)
        self.update_keywords()

        self.text_label = tk.Label(input_frame, text="Texto del Estudiante:", bg="#001f3f", fg="white")
        self.text_label.grid(row=2, column=0, sticky="w")
        self.text_entry = tk.Text(input_frame, width=50, height=10, bg="black", fg="white")  # Fondo negro
        self.text_entry.grid(row=2, column=1)

        # Crear un marco para los botones con fondo azul marino oscuro
        button_frame = tk.Frame(root, bg="#001f3f")
        button_frame.pack(pady=10)

        self.evaluate_button = tk.Button(button_frame, text="Evaluar", command=self.evaluate_text, bg="#001f3f", fg="white")
        self.evaluate_button.grid(row=0, column=0, padx=5)

        self.clear_button = tk.Button(button_frame, text="Limpiar", command=self.clear_fields, bg="#001f3f", fg="white")
        self.clear_button.grid(row=0, column=1, padx=5)

        # Crear un área de texto para mostrar la retroalimentación con fondo negro
        self.feedback_label = tk.Label(root, text="Retroalimentación:", bg="#001f3f", fg="white")
        self.feedback_label.pack()
        self.feedback_text = tk.Text(root, width=60, height=15, state=tk.DISABLED, bg="black", fg="white")  # Fondo negro
        self.feedback_text.pack()

    def update_keywords(self, *args):
        theory = self.selected_theory.get()
        keywords = ", ".join(self.keywords_dict.get(theory, []))
        self.keywords_entry.delete(0, tk.END)
        self.keywords_entry.insert(0, keywords)

    def evaluate_text(self):
        theory = self.selected_theory.get()
        keywords = self.keywords_entry.get().strip().split(',')
        text = self.text_entry.get("1.0", tk.END).strip()

        if not text:
            messagebox.showerror("Error", "El texto del estudiante es requerido.")
            return

        # Enviar datos al servidor Flask
        try:
            response = requests.post(
                'http://127.0.0.1:5000/evaluate',
                json={
                    'text': text,
                    'theory': theory,
                    'keywords': keywords
                }
            )
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            feedback = response.json().get('feedback', 'No se recibió retroalimentación.')
            self.display_feedback(feedback)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
        except ValueError:
            messagebox.showerror("Error", "La respuesta del servidor no es un JSON válido.")

    def display_feedback(self, feedback):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.insert(tk.END, feedback)
        self.feedback_text.config(state=tk.DISABLED)

    def clear_fields(self):
        self.selected_theory.set(self.theories_list[0])
        self.keywords_entry.delete(0, tk.END)
        self.text_entry.delete("1.0", tk.END)
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = EthicsChatbotGUI(root)
    root.mainloop()