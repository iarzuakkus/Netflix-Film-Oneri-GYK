-- Kullanıcılar
INSERT INTO kullanicilar (kullanici_adi, email, sifre_hash) VALUES
('aksiyon_sever', 'aksiyon@example.com', 'test123'),
('dram_sever', 'dram@example.com', 'test123'),
('bilimkurgu_sever', 'scifi@example.com', 'test123'),
('fantastik_sever', 'fantasy@example.com', 'test123'),
('hepsi_sever', 'all@example.com', 'test123');

-- İzleme geçmişi
INSERT INTO izleme_gecmisi (kullanici_id, film_id, izlenen_sure) VALUES
-- Aksiyon sever (id=1)
(1, 1, 148),  -- Inception tam izlemiş
(1, 2, 152),  -- Dark Knight tam izlemiş
(1, 4, 136),  -- Matrix tam izlemiş

-- Dram sever (id=2)
(2, 2, 152),  -- Dark Knight tam izlemiş
(2, 3, 142),  -- Forrest Gump tam izlemiş
(2, 1, 60),   -- Inception yarım bırakmış

-- Bilimkurgu sever (id=3)
(3, 1, 148),  -- Inception tam izlemiş
(3, 4, 136),  -- Matrix tam izlemiş
(3, 2, 30),   -- Dark Knight başlayıp bırakmış

-- Fantastik sever (id=4)
(3, 5, 178),  -- LOTR tam izlemiş
(3, 1, 80),   -- Inception yarım bırakmış
(3, 3, 70),   -- Forrest Gump yarım bırakmış

-- Hepsi sever (id=5)
(5, 1, 148),  -- Inception tam izlemiş
(5, 2, 152),  -- Dark Knight tam izlemiş
(5, 3, 142),  -- Forrest Gump tam izlemiş
(5, 4, 136),  -- Matrix tam izlemiş
(5, 5, 178);  -- LOTR tam izlemiş

-- Film puanları
INSERT INTO puanlar (kullanici_id, film_id, puan) VALUES
-- Aksiyon sever
(1, 1, 5),  -- Inception
(1, 2, 5),  -- Dark Knight
(1, 4, 5),  -- Matrix

-- Dram sever
(2, 2, 5),  -- Dark Knight
(2, 3, 5),  -- Forrest Gump
(2, 1, 2),  -- Inception

-- Bilimkurgu sever
(3, 1, 5),  -- Inception
(3, 4, 5),  -- Matrix
(3, 2, 2),  -- Dark Knight

-- Fantastik sever
(4, 5, 5),  -- LOTR
(4, 1, 3),  -- Inception
(4, 3, 3),  -- Forrest Gump

-- Hepsi sever
(5, 1, 4),  -- Inception
(5, 2, 4),  -- Dark Knight
(5, 3, 4),  -- Forrest Gump
(5, 4, 4),  -- Matrix
(5, 5, 4);  -- LOTR 