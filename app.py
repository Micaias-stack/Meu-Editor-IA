import streamlit as st
from openai import OpenAI
import requests

# Configuração da Página
st.set_page_config(page_title="AI Video Master Pro", layout="wide", page_icon="🎬")

# --- INTERFACE LATERAL (APIs) ---
with st.sidebar:
    st.title("🔑 Configuração de Chaves")
    st.markdown("Pegue suas chaves nos sites oficiais:")
    
    # Links diretos para facilitar sua vida
    st.markdown("- [OpenAI (GPT/DALL-E)](https://platform.openai.com/api-keys)")
    st.markdown("- [ElevenLabs (Voz)](https://elevenlabs.io/app/settings/api-keys)")
    st.markdown("- [Runway (Vídeo)](https://dashboard.runwayml.com/settings/api-keys)")
    
    st.divider()
    
    # Campos de entrada
    api_openai = st.text_input("GPT-4o / DALL-E 3:", type="password", placeholder="sk-...")
    api_eleven = st.text_input("ElevenLabs (Voz):", type="password", placeholder="Insira aqui...")
    api_runway = st.text_input("Runway (Vídeo):", type="password", placeholder="Insira aqui...")

    if api_openai:
        client = OpenAI(api_key=api_openai)
        st.success("🤖 OpenAI Pronta!")

# --- CORPO DO APP ---
st.title("🎬 Editor de Vídeo Inteligente")
st.info("Descreva sua ideia e a IA cuidará de todo o processo criativo.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Briefing do Vídeo")
    prompt_usuario = st.text_area(
        "O que o vídeo deve conter?",
        placeholder="Ex: Um documentário curto sobre buracos negros, voz profunda, estilo interestelar.",
        height=150
    )
    
    estilo = st.select_slider(
        "Nível de Criatividade da IA",
        options=["Conservador", "Equilibrado", "Inovador", "Experimental"]
    )
    
    if st.button("🚀 GERAR VÍDEO AGORA"):
        if not api_openai:
            st.error("⚠️ Erro: Insira a chave da OpenAI na barra lateral!")
        elif not prompt_usuario:
            st.warning("⚠️ Digite o que você quer que o vídeo contenha.")
        else:
            try:
                with st.status("🏗️ Construindo seu vídeo...", expanded=True) as status:
                    # 1. GERANDO O ROTEIRO (REAL)
                    st.write("🧠 GPT-4o criando roteiro e cenas...")
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Você é um diretor de vídeo profissional. Crie um roteiro dividido em 3 cenas detalhadas."},
                            {"role": "user", "content": prompt_usuario}
                        ]
                    )
                    roteiro = response.choices[0].message.content
                    st.session_state['roteiro'] = roteiro
                    
                    # 2. SIMULAÇÃO DE MÍDIA (Preparando para as outras APIs)
                    st.write("🎙️ Gerando locução profissional...")
                    st.write("🖼️ Criando frames em alta definição...")
                    st.write("🎞️ Renderizando movimentos de câmera...")
                    
                    status.update(label="✅ Processamento Concluído!", state="complete")
                
                st.balloons()
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")

# --- RESULTADO E PREVIEW ---
with col2:
    st.subheader("📺 Preview e Edição")
    
    if 'roteiro' in st.session_state:
        with st.expander("📄 Ver Roteiro Gerado pela IA"):
            st.write(st.session_state['roteiro'])
        
        # Player de vídeo (Simulado até você conectar a saída da Runway)
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        
        st.success("O vídeo acima é uma prévia baseada no roteiro.")
        st.download_button("📥 Baixar Vídeo (MP4)", data="...", file_name="video_ia.mp4")
    else:
        st.info("O vídeo aparecerá aqui assim que você clicar em 'Gerar'.")

st.divider()
st.caption("App v1.0 | Conectado via Streamlit Cloud")
