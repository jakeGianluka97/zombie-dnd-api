from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://zombie_db_ygt2_user:wwlSORNlTIZftgtEGGvbWnIJ4Veyq0rt@dpg-d0uu13adbo4c73bm9qj0-a/zombie_db_ygt2")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
