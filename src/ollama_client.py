import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def call_ollama(prompt: str, model: str = "mistral", temperature: float = 0.2) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return "OLLAMA_CONNECTION_ERROR: Ollama servisine bağlanılamadı. Ollama uygulamasını açın."
    except requests.exceptions.HTTPError as exc:
        return f"OLLAMA_HTTP_ERROR: {exc}. Model adını kontrol edin. Örn: mistral"
    except requests.exceptions.Timeout:
        return "OLLAMA_TIMEOUT_ERROR: Model yanıtı zaman aşımına uğradı."
    except Exception as exc:
        return f"OLLAMA_UNKNOWN_ERROR: {exc}"
