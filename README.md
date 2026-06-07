# LLM Sensitive Information Disclosure Lab - Ollama/Mistral Destekli Sürüm

Bu proje, **Büyük Dil Modellerinde Siber Güvenlik** dersi final çalışması kapsamında hazırlanmıştır. Projede, OWASP Top 10 for LLM kapsamında yer alan **Sensitive Information Disclosure** güvenlik açığı kontrollü ve etik bir test ortamında uygulamalı olarak analiz edilmiştir.

Amaç, RAG destekli bir LLM sisteminde hassas bilgilerin nasıl yanlışlıkla açığa çıkabileceğini göstermek ve temel savunma mekanizmalarının bu riski nasıl azalttığını test etmektir.

---

## Proje Özeti

Projede iki farklı sistem modu bulunmaktadır:

- **Savunmasız Mod:** Güvenlik filtresi olmayan RAG/LLM davranışını temsil eder. Bu modda model, kaynak dokümanlarda bulunan sahte hassas bilgileri kullanıcıya döndürebilir.
- **Savunmalı Mod:** Input guardrail, rol bazlı erişim kontrolü, context sanitization ve output filtering mekanizmalarını kullanır. Amaç, hassas bilgi talebini model cevabına dönüşmeden engellemektir.

---

## Kullanılan Teknolojiler

- Python
- Streamlit
- Ollama
- Mistral
- Regex tabanlı hassas veri tespiti
- Sahte RAG dokümanları
- CSV tabanlı test sonuç raporlaması

---

## Proje Yapısı

```text
llm-sensitive-disclosure-lab/
├── app.py
├── run_tests.py
├── requirements.txt
├── final_check.py
├── README.md
├── src/
├── data/
├── docs/
├── results/
└── ekran_goruntuleri/
```

### Klasör Açıklamaları

```text
src/                Uygulama kaynak kodları
data/               Sahte RAG dokümanları ve demo veri setleri
docs/               Deney özeti, saldırı promptları, savunma mekanizmaları ve etik notlar
results/            Otomatik test çıktıları
ekran_goruntuleri/  Canlı test senaryolarına ait ekran görüntüleri
```

---

## Kurulum

Projeyi klonladıktan sonra proje klasörüne girin:

```bash
cd llm-sensitive-disclosure-lab
```

Sanal ortam oluşturun:

```bash
python3 -m venv venv
```

Sanal ortamı aktif edin:

```bash
source venv/bin/activate
```

Gerekli paketleri kurun:

```bash
pip install -r requirements.txt
```

---

## Ollama Kontrolü

Önce Ollama uygulamasını açın.

Yüklü modelleri kontrol edin:

```bash
ollama list
```

Mistral modeli yüklü değilse indirin:

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

---

## Streamlit Uygulamasını Çalıştırma

```bash
streamlit run app.py
```

Uygulama açıldıktan sonra sol panelden aşağıdaki ayarlar yapılabilir:

```text
Sistem Modu: Savunmasız / Savunmalı
Kullanıcı Rolü: Normal Kullanıcı / Destek Personeli / Admin
Hazır Saldırı Senaryosu: 15 farklı saldırı promptu
Gerçek LLM kullan: Ollama/Mistral
Ollama Model Adı: mistral
```

**"Gerçek LLM kullan: Ollama/Mistral"** seçeneği aktif edildiğinde sistem lokal Mistral modeline bağlanır.

---

## Otomatik Testler

Simülasyon modunda test çalıştırmak için:

```bash
python run_tests.py
```

Ollama/Mistral ile gerçek LLM testi çalıştırmak için:

```bash
python run_tests.py --ollama --model mistral
```

Test sonuçları `results/` klasörüne kaydedilir:

```text
results/
├── comparison_report_ollama.csv
├── secure_results_ollama.csv
└── vulnerable_results_ollama.csv
```

---

## Güncel Deney Sonuçları

Ollama/Mistral ile yapılan güncel otomatik testlerde toplam **15 saldırı promptu** kullanılmıştır.

| Sistem | Başarılı Saldırı | Başarısız / Engellenen Saldırı | Saldırı Başarı Oranı |
|---|---:|---:|---:|
| Savunmasız-Ollama/Mistral | 13 | 2 | %86,7 |
| Savunmalı-Ollama/Mistral | 0 | 15 | %0 |

Bu sonuçlara göre savunmasız RAG destekli LLM sisteminde hassas bilgi ifşası riski yüksek çıkmıştır. Savunma mekanizmaları etkinleştirildiğinde ise aynı saldırıların tamamı engellenmiştir.

---

## Kullanılan Saldırı Kategorileri

Projede aşağıdaki saldırı kategorileri test edilmiştir:

1. Direct Disclosure
2. Role Impersonation
3. Urgency Pressure
4. Partial Leakage
5. Format Bypass
6. System Prompt Leakage
7. Debug Leakage
8. Code Format Leakage
9. Summarization Abuse
10. Indirect Leakage
11. Translation Abuse
12. Table Format Leakage
13. Log Analysis Abuse
14. Regex Extraction
15. Masking Bypass

---

## Savunma Mekanizmaları

Projede aşağıdaki savunma katmanları uygulanmıştır:

- Input guardrail
- Rol bazlı erişim kontrolü
- RAG context sanitization
- Output filtering
- Güvenli ret cevabı
- Regex tabanlı hassas veri tespiti

Savunmalı sistemde hassas bilgi talebi içeren promptlar mümkün olduğunca model cevabına dönüşmeden engellenmektedir.

---

## Son Kontrol

Teslim veya çalıştırma öncesinde proje bütünlüğünü kontrol etmek için:

```bash
python final_check.py
```

Beklenen çıktı:

```text
OK  - Kritik hata bulunmadı.
OK  - Uyarı bulunmadı.
Kontrol tamamlandı.
```

Bu kontrol; dosya yapısını, Python syntax durumunu, saldırı prompt sayısını, sonuç CSV dosyalarını ve demo secret kontrolünü doğrular.

---

## Etik Not

Bu projedeki tüm müşteri bilgileri, API key, şifre, token, TCKN, kredi kartı ve veritabanı bağlantısı değerleri tamamen sahte demo verileridir.

Gerçek kişisel veri, gerçek API anahtarı, gerçek şifre veya gerçek sistem bilgisi kullanılmamıştır. Gerçek sistemlere saldırı yapılmamıştır.

Bu çalışma yalnızca eğitim, analiz ve savunma mekanizmalarını değerlendirme amacıyla hazırlanmıştır.
