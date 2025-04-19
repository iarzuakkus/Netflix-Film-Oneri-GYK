-- Veritabanı şeması
CREATE TABLE kullanicilar (
    id SERIAL PRIMARY KEY,
    kullanici_adi VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    sifre_hash VARCHAR(255) NOT NULL,
    olusturulma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE kategoriler (
    id SERIAL PRIMARY KEY,
    ad VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE filmler (
    id SERIAL PRIMARY KEY,
    baslik VARCHAR(100) NOT NULL,
    aciklama TEXT,
    yil INTEGER,
    sure INTEGER,
    imdb_puani FLOAT,
    resim_url VARCHAR(255)
);

CREATE TABLE film_kategori (
    film_id INTEGER REFERENCES filmler(id),
    kategori_id INTEGER REFERENCES kategoriler(id),
    PRIMARY KEY (film_id, kategori_id)
);

CREATE TABLE izleme_gecmisi (
    id SERIAL PRIMARY KEY,
    kullanici_id INTEGER REFERENCES kullanicilar(id),
    film_id INTEGER REFERENCES filmler(id),
    izleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    izlenen_sure INTEGER
);

CREATE TABLE puanlar (
    id SERIAL PRIMARY KEY,
    kullanici_id INTEGER REFERENCES kullanicilar(id),
    film_id INTEGER REFERENCES filmler(id),
    puan INTEGER CHECK (puan >= 1 AND puan <= 5),
    puan_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 