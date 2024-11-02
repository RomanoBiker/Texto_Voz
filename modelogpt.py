import nltk
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup

# Descargar el paquete de tokenizer de nltk
nltk.download('punkt')

# Función para extraer texto del artículo usando requests y BeautifulSoup
def extract_article_text(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error al acceder a la URL: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        
        if not text.strip():
            raise Exception("No se pudo extraer texto del artículo.")
        
        return text
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al extraer el artículo: {str(e)}")
        return None

# Función para dividir el texto en partes más pequeñas
def split_text(text, max_chars=5000):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []

    current_length = 0
    for sentence in sentences:
        if current_length + len(sentence) > max_chars:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = len(sentence)
        else:
            current_chunk.append(sentence)
            current_length += len(sentence)

    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

# Función para convertir el artículo a audio en partes
def article_to_audio(url, output_filename='article_audio.mp3'):
    text = extract_article_text(url)
    if not text:
        return

    try:
        chunks = split_text(text)
        audio_parts = []

        # Crear y guardar múltiples partes de audio
        for i, chunk in enumerate(chunks):
            tts = gTTS(text=chunk, lang='es')
            part_filename = f"{output_filename}_part_{i}.mp3"
            tts.save(part_filename)
            audio_parts.append(part_filename)

        messagebox.showinfo("Éxito", f"Audio guardado en {len(audio_parts)} partes.")
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
