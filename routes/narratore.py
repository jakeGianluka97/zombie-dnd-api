from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models_sql import EventoNarratoDB
from database import SessionLocal
from datetime import datetime
from core.narratore_utils import genera_testo_evento

import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/narratore/logga/")
def logga_evento(testo: str, categoria: str, personaggio_id: str = None, importanza: int = 1, db: Session = Depends(get_db)):
    evento = EventoNarratoDB(
        id=str(uuid.uuid4()),
        personaggio_id=personaggio_id,
        testo=testo,
        categoria=categoria,
        importanza=importanza,
        timestamp=datetime.utcnow()
    )
    db.add(evento)
    db.commit()
    return {"msg": "Evento narrato registrato", "id": evento.id}

@router.get("/narratore/cronologia/")
def cronologia(categoria: str = None, personaggio_id: str = None, limite: int = 20, min_importanza: int = 1, db: Session = Depends(get_db)):
    query = db.query(EventoNarratoDB).filter(EventoNarratoDB.importanza >= min_importanza)
    if categoria:
        query = query.filter(EventoNarratoDB.categoria == categoria)
    if personaggio_id:
        query = query.filter(EventoNarratoDB.personaggio_id == personaggio_id)
    eventi = query.order_by(EventoNarratoDB.timestamp.desc()).limit(limite).all()
    return eventi

@router.post("/narratore/genera-e-logga/")
def genera_e_logga(tipo: str, dati: dict, importanza: int = 1, personaggio_id: str = None, db: Session = Depends(get_db)):
    testo = genera_testo_evento(tipo, dati)
    evento = EventoNarratoDB(
        id=str(uuid.uuid4()),
        personaggio_id=personaggio_id,
        testo=testo,
        categoria=tipo,
        importanza=importanza,
        timestamp=datetime.utcnow()
    )
    db.add(evento)
    db.commit()
    return {"msg": "Evento generato e registrato", "testo": testo, "id": evento.id}

