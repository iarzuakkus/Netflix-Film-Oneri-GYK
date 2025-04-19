from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from netflix.database import Base

# Film-Kategori ilişki tablosu (many-to-many ilişki için)
film_kategori = Table('film_kategori',
    Base.metadata,
    Column('film_id', Integer, ForeignKey('filmler.id')),
    Column('kategori_id', Integer, ForeignKey('kategoriler.id'))
)

class Kullanici(Base):
    __tablename__ = 'kullanicilar'
    
    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    sifre_hash = Column(String)
    
    # İlişkiler
    izleme_gecmisi = relationship("IzlemeGecmisi", back_populates="kullanici")
    puanlar = relationship("Puan", back_populates="kullanici")

class Film(Base):
    __tablename__ = 'filmler'
    
    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String, index=True)
    aciklama = Column(String)
    yil = Column(Integer)
    sure = Column(Integer)  # dakika cinsinden
    imdb_puani = Column(Float)
    resim_url = Column(String)
    
    # iliskiler
    kategoriler = relationship("Kategori", secondary=film_kategori, back_populates="filmler")
    izleme_gecmisi = relationship("IzlemeGecmisi", back_populates="film")
    puanlar = relationship("Puan", back_populates="film")

class Kategori(Base):
    __tablename__ = 'kategoriler'
    
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, unique=True, index=True)
    
    # İlişkiler
    filmler = relationship("Film", secondary=film_kategori, back_populates="kategoriler")

class IzlemeGecmisi(Base):
    __tablename__ = 'izleme_gecmisi'
    
    id = Column(Integer, primary_key=True, index=True)
    kullanici_id = Column(Integer, ForeignKey('kullanicilar.id'))
    film_id = Column(Integer, ForeignKey('filmler.id'))
    izlenen_sure = Column(Integer)  # dakika cinsinden
    
    # İlişkiler
    kullanici = relationship("Kullanici", back_populates="izleme_gecmisi")
    film = relationship("Film", back_populates="izleme_gecmisi")

class Puan(Base):
    __tablename__ = 'puanlar'
    
    id = Column(Integer, primary_key=True, index=True)
    kullanici_id = Column(Integer, ForeignKey('kullanicilar.id'))
    film_id = Column(Integer, ForeignKey('filmler.id'))
    puan = Column(Integer)  # 1-5 arası
    
    # İlişkiler
    kullanici = relationship("Kullanici", back_populates="puanlar")
    film = relationship("Film", back_populates="puanlar") 