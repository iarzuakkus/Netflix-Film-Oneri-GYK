# Netflix Benzeri Film Öneri Sistemi

Bu proje, kullanıcıların film izleme alışkanlıklarına ve değerlendirmelerine dayalı olarak kişiselleştirilmiş film önerileri sunan bir API sistemidir.

## Özellikler

- Kullanıcı kaydı ve kimlik doğrulama
- Film ve kategori yönetimi
- İzleme geçmişi takibi
- Film puanlama sistemi
- K-means tabanlı kişiselleştirilmiş film önerileri
- FastAPI ile modern REST API

## Teknolojiler

- Python 3.8+
- FastAPI
- SQLAlchemy (PostgreSQL)
- scikit-learn (K-means kümeleme)
- Uvicorn (ASGI sunucusu)

## Proje yapısı

```
netflix/
│
├── main.py                 # Ana uygulama dosyası, FastAPI route'ları
├── database.py            # Veritabanı bağlantısı ve session yönetimi
├── recommendation.py      # K-means tabanlı film öneri sistemi
├── schemas.py             # Pydantic modelleri (request/response şemaları)
├── requirements.txt       # Proje bağımlılıkları
│
├── sql/                  # SQL dosyaları
│   ├── create_tables.sql  # Veritabanı tablo yapıları
│   ├── insert_movies.sql  # Film ve kategori örnek verileri
│   └── sample_user_data.sql # Kullanıcı, izleme geçmişi ve puan örnek verileri
│
└── README.md             # Proje dokümantasyonu
```

### Dosya İçerikleri

- **main.py**: FastAPI uygulaması ve endpoint tanımları
- **database.py**: 
  - SQLAlchemy veritabanı bağlantı ayarları
  - PostgreSQL bağlantı bilgileri (kullanıcı, şifre, port vb.)
  - Veritabanı session yönetimi
  - Base model sınıfı tanımı
  - Database bağlantı dependency'si (FastAPI için)
- **recommendation.py**:
  - K-means tabanlı film öneri sistemi
  - Film ve kullanıcı özelliklerinin çıkarılması
  - Kümeleme işlemleri
  - Öneri algoritması
- **schemas.py**: API request ve response modellerinin tanımları
- **sql/create_tables.sql**: 
  - Kullanıcılar tablosu (id, kullanici_adi, email, sifre_hash)
  - Filmler tablosu (id, baslik, aciklama, yil, sure, imdb_puani)
  - Kategoriler tablosu (id, ad)
  - Film-Kategori ilişki tablosu
  - İzleme geçmişi tablosu (kullanici_id, film_id, izlenen_sure)
  - Puanlar tablosu (kullanici_id, film_id, puan)

- **sql/insert_movies.sql**:
  - Örnek film verileri
  - Film kategorileri
  - Film-kategori ilişkileri

- **sql/sample_user_data.sql**:
  - Test kullanıcıları (farklı film tercihleri olan)
  - İzleme geçmişi kayıtları
  - Film puanlamaları

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. PostgreSQL veritabanını oluşturun:
```sql
-- PostgreSQL'de veritabanını oluşturun
CREATE DATABASE netflix;
```

3. Veritabanı tablolarını oluşturun:
```bash
# sql/create_tables.sql dosyasını çalıştırın
psql -d netflix -f sql/create_tables.sql
```

4. Örnek verileri yükleyin:
```bash
# Önce filmleri ve kategorileri ekleyin
psql -d netflix -f sql/insert_movies.sql

# Sonra örnek kullanıcı verilerini ekleyin
psql -d netflix -f sql/sample_user_data.sql
```

## Çalıştırma

Uygulamayı başlatmak için:

```bash
python -m uvicorn main:app --reload
```

API dokümantasyonuna erişmek için:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoint'leri

### Kullanıcı İşlemleri
- `POST /kullanicilar/`: Yeni kullanıcı oluşturma
- `GET /kullanicilar/`: Tüm kullanıcıları listeleme

### Film İşlemleri
- `POST /filmler/`: Yeni film ekleme
- `GET /filmler/`: Tüm filmleri listeleme
- `GET /filmler/{film_id}`: Belirli bir filmin detaylarını getirme

### Öneri Sistemi
- `GET /film-onerileri/{kullanici_id}`: Kullanıcıya özel film önerileri alma
  - Query parametresi `n_oneri`: Kaç öneri istediğinizi belirtin (varsayılan: 5)

### İzleme Geçmişi
- `POST /izleme_gecmisi/`: İzleme kaydı ekleme

### Puanlama
- `POST /puanlar/`: Film puanlama

## Öneri Sistemi Nasıl Çalışır?

Sistem, K-means kümeleme algoritması kullanarak hem filmleri hem de kullanıcıları benzer gruplara ayırır ve bu grupları kullanarak öneriler oluşturur.

### Film Kümeleme
1. Her film için özellik vektörü oluşturulur:
   - Kategori bilgileri (one-hot encoding)
   - Yıl (normalize edilmiş)
   - Süre (normalize edilmiş)
   - IMDB puanı
   - Kullanıcı puanları ortalaması
   - İzlenme sayısı (popülerlik)

2. Filmler 5 kümeye ayrılır (varsayılan)

### Kullanıcı Kümeleme
1. Her kullanıcı için özellik vektörü oluşturulur:
   - Kategori tercihleri (izleme süresi ve puanlara göre)
   - Toplam izlenen film sayısı
   - Ortalama verdiği puan
   - İzleme süreleri

2. Kullanıcılar 5 kümeye ayrılır (varsayılan)

### Öneri Oluşturma Süreci
1. Kullanıcının hangi kümede olduğu belirlenir
2. Kullanıcının izlemediği filmler arasından:
   - Aynı kümede olan filmler daha yüksek puan alır
   - IMDB puanı yüksek filmler tercih edilir
   - Popüler filmler tercih edilir
3. En yüksek puanı alan filmler önerilir

### Avantajları
- Benzer kullanıcıları ve filmleri gruplar
- Kategori, puan ve izleme süresi gibi çoklu faktörleri değerlendirir
- Yeni kullanıcılar için de çalışabilir (cold start problemi)
- Ölçeklenebilir ve hızlı

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun
