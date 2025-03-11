# Buraya tüm modellerimizi koyacağız.
# Sql kodlarını yazmıyoruz.
# Python kodları yazacağız.
# Bir kere database oluşturursan daha sonradan tablonun özelliklerini değiştirmek zor olacaktır. Tabloyu silip tekrar oluşturduk.
# Bu örnekte  published = Column(Boolean,server_default='TRUE',nullable=False)    bunu değiştirdik.


from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)   
    published = Column(Boolean,server_default='TRUE',nullable=False)   
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)

    owner = relationship("User")
    # buradaki User class User daki User
    #schemasdada update edilmesi gereken şeyler var.


# Kullanıcı girişlerini yapabilmek ve yönetebilmek için bir süreç tanımlayacağız.

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=True)  # Google users may not have a password
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    is_google_user = Column(Boolean, server_default='FALSE', nullable=False)
    phone_number = Column(String, nullable=True)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)

# Food ve Nutrient modelleri
class Food(Base):
    __tablename__ = "food"
    fdc_id = Column(Integer, primary_key=True, nullable=False)
    data_type = Column(String, nullable=True)
    description = Column(String, nullable=False)
    food_category_id = Column(Integer, nullable=True)
    publication_date = Column(TIMESTAMP(timezone=True), nullable=True)

class Nutrient(Base):
    __tablename__ = "nutrient"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    unit_name = Column(String, nullable=False)
    nutrient_nbr = Column(String, nullable=True)
    rank = Column(Integer, nullable=True)

class FoodNutrient(Base):
    __tablename__ = "food_nutrient"
    id = Column(Integer, primary_key=True, nullable=False)
    fdc_id = Column(Integer, ForeignKey("food.fdc_id", ondelete="CASCADE"), nullable=False)
    nutrient_id = Column(Integer, ForeignKey("nutrient.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=True)
    data_points = Column(Integer, nullable=True)
    derivation_id = Column(Integer, nullable=True)
    min = Column(Float, nullable=True)
    max = Column(Float, nullable=True)
    median = Column(Float, nullable=True)
    footnote = Column(String, nullable=True)
    min_year_acquired = Column(Integer, nullable=True)
