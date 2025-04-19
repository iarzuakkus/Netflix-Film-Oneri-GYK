from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from netflix import models
from netflix import schemas
from netflix.database import engine, get_db
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Netflix API")

class FilmOneriSistemi:
    def __init__(self):
        self.film_ozellikleri = {}  # Film özellik matrisi
        self.film_indeksleri = {}   # Film ID'lerinin indeks eşlemesi
        
    def film_ozelliklerini_olustur(self, db: Session):
        """Film özelliklerini oluştur: kategoriler, ortalama puan, izlenme sayısı"""
        filmler = db.query(models.Film).all()
        self.film_indeksleri = {film.id: idx for idx, film in enumerate(filmler)}
        
        # Her film için özellik vektörü oluştur
        ozellik_matrisi = []
        for film in filmler:
            ozellikler = []
            
            # Kategori özellikleri (one-hot encoding)
            tum_kategoriler = db.query(models.Kategori).all()
            for kategori in tum_kategoriler:
                if kategori in film.kategoriler:
                    ozellikler.append(1)
                else:
                    ozellikler.append(0)
            
            # Ortalama puan
            puanlar = [p.puan for p in film.puanlar]
            ort_puan = np.mean(puanlar) if puanlar else film.imdb_puani
            ozellikler.append(ort_puan)
            
            # İzlenme sayısı
            izlenme_sayisi = len(film.izleme_gecmisi)
            ozellikler.append(izlenme_sayisi)
            
            # Yıl ve süre
            ozellikler.append(film.yil / 2023)  # Normalize et
            ozellikler.append(film.sure / 180)   # Normalize et
            
            ozellik_matrisi.append(ozellikler)
        
        self.film_ozellikleri = np.array(ozellik_matrisi)
    
    def kullanici_tercihlerini_hesapla(self, db: Session, kullanici_id: int):
        """Kullanıcının film tercihlerini hesapla"""
        kullanici = db.query(models.Kullanici).filter(models.Kullanici.id == kullanici_id).first()
        if not kullanici:
            return None
            
        # Kullanıcının izlediği ve puanladığı filmler
        izlenen_filmler = {g.film_id: g.izlenen_sure for g in kullanici.izleme_gecmisi}
        puanlanan_filmler = {p.film_id: p.puan for p in kullanici.puanlar}
        
        # Kullanıcı profili oluştur
        kullanici_profili = np.zeros_like(self.film_ozellikleri[0])
        for film_id, sure in izlenen_filmler.items():
            if film_id in self.film_indeksleri:
                idx = self.film_indeksleri[film_id]
                agirlik = sure / 180  # İzlenme süresine göre ağırlık
                if film_id in puanlanan_filmler:
                    agirlik *= puanlanan_filmler[film_id] / 5  # Puana göre ağırlık
                kullanici_profili += self.film_ozellikleri[idx] * agirlik
        
        return kullanici_profili
    
    def oneri_olustur(self, db: Session, kullanici_id: int, n_oneri: int = 5):
        """Kullanıcıya film önerileri oluştur"""
        # Film özelliklerini güncelle
        self.film_ozelliklerini_olustur(db)
        
        # Kullanıcı profilini al
        kullanici_profili = self.kullanici_tercihlerini_hesapla(db, kullanici_id)
        if kullanici_profili is None:
            return []
            
        # Kullanıcı profili ile tüm filmler arasındaki benzerliği hesapla
        film_benzerlikleri = cosine_similarity([kullanici_profili], self.film_ozellikleri)[0]
        
        # En benzer filmleri bul
        en_benzer_indeksler = np.argsort(film_benzerlikleri)[::-1]
        
        # Kullanıcının izlemediği filmleri öner
        kullanici = db.query(models.Kullanici).filter(models.Kullanici.id == kullanici_id).first()
        izlenen_filmler = {g.film_id for g in kullanici.izleme_gecmisi}
        
        oneriler = []
        for idx in en_benzer_indeksler:
            film_id = list(self.film_indeksleri.keys())[list(self.film_indeksleri.values()).index(idx)]
            if film_id not in izlenen_filmler:
                film = db.query(models.Film).filter(models.Film.id == film_id).first()
                oneriler.append(film)
                if len(oneriler) >= n_oneri:
                    break
        
        return oneriler

