# LLM Sensitive Information Disclosure Lab - Ollama/Mistral Destekli Sürüm

Bu proje, OWASP Top 10 for LLM kapsamında Sensitive Information Disclosure güvenlik açığını kontrollü ve etik bir test ortamında göstermek için hazırlanmıştır.

## Kurulum

```bash
cd llm-sensitive-disclosure-lab
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ollama Kontrolü

Önce Ollama uygulamasını açın.

```bash
ollama list
```

Mistral yoksa:

```bash
ollama pull mistral
```

Modeli test etmek için:

```bash
ollama run mistral
```

Çıkmak için:

```text
/bye
```

## Streamlit Uygulaması

```bash
streamlit run app.py
```

Sol panelde "Gerçek LLM kullan: Ollama/Mistral" seçeneğini açarsanız sistem Mistral modeline bağlanır.

## Otomatik Testler

Simülasyon:

```bash
python run_tests.py
```

Ollama/Mistral:

```bash
python run_tests.py --ollama --model mistral
```

## Etik Not

Tüm veriler sahte demo verisidir. Gerçek sistemlere veya gerçek kişilere ait veri kullanılmamıştır.
