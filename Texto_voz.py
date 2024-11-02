import nltk
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import os

# Descargar el paquete de tokenizer de nltk
nltk.download('punkt')

# Función para extraer texto del artículo usando requests y BeautifulSoup
def extract_article_text(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error al acceder a la URL: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Intentar extraer texto de etiquetas comunes de artículos
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        
        if not text.strip():
            raise Exception("No se pudo extraer texto del artículo.")
        
        return text
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al extraer el artículo: {str(e)}")
        return None

# Función para convertir el artículo a audio
def article_to_audio(url, output_filename='article_audio.mp3'):
    text = extract_article_text(url)
    if not text:
        return
    
    try:
        # Convertir el texto a voz usando gTTS
        tts = gTTS(text=text, lang='es')  # Cambiar 'es' a 'en' o cualquier idioma soportado
        
        # Guardar el archivo de audio
        tts.save(output_filename)
        
        # Verificar si el archivo se ha guardado correctamente
        if os.path.exists(output_filename):
            messagebox.showinfo("Éxito", f"Audio guardado como {output_filename}")
        else:
            raise Exception("No se pudo guardar el archivo de audio.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Función para manejar la acción del botón
def convert_article():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Por favor, ingrese una URL.")
        return
    
    output_filename = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                   filetypes=[("MP3 files", "*.mp3")])
    if output_filename:
        article_to_audio(url, output_filename)

# Crear la ventana principal
root = tk.Tk()
root.title("Artículo a Audio MP3")

# Etiqueta y entrada de URL
tk.Label(root, text="Ingrese la URL del artículo:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Botón para convertir
convert_button = tk.Button(root, text="Convertir a MP3", command=convert_article)
convert_button.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()
