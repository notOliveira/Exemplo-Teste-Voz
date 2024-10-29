import speech_recognition as sr
from transformers import pipeline
import tkinter as tk
import customtkinter as ctk
import threading

print("Iniciando reconhecimento de voz...\nPara finalizar, pressione Ctrl+C no terminal, ou feche a janela pelo programa.")
# Inicializa o reconhecedor de fala
recognizer = sr.Recognizer()

# Função para reconhecer e processar a fala
def reconhecer_fala():
    # Obtém o idioma selecionado
    idioma = idioma_combobox.get()

    # Atualiza a interface para mostrar a mensagem "Diga algo..."
    texto_label.configure(text="Diga algo...")
    root.update()

    # Executa o reconhecimento de fala em uma thread separada
    def reconhecimento_em_thread():
        # Exibe a barra de progresso apenas depois que a fala for identificada
        progress_bar.pack(pady=10)  # Mostra a barra de progresso
        progress_bar.start()

        with sr.Microphone() as source:
            try:
                # Ajusta o ambiente para capturar melhor o áudio
                audio = recognizer.listen(source)
                
                # Usa o Google Web Speech API para reconhecer o áudio no idioma escolhido
                texto = recognizer.recognize_google(audio, language=idioma)
                
                # Atualiza o texto na interface gráfica
                texto_label.configure(text=f"Você disse: {texto}")
                
                # Agora que o texto foi reconhecido, mostra a barra de progresso
                # e inicia a análise de sentimento
                analisar_texto_com_IA(texto)
            except sr.UnknownValueError:
                texto_label.configure(text="Não foi possível entender o que você disse.")
            except sr.RequestError:
                texto_label.configure(text="Erro ao acessar o serviço de reconhecimento de voz.")
            finally:
                # Após terminar o reconhecimento e a análise, esconde a barra de progresso
                progress_bar.stop()
                progress_bar.pack_forget()

    # Inicia a thread de reconhecimento
    threading.Thread(target=reconhecimento_em_thread, daemon=True).start()

# Função para realizar análise de sentimentos usando PLN
def analisar_texto_com_IA(texto):
    nlp = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    resultado = nlp(texto)

    # Mapeamento das estrelas para seus significados
    estrelas = resultado[0]['label']
    sentimento = {
        "1 star": "Muito negativo",
        "2 stars": "Negativo",
        "3 stars": "Neutro",
        "4 stars": "Positivo",
        "5 stars": "Muito positivo"
    }

    resultado_texto = f"Análise de sentimento: {sentimento[estrelas]}, com confiança de {resultado[0]['score']:.2f}"
    resultado_label.configure(text=resultado_texto)

# Função chamada ao clicar no botão
def iniciar_reconhecimento():
    reconhecer_fala()

# Configuração da interface gráfica
root = ctk.CTk()
root.title("Reconhecimento de Voz com Análise de Sentimento")
root.geometry("500x350")

# Label para exibir o texto reconhecido
texto_label = ctk.CTkLabel(root, text="Reconhecimento de voz", font=("Arial", 16), wraplength=480)
texto_label.pack(pady=20)

# Label para exibir o resultado da análise de sentimento
resultado_label = ctk.CTkLabel(root, text="", font=("Arial", 14), wraplength=480)
resultado_label.pack(pady=20)

# ComboBox para selecionar o idioma
idioma_label = ctk.CTkLabel(root, text="Escolha o idioma de reconhecimento:", font=("Arial", 12))
idioma_label.pack(pady=10)

idioma_combobox = ctk.CTkComboBox(root, values=["pt-BR", "en-US"])
idioma_combobox.set("pt-BR")  # Define o valor padrão como português
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
