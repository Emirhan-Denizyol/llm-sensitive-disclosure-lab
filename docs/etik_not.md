# Etik Not ve Sınırlılıklar

Bu çalışma, **Büyük Dil Modellerinde Siber Güvenlik** dersi final ödevi kapsamında eğitim ve araştırma amacıyla hazırlanmıştır.

## Etik Kapsam

Bu projede kullanılan tüm veriler tamamen sahte olarak oluşturulmuştur.

Kullanılan veri türleri:

- Sahte müşteri adları
- Sahte TCKN değerleri
- Sahte telefon numaraları
- Sahte e-posta adresleri
- Sahte kredi kartı numaraları
- Sahte API key değerleri
- Sahte admin şifreleri
- Sahte token değerleri
- Sahte veritabanı bağlantı adresleri

Gerçek kişi, gerçek kurum, gerçek müşteri veya gerçek sistem verisi kullanılmamıştır.

## Kontrollü Test Ortamı

Tüm testler lokal bilgisayarda çalışan kontrollü bir test ortamında gerçekleştirilmiştir.

Kullanılan ortam:

- Lokal Python uygulaması
- Streamlit arayüzü
- Ollama üzerinde çalışan lokal Mistral modeli
- Sahte RAG dokümanları

Gerçek sistemlere saldırı yapılmamıştır.

## Amaç

Bu çalışmanın amacı gerçek bir sisteme zarar vermek değil, LLM tabanlı sistemlerde **Sensitive Information Disclosure** açığının nasıl oluşabileceğini ve hangi savunma mekanizmalarıyla azaltılabileceğini göstermektir.

## Hukuki Sınırlılık

Bu çalışma kapsamında:

- Gerçek kişisel veri işlenmemiştir.
- Gerçek API anahtarı kullanılmamıştır.
- Gerçek şifre veya erişim bilgisi kullanılmamıştır.
- Gerçek müşteri verisi kullanılmamıştır.
- Üçüncü taraf sistemlere saldırı yapılmamıştır.
- Yetkisiz erişim denenmemiştir.

## Akademik Sınırlılıklar

Bu proje bir eğitim laboratuvarıdır. Üretim ortamı güvenliği için tek başına yeterli değildir.

Başlıca sınırlılıklar:

- Hassas veri tespiti regex tabanlıdır.
- Kullanılan RAG sistemi basitleştirilmiştir.
- Gerçek vektör veritabanı tabanlı retrieval davranışları sınırlı şekilde simüle edilmiştir.
- Model davranışı deterministik değildir.
- Farklı LLM modellerinde sonuçlar değişebilir.
- Gerçek kurum sistemlerinde daha kapsamlı erişim kontrolü gerekir.

## Güvenli Kullanım İlkesi

Bu projede yer alan saldırı promptları yalnızca kontrollü, izinli ve sahte veri içeren ortamlarda kullanılmalıdır. Gerçek sistemlerden veri çıkarmak, gerçek kişisel verileri ifşa etmek veya yetkisiz erişim sağlamak etik ve hukuki açıdan uygun değildir.

## Sonuç

Çalışma, LLM tabanlı sistemlerde hassas bilgi ifşası riskinin gerçekçi bir simülasyonla gösterilebileceğini ve çok katmanlı savunma mekanizmalarıyla bu riskin azaltılabileceğini ortaya koymaktadır.
