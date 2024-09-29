import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

class BotPerguntasRespostas:
    def __init__(self, base_conhecimento):
        self.base_conhecimento = {pergunta.lower(): resposta for pergunta, resposta in base_conhecimento.items()}
        self.perguntas_feitas = 0

    def responder_pergunta(self, pergunta):
        self.perguntas_feitas += 1
        pergunta = pergunta.lower()
        return self.base_conhecimento.get(pergunta, "Desculpe, não tenho uma resposta para essa pergunta.")

    def adicionar_conhecimento(self, pergunta, resposta):
        self.base_conhecimento[pergunta.lower()] = resposta

def reproduzir_audio(texto):
    tts = gTTS(text=texto, lang='pt-br')
    temp_file = "resposta_temp.mp3"
    tts.save(temp_file)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove(temp_file)

def capturar_audio():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo...")
        reconhecedor.adjust_for_ambient_noise(source)
        audio = reconhecedor.listen(source, timeout=5)
    try:
        pergunta = reconhecedor.recognize_google(audio, language="pt-BR")
        print(f"Você perguntou: {pergunta}")
        return pergunta
    except sr.UnknownValueError:
        print("Não foi possível entender a pergunta. Por favor, tente novamente.")
        return None
    except sr.RequestError as e:
        print(f"Erro na solicitação ao serviço de reconhecimento de fala: {e}")
        return None

class BotGUI:
    def __init__(self, master, bot):
        self.master = master
        self.bot = bot
        self.master.title("Bot de Perguntas e Respostas")
        self.master.geometry("300x700")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.frame_perguntas = ttk.Frame(self.notebook, padding="10")
        self.frame_adicionar = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.frame_perguntas, text="Perguntar")
        self.notebook.add(self.frame_adicionar, text="Adicionar Conhecimento")

        self.setup_perguntas_tab()
        self.setup_adicionar_tab()

    def setup_perguntas_tab(self):
        self.pergunta_entry = ttk.Entry(self.frame_perguntas, width=50)
        self.pergunta_entry.pack(pady=10)

        self.enviar_btn = ttk.Button(self.frame_perguntas, text="Enviar", command=self.enviar_pergunta)
        self.enviar_btn.pack(pady=5)

        self.resposta_text = tk.Text(self.frame_perguntas, wrap=tk.WORD, width=50, height=10)
        self.resposta_text.pack(pady=10)

        self.mic_btn = ttk.Button(self.frame_perguntas, text="🎤", command=self.ativar_voz, width=3)
        self.mic_btn.pack(pady=5)

    def setup_adicionar_tab(self):
        ttk.Label(self.frame_adicionar, text="Nova Pergunta:").pack(pady=5)
        self.nova_pergunta_entry = ttk.Entry(self.frame_adicionar, width=50)
        self.nova_pergunta_entry.pack(pady=5)

        ttk.Label(self.frame_adicionar, text="Resposta:").pack(pady=5)
        self.nova_resposta_text = tk.Text(self.frame_adicionar, wrap=tk.WORD, width=50, height=5)
        self.nova_resposta_text.pack(pady=5)

        self.adicionar_btn = ttk.Button(self.frame_adicionar, text="Adicionar à Base de Conhecimento", command=self.adicionar_conhecimento)
        self.adicionar_btn.pack(pady=10)

    def enviar_pergunta(self):
        pergunta = self.pergunta_entry.get()
        resposta = self.bot.responder_pergunta(pergunta)
        self.exibir_resposta(resposta)
        reproduzir_audio(resposta)

    def ativar_voz(self):
        pergunta = capturar_audio()
        if pergunta:
            self.pergunta_entry.delete(0, tk.END)
            self.pergunta_entry.insert(0, pergunta)
            self.enviar_pergunta()

    def exibir_resposta(self, resposta):
        self.resposta_text.delete(1.0, tk.END)
        self.resposta_text.insert(tk.END, resposta)

    def adicionar_conhecimento(self):
        nova_pergunta = self.nova_pergunta_entry.get()
        nova_resposta = self.nova_resposta_text.get("1.0", tk.END).strip()

        if nova_pergunta and nova_resposta:
            self.bot.adicionar_conhecimento(nova_pergunta, nova_resposta)
            messagebox.showinfo("Sucesso", "Novo conhecimento adicionado com sucesso!")
            self.nova_pergunta_entry.delete(0, tk.END)
            self.nova_resposta_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, preencha tanto a pergunta quanto a resposta.")

if __name__ == "__main__":
    base_de_conhecimento = {
        "qual é o seu nome": "Eu sou um assistente virtual, Destruidor de galáxias e rei dos reinos sem conhecimento.",
        "qual o seu nome": "Eu sou um assistente virtual, Destruidor de galáxias e rei dos reinos sem conhecimento.",
        "seu nome": "Eu sou um assistente virtual, Destruidor de galáxias e rei dos reinos sem conhecimento.",
        "qual é a capital do brasil": "A capital do Brasil é Brasília.",
        "quem é o presidente dos estados unidos": "O presidente dos Estados Unidos é Joe Biden.",
        "qual é a cor do céu": "A cor do céu é azul.",
        "quanto é 2 mais 2": "2 mais 2 é igual a 4.",
        "2 mais 2": "2 mais 2 é igual a 4.",
        "some 2 mais 2": "2 mais 2 é igual a 4.",
        "quanto é 2 + 2": "2 mais 2 é igual a 4.",
        "como você está": "Eu sou apenas um programa de computador, mas estou funcionando bem!",
        "o que você faz": "Eu sou um assistente virtual projetado para responder a perguntas.",
        "qual é a sua cor favorita": "Eu não tenho uma cor favorita, pois sou um programa de computador.",
        "qual é o maior planeta do sistema solar": "O maior planeta do sistema solar é Júpiter.",
        "quem pintou a mona lisa": "A Mona Lisa foi pintada por Leonardo da Vinci.",
        "qual é o elemento químico mais abundante no universo": "O elemento químico mais abundante no universo é o hidrogênio.",
        "em que ano começou a primeira guerra mundial": "A Primeira Guerra Mundial começou em 1914.",
        "qual é o menor país do mundo": "O menor país do mundo é o Vaticano.",
        "quem escreveu dom quixote": "Dom Quixote foi escrito por Miguel de Cervantes.",
        "qual é a montanha mais alta do mundo": "A montanha mais alta do mundo é o Monte Everest.",
        "quem inventou a lâmpada elétrica": "A lâmpada elétrica foi inventada por Thomas Edison.",
        "qual é o maior oceano do mundo": "O maior oceano do mundo é o Oceano Pacífico.",
        "quem foi o primeiro homem a pisar na lua": "O primeiro homem a pisar na lua foi Neil Armstrong.",
    }

    bot = BotPerguntasRespostas(base_de_conhecimento)
    root = tk.Tk()
    app = BotGUI(root, bot)
    root.mainloop()

    ## feito por Renan Matheus ##