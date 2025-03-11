# Backend Yapı Analizi

## Genel Mimari

Backend yapınız FastAPI tabanlı bir REST API olarak tasarlanmış. Modern bir Python web framework'ü olan FastAPI kullanılarak geliştirilmiş ve aşağıdaki temel bileşenleri içeriyor:

1. **Veritabanı**: PostgreSQL veritabanı kullanılıyor ve SQLAlchemy ORM ile etkileşim sağlanıyor.
2. **Kimlik Doğrulama**: JWT tabanlı kimlik doğrulama sistemi ve Google OAuth entegrasyonu mevcut.
3. **Docker Desteği**: Hem geliştirme hem de üretim ortamları için Docker yapılandırmaları bulunuyor.
4. **Veritabanı Migrasyonları**: Alembic kullanılarak veritabanı şema değişiklikleri yönetiliyor.
5. **Besin Değerleri API**: USDA FoodData Central veritabanından alınan besin değerleri bilgilerini sunan API endpoint'leri.

## Dosya Yapısı

```
backend/
├── __pycache__/
├── alembic/                # Veritabanı migrasyon yönetimi
├── app/                    # Ana uygulama kodu
│   ├── __pycache__/
│   ├── routers/            # API endpoint'leri
│   │   ├── auth.py         # Kimlik doğrulama
│   │   ├── google_auth.py  # Google OAuth entegrasyonu
│   │   ├── post.py         # Post işlemleri
│   │   ├── user.py         # Kullanıcı işlemleri
│   │   ├── vote.py         # Oy verme işlemleri
│   │   └── food.py         # Besin değerleri işlemleri
│   ├── config.py           # Uygulama yapılandırması
│   ├── database.py         # Veritabanı bağlantısı
│   ├── main.py             # Ana uygulama giriş noktası
│   ├── models.py           # Veritabanı modelleri
│   ├── oauth2.py           # JWT kimlik doğrulama
│   ├── schemas.py          # Pydantic modelleri (API şemaları)
│   └── utils.py            # Yardımcı fonksiyonlar
├── venv/                   # Python sanal ortamı
├── .env                    # Ortam değişkenleri
├── alembic.ini             # Alembic yapılandırması
├── docker-compose-dev.yml  # Geliştirme Docker yapılandırması
├── docker-compose-prod.yml # Üretim Docker yapılandırması
├── Dockerfile              # Docker imaj yapılandırması
├── food_query.py           # Besin değerleri sorgulama script'i
└── requirements.txt        # Python bağımlılıkları
```

## Veri Modelleri

Üç ana veri modeli tanımlanmış:

1. **Post**: İçerik paylaşımları için

   - Başlık, içerik, yayınlanma durumu, oluşturma zamanı ve sahip bilgisi içeriyor
   - Kullanıcı ile ilişkilendirilmiş

2. **User**: Kullanıcı hesapları için

   - E-posta, şifre, oluşturma zamanı, Google kullanıcısı olup olmadığı ve telefon numarası bilgilerini içeriyor

3. **Vote**: Kullanıcıların postlara oy vermesi için

   - Kullanıcı ID ve post ID ile ilişkilendirilmiş

4. **Food**: Yiyecek bilgileri için
5. **Nutrient**: Besin öğeleri bilgileri için
6. **FoodNutrient**: Yiyecek-besin ilişkileri için

## Besin Değerleri API

Yeni eklenen besin değerleri API'si, USDA FoodData Central veritabanından alınan verileri kullanarak yiyeceklerin besin değerleri bilgilerini sunar. API aşağıdaki endpoint'leri içerir:

- `GET /food/`: Yiyecekleri listeler ve arama yapar
- `GET /food/{fdc_id}`: Belirli bir yiyeceğin detaylarını getirir
- `GET /food/{fdc_id}/nutrients`: Bir yiyeceğin tüm besin değerlerini getirir
- `GET /food/{fdc_id}/macronutrients`: Bir yiyeceğin makro besin değerlerini getirir (kalori, protein, yağ, karbonhidrat)
- `GET /food/{fdc_id}/micronutrients`: Bir yiyeceğin mikro besin değerlerini getirir (vitaminler ve mineraller)
- `GET /food/{fdc_id}/phytochemicals`: Bir yiyeceğin fitokimyasal bileşenlerini getirir
- `GET /food/{fdc_id}/summary`: Bir yiyeceğin tüm besin değerlerinin özetini getirir

## Besin Değerleri Sorgulama Script'i

`food_query.py` script'i, besin değerleri API'sini kullanarak terminal üzerinden yiyeceklerin besin değerlerini sorgulamayı sağlar. Kullanımı:

```
python food_query.py <yiyecek_adı>
```

Script, belirtilen yiyecek adına göre arama yapar ve bulunan yiyecekleri listeler. Kullanıcı, listeden bir yiyecek seçerek detaylı besin değerleri bilgilerini görüntüleyebilir.

## API Endpoint'leri

1. **Kullanıcı İşlemleri**:

   - Kullanıcı oluşturma
   - Kullanıcı bilgilerini getirme

2. **Kimlik Doğrulama**:

   - JWT token ile giriş
   - Google OAuth ile giriş

3. **Post İşlemleri**:

   - Post oluşturma, okuma, güncelleme ve silme (CRUD)
   - Filtreleme, sayfalama ve arama özellikleri

4. **Oy İşlemleri**:
   - Post'lara oy verme/oy kaldırma

## Güvenlik Özellikleri

- Şifreler bcrypt ile hashleniyor
- JWT tabanlı kimlik doğrulama
- Google OAuth entegrasyonu
- Yetkilendirme kontrolleri (kullanıcılar sadece kendi postlarını düzenleyebilir/silebilir)

## Docker Yapılandırması

- Geliştirme ortamı için hot-reload özellikli yapılandırma
- Üretim ortamı için optimize edilmiş yapılandırma
- PostgreSQL veritabanı için container

## Güçlü Yönler

1. **Modern Teknolojiler**: FastAPI, Pydantic, SQLAlchemy gibi modern Python kütüphaneleri kullanılmış.
2. **Güvenlik**: JWT ve OAuth entegrasyonu ile güçlü kimlik doğrulama.
3. **Konteynerizasyon**: Docker ile kolay dağıtım ve ölçeklendirme.
4. **Veritabanı Migrasyonları**: Alembic ile veritabanı şema değişikliklerinin yönetimi.
5. **Modüler Yapı**: Router'lar ile modüler ve bakımı kolay kod yapısı.

## Geliştirilebilecek Alanlar

1. **Test Kodu**: Test dosyaları göremedim, birim ve entegrasyon testleri eklenebilir.
2. **Dokümantasyon**: API dokümantasyonu için daha fazla açıklama eklenebilir.
3. **Hata İşleme**: Daha kapsamlı hata işleme mekanizmaları eklenebilir.
4. **Loglama**: Sistematik loglama mekanizması eklenebilir.
5. **Rate Limiting**: API isteklerini sınırlandırma mekanizması eklenebilir.
