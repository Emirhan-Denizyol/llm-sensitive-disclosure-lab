import argparse
import pandas as pd
from pathlib import Path

from src.attack_prompts import ATTACK_PROMPTS
from src.vulnerable_chatbot import generate_vulnerable_response
from src.secure_chatbot import generate_secure_response
from src.evaluator import evaluate_response

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

def run_all_tests(role: str = "Normal Kullanıcı", use_ollama: bool = False, model: str = "mistral"):
    vulnerable_rows = []
    secure_rows = []

    for test in ATTACK_PROMPTS:
        prompt = test["prompt"]
        vulnerable_response = generate_vulnerable_response(prompt, role=role, use_ollama=use_ollama, model=model)
        secure_response = generate_secure_response(prompt, role=role, use_ollama=use_ollama, model=model)

        vulnerable_rows.append(evaluate_response(
            test["id"], test["name"], test["category"], prompt, vulnerable_response,
            "Savunmasız-Ollama" if use_ollama else "Savunmasız", role
        ))
        secure_rows.append(evaluate_response(
            test["id"], test["name"], test["category"], prompt, secure_response,
            "Savunmalı-Ollama" if use_ollama else "Savunmalı", role
        ))

    vulnerable_df = pd.DataFrame(vulnerable_rows)
    secure_df = pd.DataFrame(secure_rows)
    combined_df = pd.concat([vulnerable_df, secure_df], ignore_index=True)

    suffix = "ollama" if use_ollama else "simulation"
    vulnerable_df.to_csv(RESULTS_DIR / f"vulnerable_results_{suffix}.csv", index=False)
    secure_df.to_csv(RESULTS_DIR / f"secure_results_{suffix}.csv", index=False)
    combined_df.to_csv(RESULTS_DIR / f"comparison_report_{suffix}.csv", index=False)

    print("Testler tamamlandı.")
    print(f"Savunmasız sonuçlar: {RESULTS_DIR / f'vulnerable_results_{suffix}.csv'}")
    print(f"Savunmalı sonuçlar: {RESULTS_DIR / f'secure_results_{suffix}.csv'}")
    print(f"Karşılaştırma raporu: {RESULTS_DIR / f'comparison_report_{suffix}.csv'}")
    print("\nÖzet:")
    print(combined_df.groupby(["mode", "attack_successful"]).size())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ollama", action="store_true", help="Gerçek Ollama/Mistral modelini kullanır.")
    parser.add_argument("--model", default="mistral", help="Ollama model adı. Varsayılan: mistral")
    parser.add_argument("--role", default="Normal Kullanıcı", help="Kullanıcı rolü")
    args = parser.parse_args()
    run_all_tests(role=args.role, use_ollama=args.ollama, model=args.model)
