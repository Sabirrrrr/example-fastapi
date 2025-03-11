from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func, text, inspect
import logging
import traceback

from .. import models, schemas
from ..database import get_db

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Router tanımı - özel yollar için ayrı bir router oluşturuyoruz
router = APIRouter(prefix="/food", tags=['Food'])

# Test endpoint'i
@router.get("/test", include_in_schema=True)
def test_endpoint():
    return {"message": "API çalışıyor!"}

# Tüm yiyecekleri listele
@router.get("/")
def get_foods(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    try:
        logger.info(f"Yiyecek araması başlatılıyor: '{search}'")
        
        # Önce tabloların varlığını kontrol et
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        logger.info(f"Mevcut tablolar: {tables}")
        
        if 'food' not in tables:
            logger.error("'food' tablosu veritabanında bulunamadı!")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="'food' tablosu veritabanında bulunamadı!")
        
        # Tablo yapısını kontrol et
        columns = [c['name'] for c in inspector.get_columns('food')]
        logger.info(f"'food' tablosu sütunları: {columns}")
        
        # Sorguyu oluştur
        logger.info("Sorgu oluşturuluyor...")
        query = db.query(models.Food)
        
        # Filtreleme
        logger.info(f"Filtreleme uygulanıyor: description LIKE '%{search}%'")
        query = query.filter(models.Food.description.contains(search))
        
        # Limit ve offset
        logger.info(f"Limit: {limit}, Offset: {skip} uygulanıyor")
        query = query.limit(limit).offset(skip)
        
        # Sorguyu çalıştır
        logger.info("Sorgu çalıştırılıyor...")
        foods = query.all()
        
        logger.info(f"{len(foods)} yiyecek bulundu")
        
        # Sonuçları dönmeden önce kontrol et
        result = []
        for food in foods:
            logger.info(f"Food: {food.fdc_id} - {food.description}")
            # Doğrudan dict olarak dönüştür
            food_dict = {
                "fdc_id": food.fdc_id,
                "description": food.description,
                "data_type": food.data_type,
                "food_category_id": food.food_category_id,
                "publication_date": food.publication_date
            }
            result.append(food_dict)
        
        return result
    except Exception as e:
        logger.error(f"Yiyecek listesi alınırken hata: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Yiyecek listesi alınırken hata: {str(e)}")

# Belirli bir yiyeceği ID'ye göre getir
@router.get("/{fdc_id}")
def get_food(fdc_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.fdc_id == fdc_id).first()
    
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yiyecek ID: {fdc_id} bulunamadı")
    
    # Manuel dönüşüm
    return {
        "fdc_id": food.fdc_id,
        "description": food.description,
        "data_type": food.data_type,
        "food_category_id": food.food_category_id,
        "publication_date": food.publication_date
    }

# Bir yiyeceğin tüm besin değerlerini getir
@router.get("/{fdc_id}/nutrients")
def get_food_nutrients(fdc_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.fdc_id == fdc_id).first()
    
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yiyecek ID: {fdc_id} bulunamadı")
    
    # Yiyeceğin tüm besin değerlerini al
    nutrients_query = db.execute(text("""
        SELECT n.id, n.name, n.unit_name, fn.amount
        FROM food_nutrient fn
        JOIN nutrient n ON fn.nutrient_id = n.id
        WHERE fn.fdc_id = :fdc_id
    """), {"fdc_id": fdc_id})
    
    nutrients = []
    for row in nutrients_query:
        nutrient = {
            "id": row.id,
            "name": row.name,
            "unit_name": row.unit_name,
            "amount": row.amount
        }
        nutrients.append(nutrient)
    
    # Manuel dönüşüm
    food_dict = {
        "fdc_id": food.fdc_id,
        "description": food.description,
        "data_type": food.data_type,
        "food_category_id": food.food_category_id,
        "publication_date": food.publication_date
    }
    
    return {
        "food": food_dict,
        "nutrients": nutrients
    }

# Bir yiyeceğin makro besin değerlerini getir (kalori, protein, yağ, karbonhidrat)
@router.get("/{fdc_id}/macronutrients")
def get_food_macronutrients(fdc_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.fdc_id == fdc_id).first()
    
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yiyecek ID: {fdc_id} bulunamadı")
    
    # Makro besin değerlerini al
    macro_query = db.execute(text("""
        SELECT n.name, fn.amount
        FROM food_nutrient fn
        JOIN nutrient n ON fn.nutrient_id = n.id
        WHERE fn.fdc_id = :fdc_id
        AND n.name IN ('Energy', 'Protein', 'Total lipid (fat)', 'Carbohydrate, by difference')
    """), {"fdc_id": fdc_id})
    
    macros = {
        "calories": 0.0,
        "protein": 0.0,
        "fat": 0.0,
        "carbohydrates": 0.0
    }
    
    for row in macro_query:
        if row.name == 'Energy':
            macros["calories"] = row.amount
        elif row.name == 'Protein':
            macros["protein"] = row.amount
        elif row.name == 'Total lipid (fat)':
            macros["fat"] = row.amount
        elif row.name == 'Carbohydrate, by difference':
            macros["carbohydrates"] = row.amount
    
    return macros

