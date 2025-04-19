from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from netflix import models
from netflix import schemas
from netflix.database import engine, get_db
from netflix.recommendation import FilmOneriSistemi

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Netflix API")

# Öneri sistemi örneği oluştur
oneri_sistemi = FilmOneriSistemi(n_clusters=5)

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
    
    # K-means tabanlı öneri sistemini kullan
    onerilen_filmler = oneri_sistemi.oneri_olustur(db, kullanici_id, n_oneri)
    return onerilen_filmler 