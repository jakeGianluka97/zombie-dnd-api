from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models_sql import TraumaMemoriaDB, PersonaggioDB

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/traumi-memorie/")
def lista_traumi(db: Session = Depends(get_db)):
    return db.query(TraumaMemoriaDB).all()

@router.post("/personaggio/aggiungi-trauma/")
def aggiungi_trauma(id: str, codice: str, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    trauma = db.query(TraumaMemoriaDB).filter_by(codice=codice, tipo="trauma").first()
    if not p or not trauma:
        return {"errore": "Personaggio o trauma non trovato"}
    if codice not in p.traumi:
        p.traumi.append(codice)
        db.commit()
    return {"msg": f"{trauma.nome} assegnato a {p.nome}"}

@router.post("/personaggio/aggiungi-memoria/")
def aggiungi_memoria(id: str, codice: str, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    memoria = db.query(TraumaMemoriaDB).filter_by(codice=codice, tipo="memoria").first()
    if not p or not memoria:
        return {"errore": "Personaggio o memoria non trovata"}
    if codice not in p.memorie:
        p.memorie.append(codice)
        db.commit()
    return {"msg": f"{memoria.nome} assegnata a {p.nome}"}
