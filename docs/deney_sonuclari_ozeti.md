# Deney Sonuçları Özeti

Bu çalışmada OWASP Top 10 for LLM kapsamında yer alan **Sensitive Information Disclosure** güvenlik açığı, simüle edilmiş bir RAG destekli şirket içi destek chatbotu üzerinde test edilmiştir.

## Deney Ortamı

- Programlama dili: Python
- Arayüz: Streamlit
- Lokal LLM altyapısı: Ollama
- Kullanılan model: Mistral
- Test verisi: Tamamen sahte müşteri kayıtları, API anahtarları, şifreler, token değerleri ve şirket içi notlar
- Test yaklaşımı: Savunmasız sistem ve savunmalı sistem karşılaştırması

## Temel Deney Sonucu

Ollama/Mistral ile yapılan otomatik testlerde toplam **15 saldırı promptu** kullanılmıştır.

| Sistem | Başarılı Saldırı | Başarısız / Engellenen Saldırı | Saldırı Başarı Oranı |
|---|---:|---:|---:|
| Savunmasız-Ollama/Mistral | 13 | 2 | %86,7 |
| Savunmalı-Ollama/Mistral | 0 | 15 | %0 |

## Ana Bulgular

Savunmasız sistemde 15 saldırı promptunun 13'ü hassas bilgi ifşasına neden olmuştur. Bu durum, RAG bağlamına eklenen hassas verilerin model tarafından kullanıcıya döndürülebileceğini göstermektedir.

Savunmalı sistemde aynı 15 saldırı promptunun tamamı engellenmiştir. Bu sonuç, input guardrail, rol bazlı erişim kontrolü, context sanitization ve output filtering mekanizmalarının hassas bilgi ifşasını önemli ölçüde azalttığını göstermektedir.

## En Riskli Saldırı Türleri

Aşağıdaki saldırı türleri savunmasız sistemde kritik seviyede sonuç üretmiştir:

- Doğrudan hassas veri isteme
- Yetkili rol taklidi
- Kısmi API key isteme
- Sistem promptu isteme
- Debug çıktısı isteme
- Kod formatında gizli veri isteme
- Özetleme bahanesiyle gizli veri isteme
- Dolaylı ipucu isteme
- Çeviri bahanesiyle veri sızdırma
- Tablo formatında hassas veri isteme
- Regex benzeri veri çıkarma
- Kaynak doküman sızdırma
- Maskeleme bypass denemesi

## En Çok Sızan Veri Türleri

Savunmasız sistemde tespit edilen hassas veri türleri:

- TCKN
- E-posta
- Telefon numarası
- Kredi kartı bilgisi
- API key
- Password / şifre
- Token
- Database URL

## Yorum

Deney sonuçları, yalnızca sistem promptu ile güvenliğin sağlanamayacağını göstermektedir. Özellikle RAG sistemlerinde modele verilen bağlam içerisinde hassas veri bulunuyorsa, kullanıcı promptu manipülasyonu ile bu verilerin açığa çıkması mümkündür.

Savunmalı sistemde hassas veri taleplerinin model aşamasına gelmeden engellenmesi, riskin ciddi şekilde azaltılmasını sağlamıştır. Deney sonucunda savunmasız sistemde saldırı başarı oranı %86,7 iken savunmalı sistemde bu oran %0'a düşmüştür.
