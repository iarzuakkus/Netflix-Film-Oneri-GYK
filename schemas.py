from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FilmBase(BaseModel):
    baslik: str
    aciklama: str
    yil: int
    sure: int
    imdb_puani: float
    resim_url: str

    class Config:
        from_attributes = True

class FilmBrief(FilmBase):
    id: int

class KategoriBase(BaseModel):
    id: int
    ad: str

    class Config:
        from_attributes = True

class Kategori(KategoriBase):
    filmler: List[FilmBrief]

class Film(FilmBase):
    id: int
    kategoriler: List[KategoriBase]

class FilmCreate(FilmBase):
    kategori_ids: List[int]

class Kullanici(BaseModel):
    id: int
    kullanici_adi: str
    email: str
    sifre: str

    class Config:
        from_attributes = True

class IzlemeGecmisi(BaseModel):
    id: int
    kullanici_id: int
    film_id: int
    izlenen_sure: int

    class Config:
        from_attributes = True

class Puan(BaseModel):
    id: int
    kullanici_id: int
    film_id: int
    puan: int

    class Config:
        from_attributes = True 