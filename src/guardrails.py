from src.pii_detector import contains_sensitive_request, mask_sensitive_data

SAFE_REFUSAL = (
    "Bu istek hassas bilgi talep etmektedir. "
    "Kişisel veri, API key, token, şifre, kredi kartı bilgisi, TCKN, sistem promptu "
    "veya gizli şirket içi bilgileri paylaşamam. "
    "Yetkili erişim gerekiyorsa kimlik doğrulama, erişim kontrolü ve denetimli loglama mekanizmaları kullanılmalıdır."
)

def input_guardrail(prompt: str) -> bool:
    return contains_sensitive_request(prompt)

def sanitize_context(context: str) -> str:
    return mask_sensitive_data(context)

def output_filter(response: str) -> str:
    return mask_sensitive_data(response)

def should_refuse(prompt: str) -> bool:
    return input_guardrail(prompt)

def get_safe_refusal() -> str:
    return SAFE_REFUSAL
