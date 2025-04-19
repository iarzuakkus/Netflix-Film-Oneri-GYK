-- Kategoriler
INSERT INTO kategoriler (ad) VALUES
('Aksiyon'),
('Dram'),
('Bilim Kurgu'),
('Fantastik'),
('Macera');

-- Filmler
INSERT INTO filmler (baslik, aciklama, yil, sure, imdb_puani, resim_url) VALUES
('Inception', 'Rüyalar içinde geçen bir bilim kurgu filmi', 2010, 148, 8.8, 'https://example.com/inception.jpg'),
('The Dark Knight', 'Batman''in Joker ile mücadelesi', 2008, 152, 9.0, 'https://example.com/dark_knight.jpg'),
('Forrest Gump', 'Sıra dışı bir adamın hayat hikayesi', 1994, 142, 8.8, 'https://example.com/forrest_gump.jpg'),
('Matrix', 'Simülasyon dünyasında geçen bir film', 1999, 136, 8.7, 'https://example.com/matrix.jpg'),
('The Lord of the Rings', 'Yüzüklerin Efendisi: Yüzük Kardeşliği', 2001, 178, 8.8, 'https://example.com/lotr.jpg');

-- Film-Kategori İlişkileri
INSERT INTO film_kategori (film_id, kategori_id) VALUES
(1, 1), -- Inception: Aksiyon
(1, 3), -- Inception: Bilim Kurgu
(2, 1), -- Dark Knight: Aksiyon
(2, 2), -- Dark Knight: Dram
(3, 2), -- Forrest Gump: Dram
(4, 1), -- Matrix: Aksiyon
(4, 3), -- Matrix: Bilim Kurgu
(5, 4), -- LOTR: Fantastik
(5, 5); -- LOTR: Macera 