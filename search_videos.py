import speech_recognition as sr
from transformers import pipeline
import tkinter as tk
import customtkinter as ctk
import threading
import requests
import webbrowser  # Para abrir os links no navegador

print("Iniciando reconhecimento de voz...\nPara finalizar, pressione Ctrl+C no terminal, ou feche a janela pelo programa.")
# Inicializa o reconhecedor de fala
recognizer = sr.Recognizer()

# Função para buscar vídeos no YouTube
def buscar_videos_youtube(prompt):
    query = prompt.replace(" ", "+")
    api_key = "AIzaSyCyxXROEnVVLLSRmb04or9-JsxJsJ9ZDt4"  # Substitua pela sua chave da API do YouTube
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&key={api_key}&maxResults=3&q={query}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        links = []
        for item in data['items']:
            links.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")
        return links
    else:
        return ["Erro ao acessar a API do YouTube."]

# Função para abrir o link no navegador
def abrir_link(url):
    webbrowser.open(url)

# Função para reconhecer e processar a fala
def reconhecer_fala():
    idioma = idioma_combobox.get()
    texto_label.configure(text="Diga algo...")
    root.update()

    def reconhecimento_em_thread():
        progress_bar.pack(pady=10)
        progress_bar.start()

        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source)
                texto = recognizer.recognize_google(audio, language=idioma)
                texto_label.configure(text=f"Você disse: {texto}")
                
                links = buscar_videos_youtube(texto)
                
                # Limpa a área dos botões antes de adicionar os novos
                for widget in botoes_frame.winfo_children():
                    widget.destroy()
                
                # Cria botões para os links
                if "Erro" in links[0]:
                    resultado_label.configure(text="Erro ao acessar a API do YouTube.")
                else:
                    resultado_label.configure(text="Vídeos encontrados:")
                    for i, link in enumerate(links):
                        botao_video = ctk.CTkButton(
                            botoes_frame,
                            text=f"Vídeo {i + 1}",
                            command=lambda url=link: abrir_link(url)
                        )
                        botao_video.pack(pady=5)
            except sr.UnknownValueError:
                texto_label.configure(text="Não foi possível entender o que você disse.")
            except sr.RequestError:
                texto_label.configure(text="Erro ao acessar o serviço de reconhecimento de voz.")
            finally:
                progress_bar.stop()
                progress_bar.pack_forget()

    threading.Thread(target=reconhecimento_em_thread, daemon=True).start()

# Função chamada ao clicar no botão
def iniciar_reconhecimento():
    reconhecer_fala()

# Configuração da interface gráfica
root = ctk.CTk()
root.title("Reconhecimento de Voz com Busca no YouTube")
root.geometry("500x400")

# Label para exibir o texto reconhecido
texto_label = ctk.CTkLabel(root, text="Reconhecimento de voz", font=("Arial", 16), wraplength=480)
texto_label.pack(pady=20)

# Label para exibir os resultados
resultado_label = ctk.CTkLabel(root, text="", font=("Arial", 14), wraplength=480)
resultado_label.pack(pady=10)

# Frame para adicionar os botões dinamicamente
botoes_frame = ctk.CTkFrame(root)
botoes_frame.pack(pady=10)

# ComboBox para selecionar o idioma
idioma_label = ctk.CTkLabel(root, text="Escolha o idioma de reconhecimento:", font=("Arial", 12))
idioma_label.pack(pady=10)

idioma_combobox = ctk.CTkComboBox(root, values=["pt-BR", "en-US"])
idioma_combobox.set("pt-BR")
idioma_combobox.pack(pady=10)

# Barra de progresso
progress_bar = ctk.CTkProgressBar(root, width=400)

# Botão para iniciar o reconhecimento de voz
botao = ctk.CTkButton(root, text="Iniciar Reconhecimento", command=iniciar_reconhecimento)
botao.pack(pady=10)

# Botão para sair
exit = ctk.CTkButton(root, text="Sair", command=root.destroy)
exit.pack(pady=10)

# Executa o loop da interface gráfica
root.mainloop()
