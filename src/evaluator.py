from typing import Dict, Any
from src.pii_detector import detect_sensitive_data, risk_level, is_attack_successful

def evaluate_response(test_id: int, test_name: str, category: str, prompt: str, response: str, mode: str, role: str) -> Dict[str, Any]:
    findings = detect_sensitive_data(response)
    risk = risk_level(findings)
    success = is_attack_successful(findings)
    return {
        "test_id": test_id,
        "test_name": test_name,
        "category": category,
        "mode": mode,
        "role": role,
        "prompt": prompt,
        "detected_sensitive_types": ", ".join(findings.keys()) if findings else "-",
        "risk_level": risk,
        "attack_successful": "Evet" if success else "Hayır",
        "response_preview": response[:500].replace("\n", " ")
    }
