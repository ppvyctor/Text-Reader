import pyttsx3
import streamlit as st
import PyPDF2
import pdf2image
import tempfile
from docx.api import Document
import os

engine = pyttsx3.init()

def ler_texto(engine, texto, taixadefala, voz):
    # Configuração de tom de voz
    engine.setProperty("rate", taixadefala)
    
    # Configuração de volume
    engine.setProperty("volume", 1)
    
    # Configuração de qual voz querer
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voz].id)
    
    path_audio = ""
    
    with tempfile.NamedTemporaryFile(delete = False, suffix=".mp3") as temp_audio:
        engine.save_to_file(texto, temp_audio.name)
        path = "\\".join(temp_audio.name.split("\\")[: len(temp_audio.name.split("\\")) - 1])
        path_audio = temp_audio.name
    
        folden = os.listdir(path) 
        for x in range(len(folden)):
            
            folden[x] = os.path.join(path, folden[x])
            
        for x in range(len(folden)):
            if folden[x].split(".")[len(folden[x].split(".")) - 1] in ["pdf", "mp3"]: 
                
                if folden[x].split(".")[len(folden[x].split(".")) - 1] != "mp3" or folden[x].split(".")[len(folden[x].split(".")) - 1] != temp_audio:
                    try:
                        os.remove(folden[x])
                    except:
                        pass
    
    engine.runAndWait()

    return path_audio

# Modifica a vísualização do site, para que pegue toda a tela
st.set_page_config(layout="wide")

# Centraliza e coloca o título
st.markdown("<h1 style='text-align: center;'>Bem-vindo ao leitor de texto!!📖</h1>", unsafe_allow_html=True)

# Divide o site em colunas, no caso 1/4 da coluna está na esquerda e 3/4 está na direita
left, right = st.columns([1, 4])


# Lado direito da tela
with right:
    file = st.file_uploader("Descarregue seu arquivo aqui.", type=["pdf", "docx"])
    
    if file is None:
        texto = st.text_area("### **Digite seu texto abaixo.**", height=500)
    
    else:
        if "pdf" in file.name.split(".")[len(file.name.split(".")) - 1]:
            documento = PyPDF2.PdfReader(file)
            
            num_paginas = len(documento.pages)
            pag_atual = st.slider("Página", min_value = 1, max_value = num_paginas, value = 1, step = 1) - 1
            
            pagina = documento.pages[pag_atual]
            texto = pagina.extract_text()
            
            
            with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as temporariefile:
                temporariefile.write(file.getvalue())
                temporariefile.flush()
                
                
                
                pagina = pdf2image.convert_from_path(temporariefile.name, 700, first_page=pag_atual+1, last_page=pag_atual+1)
                st.image(pagina)
                pagina = None
                path_pag = fr"{temporariefile.name}"
            
        elif "docx" in file.name.split(".")[len(file.name.split(".")) - 1]:
            documento = Document(file)
            texto = []
            for paragraph in documento.paragraphs:
                texto.append(paragraph.text)
            
            # Imprime o texto
            for t in texto:
                st.write(t)
            
            texto = "\n".join(texto)

path_picture = ""
    
# Lado esquerdo da tela
with left:
    # Colocando uma barra que controla a velocidade do audio
    tomDeVoz = st.slider("Velocidade do áudio.", min_value = 1, max_value = 400, value = 200, step = 1)
    
    motor_voz = pyttsx3.init()
    audio = motor_voz.getProperty('voices')
    nomes = []
    
    for index, voice in enumerate(audio):
        nomes.append([voice.name.replace("Microsoft ", ""), index])
    
    # Colocando a opção do audio
    narrador = st.radio("Vozes", [x[0] for x in nomes])
    
    if narrador == nomes[0][0]:
        voz = 0
    elif narrador == nomes[1][0]:
        voz = 1
    else:
        voz = 2

    if texto == "" or texto.replace(" ", "") == "": st.markdown("##### **Digite ou cole um texto ao lado para liberar o botão do áudio.**")
    
    else:
        # Adicionando o botão para ler o texto
        if st.button("Inicia a leitura do texto."):   
            try:
                path_picture = ler_texto(engine, texto, tomDeVoz, voz)
                st.audio(path_picture, format="audio/mp3", autoplay = True)
                
                engine.endLoop()
            except:
                try:
                    engine.endLoop()
                except:
                    pass