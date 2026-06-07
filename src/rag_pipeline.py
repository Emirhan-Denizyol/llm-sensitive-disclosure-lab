from pathlib import Path
from typing import List, Dict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_documents() -> List[Dict[str, str]]:
    docs = []
    for file_path in sorted(DATA_DIR.glob("*.txt")):
        docs.append({"source": file_path.name, "content": file_path.read_text(encoding="utf-8")})
    return docs

def simple_retrieve(query: str, role: str = "Normal Kullanıcı", secure: bool = False) -> List[Dict[str, str]]:
    docs = load_documents()
    q = query.lower()

    if secure:
        allowed_sources = {
            "Normal Kullanıcı": {"company_policy.txt"},
            "Destek Personeli": {"company_policy.txt", "support_notes.txt"},
            "Admin": {"company_policy.txt", "support_notes.txt", "customer_records.txt"},
        }
        docs = [d for d in docs if d["source"] in allowed_sources.get(role, {"company_policy.txt"})]

    scored = []
    for doc in docs:
        content_lower = doc["content"].lower()
        score = 0
        for token in q.split():
            if len(token) > 3 and token in content_lower:
                score += 1

        if not secure and any(k in q for k in ["api", "şifre", "sifre", "password", "tckn", "telefon", "müşteri", "musteri", "admin", "token", "secret", "debug", "sistem"]):
            if doc["source"] in {"customer_records.txt", "internal_credentials.txt", "support_notes.txt", "system_instructions.txt"}:
                score += 5

        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return docs[:2]
    return [doc for _, doc in scored[:3]]

def build_context(retrieved_docs: List[Dict[str, str]]) -> str:
    chunks = []
    for doc in retrieved_docs:
        chunks.append(f"[Kaynak: {doc['source']}]\n{doc['content']}")
    return "\n\n---\n\n".join(chunks)
