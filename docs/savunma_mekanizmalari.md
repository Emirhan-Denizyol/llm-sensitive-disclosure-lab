# Savunma Mekanizmaları

Bu çalışmada **Sensitive Information Disclosure** riskini azaltmak için birden fazla savunma katmanı kullanılmıştır.

## 1. Input Guardrail

Kullanıcı promptu modele gönderilmeden önce analiz edilir.

Amaç:

- Hassas veri talebi içeren promptları erken aşamada yakalamak
- Modelin riskli prompta cevap üretmesini engellemek
- Gereksiz LLM çağrılarını azaltmak

Tespit edilen bazı riskli ifadeler:

- TCKN
- telefon
- e-posta
- kredi kartı
- API key
- token
- secret
- password / şifre
- sistem promptu
- admin bilgisi
- veritabanı bağlantısı

## 2. Rol Bazlı Erişim Kontrolü

Kullanıcı rolüne göre RAG sisteminin erişebileceği kaynak dokümanlar sınırlandırılmıştır.

| Rol | Erişim |
|---|---|
| Normal Kullanıcı | Genel şirket politikası |
| Destek Personeli | Genel politika ve destek notları |
| Admin | Genel politika, destek notları ve müşteri kayıtları |

Bu yaklaşım, her kullanıcının tüm dokümanlara erişmesini engeller.

## 3. Context Sanitization

RAG tarafından getirilen kaynak dokümanlar modele verilmeden önce hassas veri açısından temizlenir veya maskelenir.

Örnek maskeleme:

```text
11111111110 → [MASKED_TCKN]
ahmet.yilmaz@example.com → [MASKED_EMAIL]
0555 111 22 33 → [MASKED_PHONE]
sk-test-1234567890abcdef → [MASKED_API_KEY]
AdminDemoPass123! → [MASKED_PASSWORD]
```

## 4. Output Filtering

Model cevabı kullanıcıya gösterilmeden önce tekrar analiz edilir.

Amaç:

- Modelin yanlışlıkla hassas veri üretmesini engellemek
- Prompt bypass girişimlerinde son güvenlik katmanı sağlamak
- Hassas veri örüntülerini maskelemek

## 5. Güvenli Ret Cevabı

Hassas bilgi talep eden isteklerde sistem doğrudan güvenli ret cevabı üretir.

Örnek güvenli ret cevabı:

```text
Bu istek hassas bilgi talep etmektedir. Kişisel veri, API key, token, şifre, kredi kartı bilgisi, TCKN, sistem promptu veya gizli şirket içi bilgileri paylaşamam.
```

## 6. Defense-in-Depth Yaklaşımı

Tek bir savunma katmanı yeterli değildir. Bu nedenle sistemde çok katmanlı savunma uygulanmıştır:

```text
Kullanıcı Promptu
↓
Input Guardrail
↓
Rol Bazlı Erişim Kontrolü
↓
RAG Context Sanitization
↓
LLM Yanıt Üretimi
↓
Output Filtering
↓
Kullanıcıya Güvenli Yanıt
```

## 7. Savunma Sonuçları

Ollama/Mistral ile yapılan güncel testlerde toplam **15 saldırı promptu** çalıştırılmıştır.

| Sistem | Başarılı Saldırı | Engellenen / Başarısız Saldırı | Saldırı Başarı Oranı |
|---|---:|---:|---:|
| Savunmasız sistem | 13 | 2 | %86,7 |
| Savunmalı sistem | 0 | 15 | %0 |

Bu sonuç, savunma mekanizmalarının hassas bilgi ifşası riskini önemli ölçüde azalttığını göstermektedir.

## 8. Sınırlılıklar

Bu savunma mekanizmaları temel regex ve anahtar kelime kontrollerine dayanmaktadır. Gerçek sistemlerde aşağıdaki ek mekanizmalar kullanılmalıdır:

- Gelişmiş PII detection servisleri
- DLP sistemleri
- Kimlik doğrulama ve yetkilendirme
- Audit log
- Rate limiting
- Prompt injection detection
- Retrieval-level access control
- Secret scanning
- Human approval workflows
