import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from typing import List, Dict
from . import models

class FilmOneriSistemi:
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.kmeans_kullanicilar = KMeans(n_clusters=n_clusters)
        self.kmeans_filmler = KMeans(n_clusters=n_clusters)
        self.scaler = StandardScaler()
        self.kullanici_ozellikleri = {}
        self.film_ozellikleri = {}
        
    def film_ozelliklerini_olustur(self, db: Session):
        """Film özellik vektörlerini oluştur"""
        filmler = db.query(models.Film).all()
        ozellik_matrisi = []
        
        for film in filmler:
            ozellikler = []
            
            # Kategori ozellikleri (one-hot encoding)
            tum_kategoriler = db.query(models.Kategori).all()
            for kategori in tum_kategoriler:
                if kategori in film.kategoriler:
                    ozellikler.append(1)
                else:
                    ozellikler.append(0)
            
            # Film özellikleri
            ozellikler.extend([
                film.yil / 2023,  # Yıl normalizasyonu
                film.sure / 180,  # Süre normalizasyonu
                film.imdb_puani / 10  # IMDB puanı normalizasyonu
            ])
            
            # Ortalama kullanıcı puanı
            puanlar = [p.puan for p in film.puanlar]
            ort_puan = np.mean(puanlar) if puanlar else film.imdb_puani
            ozellikler.append(ort_puan / 5)  # Puan normalizasyonu
            
            # İzlenme sayısı
            izlenme_sayisi = len(film.izleme_gecmisi)
            ozellikler.append(izlenme_sayisi)  # Popülerlik göstergesi
            
            ozellik_matrisi.append(ozellikler)
            self.film_ozellikleri[film.id] = ozellikler
        
        # Özellikleri normalize et
        if ozellik_matrisi:
            normalized_features = self.scaler.fit_transform(ozellik_matrisi)
            
            # Filmleri kümelere ayır
            self.kmeans_filmler.fit(normalized_features)
            
            # Film kümelerini sakla
            for film_id, cluster in zip(self.film_ozellikleri.keys(), self.kmeans_filmler.labels_):
                self.film_ozellikleri[film_id] = {
                    'ozellikler': ozellik_matrisi[list(self.film_ozellikleri.keys()).index(film_id)],
                    'kume': cluster
                }
    
    def kullanici_ozelliklerini_olustur(self, db: Session):
        """Kullanıcı özellik vektörlerini oluştur"""
        kullanicilar = db.query(models.Kullanici).all()
        ozellik_matrisi = []
        
        for kullanici in kullanicilar:
            ozellikler = []
            
            # İzleme alışkanlıkları
            izleme_gecmisi = {g.film_id: g.izlenen_sure for g in kullanici.izleme_gecmisi}
            film_puanlari = {p.film_id: p.puan for p in kullanici.puanlar}
            
            # Kategori tercihleri
            kategori_puanlari = {}
            for film_id, sure in izleme_gecmisi.items():
                film = db.query(models.Film).filter(models.Film.id == film_id).first()
                if film:
                    for kategori in film.kategoriler:
                        # İzleme süresi ve puana göre kategori skoru hesapla
                        sure_skoru = sure / film.sure if film.sure else 0
                        puan_skoru = film_puanlari.get(film_id, 0) / 5
                        skor = (sure_skoru + puan_skoru) / 2
                        
                        if kategori.id in kategori_puanlari:
                            kategori_puanlari[kategori.id] += skor
                        else:
                            kategori_puanlari[kategori.id] = skor
            
            # Kategori skorlarını normalize et
            tum_kategoriler = db.query(models.Kategori).all()
            for kategori in tum_kategoriler:
                ozellikler.append(kategori_puanlari.get(kategori.id, 0))
            
            # İzleme ve puanlama yoğunluğu
            ozellikler.extend([
                len(izleme_gecmisi),  # Toplam izlenen film sayısı
                np.mean(list(film_puanlari.values())) if film_puanlari else 0  # Ortalama puan
            ])
            
            ozellik_matrisi.append(ozellikler)
            self.kullanici_ozellikleri[kullanici.id] = ozellikler
        
        # Özellikleri normalize et
        if ozellik_matrisi:
            normalized_features = self.scaler.fit_transform(ozellik_matrisi)
            
            # Kullanıcıları kümelere ayır
            self.kmeans_kullanicilar.fit(normalized_features)
            
            # Kullanıcı kümelerini sakla
            for kullanici_id, cluster in zip(self.kullanici_ozellikleri.keys(), self.kmeans_kullanicilar.labels_):
                self.kullanici_ozellikleri[kullanici_id] = {
                    'ozellikler': ozellik_matrisi[list(self.kullanici_ozellikleri.keys()).index(kullanici_id)],
                    'kume': cluster
                }
    
    def oneri_olustur(self, db: Session, kullanici_id: int, n_oneri: int = 5) -> List[models.Film]:
        """Kullanıcıya film önerileri oluştur"""
        # Özellikleri güncelle
        self.film_ozelliklerini_olustur(db)
        self.kullanici_ozelliklerini_olustur(db)
        
        # Kullanıcı var mı kontrol et
        if kullanici_id not in self.kullanici_ozellikleri:
            return []
        
        # Kullanıcının kümesini bul
        kullanici_kumesi = self.kullanici_ozellikleri[kullanici_id]['kume']
        
        # Kullanıcının izlediği filmler
        izlenen_filmler = {
            g.film_id for g in db.query(models.IzlemeGecmisi)
            .filter(models.IzlemeGecmisi.kullanici_id == kullanici_id)
            .all()
        }
        
        # Aynı kümedeki filmleri bul ve puanla
        film_puanlari = {}
        for film_id, film_data in self.film_ozellikleri.items():
            if film_id not in izlenen_filmler:  # Sadece izlenmemiş filmler
                # Film kullanıcının kümesiyle aynı kümede mi?
                film_kumesi = film_data['kume']
                
                # Küme benzerliğine göre puan ver
                kume_puani = 1.0 if film_kumesi == kullanici_kumesi else 0.5
                
                # Filmin özelliklerine göre ek puan
                film = db.query(models.Film).filter(models.Film.id == film_id).first()
                if film:
                    # IMDB puanı ve popülerliğe göre ek puan
                    imdb_puani = film.imdb_puani / 10
                    populerlik = len(film.izleme_gecmisi) / 100
                    
                    # Toplam puanı hesapla
                    toplam_puan = (kume_puani + imdb_puani + populerlik) / 3
                    film_puanlari[film_id] = toplam_puan
        
        # En yüksek puanlı filmleri seç
        onerilecek_film_idleri = sorted(
            film_puanlari.keys(),
            key=lambda x: film_puanlari[x],
            reverse=True
        )[:n_oneri]
        
        # Film objelerini getir
        onerilen_filmler = []
        for film_id in onerilecek_film_idleri:
            film = db.query(models.Film).filter(models.Film.id == film_id).first()
            if film:
                onerilen_filmler.append(film)
        
        return onerilen_filmler 