# Bir yiyeceğin mikro besin değerlerini getir (vitaminler ve mineraller)
@router.get("/{fdc_id}/micronutrients")
def get_food_micronutrients(fdc_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.fdc_id == fdc_id).first()
    
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yiyecek ID: {fdc_id} bulunamadı")
    
    # Vitamin ve mineralleri al
    vitamins_query = db.execute(text("""
        SELECT n.id, n.name, n.unit_name, fn.amount
        FROM food_nutrient fn
        JOIN nutrient n ON fn.nutrient_id = n.id
        WHERE fn.fdc_id = :fdc_id
        AND (n.name LIKE '%vitamin%' OR n.name LIKE '%Vitamin%')
    """), {"fdc_id": fdc_id})
    
    minerals_query = db.execute(text("""
        SELECT n.id, n.name, n.unit_name, fn.amount
        FROM food_nutrient fn
        JOIN nutrient n ON fn.nutrient_id = n.id
        WHERE fn.fdc_id = :fdc_id
        AND (
            n.name LIKE '%calcium%' OR n.name LIKE '%iron%' OR n.name LIKE '%magnesium%' OR
            n.name LIKE '%phosphorus%' OR n.name LIKE '%potassium%' OR n.name LIKE '%sodium%' OR
            n.name LIKE '%zinc%' OR n.name LIKE '%copper%' OR n.name LIKE '%manganese%' OR
            n.name LIKE '%selenium%' OR n.name LIKE '%fluoride%' OR n.name LIKE '%iodine%'
        )
    """), {"fdc_id": fdc_id})
    
    vitamins = []
    for row in vitamins_query:
        vitamin = {
            "id": row.id,
            "name": row.name,
            "unit_name": row.unit_name,
            "amount": row.amount
        }
        vitamins.append(vitamin)
    
    minerals = []
    for row in minerals_query:
        mineral = {
            "id": row.id,
            "name": row.name,
            "unit_name": row.unit_name,
            "amount": row.amount
        }
        minerals.append(mineral)
    
    return {
        "vitamins": vitamins,
        "minerals": minerals
    }

# Bir yiyeceğin fitokimyasal bileşenlerini getir
@router.get("/{fdc_id}/phytochemicals")
def get_food_phytochemicals(fdc_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.fdc_id == fdc_id).first()
    
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yiyecek ID: {fdc_id} bulunamadı")
    
    # Fitokimyasal bileşenleri al
    phyto_query = db.execute(text("""
        SELECT n.id, n.name, n.unit_name, fn.amount
        FROM food_nutrient fn
        JOIN nutrient n ON fn.nutrient_id = n.id
        WHERE fn.fdc_id = :fdc_id
        AND (
            n.name LIKE '%phyto%' OR n.name LIKE '%flavo%' OR n.name LIKE '%carot%' OR
            n.name LIKE '%anthocyan%' OR n.name LIKE '%isoflavone%' OR n.name LIKE '%lutein%' OR
            n.name LIKE '%zeaxanthin%' OR n.name LIKE '%lycopene%'
        )
    """), {"fdc_id": fdc_id})
    
    compounds = []
    for row in phyto_query:
        compound = {
            "id": row.id,
            "name": row.name,
            "unit_name": row.unit_name,
            "amount": row.amount
        }
        compounds.append(compound)
    
    return {
        "compounds": compounds
    }

# Bir yiyeceğin tüm besin değerlerinin özeti
@router.get("/{fdc_id}/summary")
def get_food_nutrient_summary(fdc_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.fdc_id == fdc_id).first()
    
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yiyecek ID: {fdc_id} bulunamadı")
    
    # Makro besinleri al
    macros = get_food_macronutrients(fdc_id, db)
    
    # Mikro besinleri al
    micros = get_food_micronutrients(fdc_id, db)
    
    # Fitokimyasalları al
    phytos = get_food_phytochemicals(fdc_id, db)
    
    # Manuel dönüşüm
    food_dict = {
        "fdc_id": food.fdc_id,
        "description": food.description,
        "data_type": food.data_type,
        "food_category_id": food.food_category_id,
        "publication_date": food.publication_date
    }
    
    return {
        "food": food_dict,
        "macronutrients": macros,
        "micronutrients": micros,
        "phytochemicals": phytos
    } 