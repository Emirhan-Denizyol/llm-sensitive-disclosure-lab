import streamlit as st
import pandas as pd

from src.attack_prompts import ATTACK_PROMPTS
from src.vulnerable_chatbot import generate_vulnerable_response
from src.secure_chatbot import generate_secure_response
from src.evaluator import evaluate_response
from src.pii_detector import detect_sensitive_data

st.set_page_config(page_title="LLM Sensitive Information Disclosure Lab", page_icon="🔐", layout="wide")

st.title("🔐 LLM Sensitive Information Disclosure Lab")
st.caption("OWASP Top 10 for LLM - Sensitive Information Disclosure uygulamalı test ortamı")
st.warning("Etik not: Bu projedeki tüm müşteri bilgileri, API key, şifre ve token değerleri tamamen sahte demo verileridir.")

with st.sidebar:
    st.header("Test Ayarları")
    mode = st.radio("Sistem Modu", ["Savunmasız", "Savunmalı"])
    role = st.selectbox("Kullanıcı Rolü", ["Normal Kullanıcı", "Destek Personeli", "Admin"])
    selected_test_name = st.selectbox("Hazır Saldırı Senaryosu", [f"{t['id']}. {t['name']}" for t in ATTACK_PROMPTS])
    st.divider()
    st.subheader("LLM Ayarı")
    use_ollama = st.checkbox("Gerçek LLM kullan: Ollama/Mistral", value=False)
    model_name = st.text_input("Ollama Model Adı", value="mistral")

selected_id = int(selected_test_name.split(".")[0])
selected_test = next(t for t in ATTACK_PROMPTS if t["id"] == selected_id)

st.subheader("Saldırı Promptu / Test Senaryosu")
prompt = st.text_area("Prompt", value=selected_test["prompt"], height=120)

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.metric("Test ID", selected_test["id"])
with col2:
    st.metric("Kategori", selected_test["category"])
with col3:
    st.metric("Mod", mode)
with col4:
    st.metric("LLM", model_name if use_ollama else "Simülasyon")

if st.button("Testi Çalıştır", type="primary"):
    with st.spinner("Model yanıtı üretiliyor..."):
        if mode == "Savunmasız":
            response = generate_vulnerable_response(prompt, role=role, use_ollama=use_ollama, model=model_name)
        else:
            response = generate_secure_response(prompt, role=role, use_ollama=use_ollama, model=model_name)

    result = evaluate_response(selected_test["id"], selected_test["name"], selected_test["category"], prompt, response, f"{mode}-Ollama" if use_ollama else mode, role)
    findings = detect_sensitive_data(response)

    st.divider()
    st.subheader("Model Yanıtı")
    st.text_area("Yanıt", value=response, height=350)

    if response.startswith("OLLAMA_"):
        st.error(response)
        st.info("Ollama uygulamasını açın ve terminalde `ollama run mistral` ile modeli test edin.")

    st.subheader("Güvenlik Analizi")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Saldırı Başarılı mı?", result["attack_successful"])
    with c2:
        st.metric("Risk Seviyesi", result["risk_level"])
    with c3:
        st.metric("Tespit Edilen Tür Sayısı", len(findings))

    if findings:
        st.error("Yanıtta hassas veri örüntüleri tespit edildi.")
        findings_table = [{"Hassas Veri Türü": label, "Örnek Değerler": ", ".join(values[:3])} for label, values in findings.items()]
        st.dataframe(pd.DataFrame(findings_table), use_container_width=True)
    else:
        st.success("Yanıtta hassas veri örüntüsü tespit edilmedi.")

st.divider()
st.subheader("10 Test Senaryosu")
st.dataframe(pd.DataFrame(ATTACK_PROMPTS)[["id", "name", "category", "prompt"]], use_container_width=True)

st.info("Tüm testleri terminalden çalıştırmak için:\n\n`python run_tests.py` → simülasyon testi\n\n`python run_tests.py --ollama --model mistral` → gerçek Ollama/Mistral testi")
