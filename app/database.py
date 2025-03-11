from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from psycopg2.extras import RealDictCursor
import psycopg2
import time
# from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

# This is a starting settings
# Database ile alakalı işlemleri yapıyoruz.
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:sabir123QW!&@localhost:5432/fastapi'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit= False  ,autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # ***************************************************************************
# '''
# Surekli bir dongu icerisinde kalarak db baglantisinin gerceklesmesini bekler
# Burayı artık kullanmıyoruz.
# '''
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost' , database='fastapi', user='postgres', password='sabir123QW!&', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connectiong to database failed")
#         print("Error:", error)
#         time.sleep(2)
# # ***************************************************************************