# Öneri sistemi örneği oluştur
oneri_sistemi = FilmOneriSistemi()

# Kullanıcı işlemleri
@app.post("/kullanicilar/", response_model=schemas.Kullanici)
def kullanici_olustur(kullanici: schemas.Kullanici, db: Session = Depends(get_db)):
    db_kullanici = models.Kullanici(
        kullanici_adi=kullanici.kullanici_adi,
        email=kullanici.email,
        sifre_hash=kullanici.sifre
    )
    db.add(db_kullanici)
    db.commit()
    db.refresh(db_kullanici)
    return db_kullanici

@app.get("/kullanicilar/", response_model=List[schemas.Kullanici])
def kullanicilari_listele(db: Session = Depends(get_db)):
    return db.query(models.Kullanici).all()

# Film işlemleri
@app.post("/filmler/", response_model=schemas.Film)
def film_olustur(film: schemas.FilmCreate, db: Session = Depends(get_db)):
    db_film = models.Film(
        baslik=film.baslik,
        aciklama=film.aciklama,
        yil=film.yil,
        sure=film.sure,
        imdb_puani=film.imdb_puani,
        resim_url=film.resim_url
    )
    
    # Kategorileri ekle
    for kategori_id in film.kategori_ids:
        kategori = db.query(models.Kategori).filter(models.Kategori.id == kategori_id).first()
        if kategori:
            db_film.kategoriler.append(kategori)
    
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film

@app.get("/filmler/", response_model=List[schemas.Film])
def filmleri_listele(db: Session = Depends(get_db)):
    return db.query(models.Film).all()

@app.get("/filmler/{film_id}", response_model=schemas.Film)
def film_getir(film_id: int, db: Session = Depends(get_db)):
    db_film = db.query(models.Film).filter(models.Film.id == film_id).first()
    if db_film is None:
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    return db_film

# Kategori işlemleri
@app.post("/kategoriler/", response_model=schemas.Kategori)
def kategori_olustur(kategori: schemas.Kategori, db: Session = Depends(get_db)):
    db_kategori = models.Kategori(ad=kategori.ad)
    db.add(db_kategori)
    db.commit()
    db.refresh(db_kategori)
    return db_kategori

@app.get("/kategoriler/", response_model=List[schemas.Kategori])
def kategorileri_listele(db: Session = Depends(get_db)):
    return db.query(models.Kategori).all()

# İzleme geçmişi işlemleri
@app.post("/izleme_gecmisi/", response_model=schemas.IzlemeGecmisi)
def izleme_ekle(izleme: schemas.IzlemeGecmisi, db: Session = Depends(get_db)):
    db_izleme = models.IzlemeGecmisi(
        kullanici_id=izleme.kullanici_id,
        film_id=izleme.film_id,
        izlenen_sure=izleme.izlenen_sure
    )
    db.add(db_izleme)
    db.commit()
    db.refresh(db_izleme)
    return db_izleme

# Puan işlemleri
@app.post("/puanlar/", response_model=schemas.Puan)
def puan_ekle(puan: schemas.Puan, db: Session = Depends(get_db)):
    db_puan = models.Puan(
        kullanici_id=puan.kullanici_id,
        film_id=puan.film_id,
        puan=puan.puan
    )
    db.add(db_puan)
    db.commit()
    db.refresh(db_puan)
    return db_puan

@app.get("/film-onerileri/{kullanici_id}", response_model=List[schemas.Film])
def film_onerileri(kullanici_id: int, n_oneri: int = 5, db: Session = Depends(get_db)):
    """Kullanıcıya özel film önerileri oluştur"""
    # Kullanıcının varlığını kontrol et
    kullanici = db.query(models.Kullanici).filter(models.Kullanici.id == kullanici_id).first()
    if not kullanici:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    # Öneri oluştur
    onerilen_filmler = oneri_sistemi.oneri_olustur(db, kullanici_id, n_oneri)
    return onerilen_filmler 