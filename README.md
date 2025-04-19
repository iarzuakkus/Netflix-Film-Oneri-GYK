# Netflix Benzeri Film Öneri Sistemi

Bu proje, kullanıcıların film izleme alışkanlıklarına ve değerlendirmelerine dayalı olarak kişiselleştirilmiş film önerileri sunan bir API sistemidir.

## Özellikler

- Kullanıcı kaydı ve kimlik doğrulama
- Film ve kategori yönetimi
- İzleme geçmişi takibi
- Film puanlama sistemi
- Kişiselleştirilmiş film önerileri
- FastAPI ile modern REST API

## Teknolojiler

- Python 3.8+
- FastAPI
- SQLAlchemy (PostgreSQL)
- scikit-learn (Öneri sistemi için)
- Uvicorn (ASGI sunucusu)

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

Sistem şu faktörleri göz önünde bulundurarak öneriler oluşturur:
1. Kullanıcının izlediği filmlerin kategorileri
2. İzleme süreleri (filmi ne kadar tamamladığı)
3. Kullanıcının verdiği puanlar
4. Film özellikleri (yıl, süre, IMDB puanı)

Öneriler, cosine similarity kullanılarak hesaplanır ve kullanıcının daha önce izlemediği filmler arasından seçilir.

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun 