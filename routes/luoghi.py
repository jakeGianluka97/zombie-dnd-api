from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models_sql import LuogoDB, CollegamentoDB
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/luoghi/")
def crea_luogo(luogo: dict, db: Session = Depends(get_db)):
    if db.query(LuogoDB).filter(LuogoDB.id == luogo["id"]).first():
        return {"errore": "Luogo già esistente"}
    nuovo = LuogoDB(**luogo)
    db.add(nuovo)
    db.commit()
    return {"msg": f"Luogo '{luogo['nome']}' creato con successo"}

@router.post("/collegamento/")
def crea_collegamento(da_id: str, a_id: str, distanza: float, db: Session = Depends(get_db)):
    if not db.query(LuogoDB).filter(LuogoDB.id == da_id).first() or not db.query(LuogoDB).filter(LuogoDB.id == a_id).first():
        return {"errore": "Uno o entrambi i luoghi non esistono"}
    
    link = CollegamentoDB(
        id=str(uuid.uuid4()),
        da_id=da_id,
        a_id=a_id,
        distanza=distanza
    )
    db.add(link)
    db.commit()
    return {"msg": f"Collegamento creato tra {da_id} e {a_id}"}

@router.get("/luoghi/")
def lista_luoghi(db: Session = Depends(get_db)):
    return db.query(LuogoDB).all()

@router.get("/luoghi/{id}/collegamenti")
def collegamenti(id: str, db: Session = Depends(get_db)):
    conn = db.query(CollegamentoDB).filter(CollegamentoDB.da_id == id).all()
    return [{"a_id": c.a_id, "distanza": c.distanza} for c in conn]
