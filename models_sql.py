from sqlalchemy import Column, String, Integer, JSON
from database import Base

class PersonaggioDB(Base):
    __tablename__ = "personaggi"
    id = Column(String, primary_key=True, index=True)
    nome = Column(String)
    eta = Column(Integer)
    ruolo = Column(String)
    lingua = Column(String)
    stato = Column(String, default="vivo")
    salute = Column(Integer, default=100)
    sanita_mentale = Column(Integer, default=100)
    inventario = Column(JSON, default={})
    relazioni = Column(JSON, default={})
    competenze = Column(JSON, default=[])
    ultimo_luogo = Column(String, default="sconosciuto")
