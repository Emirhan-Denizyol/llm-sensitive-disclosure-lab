from pathlib import Path
import compileall
import pandas as pd
import re
import sys

ROOT = Path(".")
errors = []
warnings = []

required_files = [
    "app.py",
    "run_tests.py",
    "requirements.txt",
    "README.md",
    "src/__init__.py",
    "src/attack_prompts.py",
    "src/evaluator.py",
    "src/guardrails.py",
    "src/ollama_client.py",
    "src/pii_detector.py",
    "src/rag_pipeline.py",
    "src/secure_chatbot.py",
    "src/vulnerable_chatbot.py",
    "data/company_policy.txt",
    "data/customer_records.txt",
    "data/internal_credentials.txt",
    "data/support_notes.txt",
    "data/system_instructions.txt",
    "docs/deney_sonuclari_ozeti.md",
    "docs/saldiri_promptlari.md",
    "docs/savunma_mekanizmalari.md",
    "docs/etik_not.md",
]

required_result_files = [
    "results/vulnerable_results_ollama.csv",
    "results/secure_results_ollama.csv",
    "results/comparison_report_ollama.csv",
]

print("\n==============================")
print("1) DOSYA VE KLASÖR KONTROLÜ")
print("==============================")

for file in required_files:
    if not (ROOT / file).exists():
        errors.append(f"Eksik dosya: {file}")
    else:
        print(f"OK  - {file}")

print("\n==============================")
print("2) RESULTS DOSYALARI KONTROLÜ")
print("==============================")

for file in required_result_files:
    if not (ROOT / file).exists():
        warnings.append(f"Sonuç dosyası bulunamadı: {file}")
    else:
        print(f"OK  - {file}")

print("\n==============================")
print("3) PYTHON SYNTAX KONTROLÜ")
print("==============================")

success = compileall.compile_dir("src", quiet=1)
if not success:
    errors.append("src klasöründe Python syntax hatası olabilir.")
else:
    print("OK  - src klasörü compile edildi.")

success_app = compileall.compile_file("app.py", quiet=1)
success_run = compileall.compile_file("run_tests.py", quiet=1)

if not success_app:
    errors.append("app.py syntax hatası olabilir.")
else:
    print("OK  - app.py compile edildi.")

if not success_run:
    errors.append("run_tests.py syntax hatası olabilir.")
else:
    print("OK  - run_tests.py compile edildi.")

print("\n==============================")
print("4) SALDIRI PROMPT SAYISI KONTROLÜ")
print("==============================")

try:
    from src.attack_prompts import ATTACK_PROMPTS
    print(f"OK  - Toplam saldırı promptu sayısı: {len(ATTACK_PROMPTS)}")
    if len(ATTACK_PROMPTS) < 10:
        errors.append("Saldırı promptu sayısı 10'dan az.")
except Exception as e:
    errors.append(f"attack_prompts.py import edilemedi: {e}")

print("\n==============================")
print("5) OLLAMA SONUÇ CSV ANALİZİ")
print("==============================")

comparison_path = ROOT / "results/comparison_report_ollama.csv"

if comparison_path.exists():
    try:
        df = pd.read_csv(comparison_path)
        print("OK  - comparison_report_ollama.csv okundu.")
        print("\nÖzet:")
        print(df.groupby(["mode", "attack_successful"]).size())

        required_columns = [
            "test_id",
            "test_name",
            "category",
            "mode",
            "role",
            "prompt",
            "detected_sensitive_types",
            "risk_level",
            "attack_successful",
            "response_preview",
        ]

        missing_columns = [c for c in required_columns if c not in df.columns]
        if missing_columns:
            errors.append(f"CSV kolonları eksik: {missing_columns}")
        else:
            print("OK  - CSV kolonları tam.")

        if len(df) < 20:
            warnings.append("comparison_report_ollama.csv 20 satırdan az görünüyor. 10 saldırı x 2 mod beklenir.")
        else:
            print(f"OK  - CSV satır sayısı: {len(df)}")

    except Exception as e:
        errors.append(f"comparison_report_ollama.csv okunamadı: {e}")
else:
    warnings.append("comparison_report_ollama.csv bulunamadı.")

print("\n==============================")
print("6) SAHTE VERİ / GERÇEK SECRET KONTROLÜ")
print("==============================")

all_text = ""
for folder in ["data", "src", "docs"]:
    for path in (ROOT / folder).rglob("*"):
        if path.is_file():
            try:
                all_text += "\n" + path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass

expected_demo_markers = [
    "sk-test-1234567890abcdef",
    "AdminDemoPass123",
    "demo_user",
    "example.com",
    "11111111110",
]

for marker in expected_demo_markers:
    if marker in all_text:
        print(f"OK  - Beklenen sahte demo verisi bulundu: {marker}")

suspicious_patterns = {
    "OPENAI_API_KEY benzeri": r"sk-[A-Za-z0-9]{40,}",
    "AWS Access Key benzeri": r"AKIA[0-9A-Z]{16}",
    "Private key başlangıcı": r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
}

for name, pattern in suspicious_patterns.items():
    matches = re.findall(pattern, all_text)
    if matches:
        warnings.append(f"Şüpheli gerçek secret pattern bulundu: {name}")

print("\n==============================")
print("7) SONUÇ")
print("==============================")

if errors:
    print("\nKRİTİK HATALAR:")
    for e in errors:
        print(f"- {e}")
else:
    print("OK  - Kritik hata bulunmadı.")

if warnings:
    print("\nUYARILAR:")
    for w in warnings:
        print(f"- {w}")
else:
    print("OK  - Uyarı bulunmadı.")

print("\nKontrol tamamlandı.")
