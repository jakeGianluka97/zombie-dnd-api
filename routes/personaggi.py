import json
import uuid
import random
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from models_sql import PersonaggioDB
from database import SessionLocal
from core.tratti import TRATTI



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

TRATTI_POSITIVI = [k for k, v in TRATTI.items() if v["categoria"] == "positivo"]
TRATTI_NEGATIVI = [k for k, v in TRATTI.items() if v["categoria"] == "negativo"]
TRATTI_NEUTRI   = [k for k, v in TRATTI.items() if v["categoria"] == "neutro"]


def genera_tratti():
    positivi = random.sample(TRATTI_POSITIVI, k=2)
    negativi = random.sample(TRATTI_NEGATIVI, k=1)
    neutri = random.sample(TRATTI_NEUTRI, k=1)
    return positivi + negativi + neutri

@router.post("/personaggi/")
def crea_personaggio(p: dict, db: Session = Depends(get_db)):
    p["id"] = str(uuid.uuid4())
    personaggio = PersonaggioDB(**p)
    db.add(personaggio)
    db.commit()
    p["tratti"] = genera_tratti()
    db.refresh(personaggio)
    return {"msg": f"Creato {personaggio.nome}", "id": personaggio.id}

@router.get("/personaggi/")
def lista_personaggi(db: Session = Depends(get_db)):
    return db.query(PersonaggioDB).all()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/personaggi/{id}")
def get_personaggio(id: str, db: Session = Depends(get_db)):
    personaggio = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if personaggio is None:
        return {"errore": "Personaggio non trovato"}
    return personaggio


@router.put("/relazione/fiducia/")
def modifica_fiducia(id_da: str, id_a: str, variazione: int, bidirezionale: bool = False, db: Session = Depends(get_db)):
    p1 = db.query(PersonaggioDB).filter(PersonaggioDB.id == id_da).first()
    p2 = db.query(PersonaggioDB).filter(PersonaggioDB.id == id_a).first()

    if not p1 or not p1.relazioni or id_a not in p1.relazioni:
        return {"errore": "Relazione non trovata"}

    # Modifica fiducia da p1 a p2
    relazione = p1.relazioni[id_a]
    relazione["fiducia"] = max(0, min(100, relazione["fiducia"] + variazione))
    relazioni_p1 = dict(p1.relazioni)
    relazioni_p1[id_a] = relazione
    p1.relazioni = relazioni_p1

    # Se bidirezionale, aggiorna anche da p2 a p1
    if bidirezionale and p2 and p2.relazioni and id_da in p2.relazioni:
        relazione2 = p2.relazioni[id_da]
        relazione2["fiducia"] = max(0, min(100, relazione2["fiducia"] + variazione))
        relazioni_p2 = dict(p2.relazioni)
        relazioni_p2[id_da] = relazione2
        p2.relazioni = relazioni_p2

    db.commit()
    return {"msg": f"Fiducia aggiornata (±{variazione}){' in entrambi i sensi' if bidirezionale else ''}"}




@router.put("/relazione/fiducia/")
def modifica_fiducia(id_da: str, id_a: str, variazione: int, db: Session = Depends(get_db)):
    p1 = db.query(PersonaggioDB).filter(PersonaggioDB.id == id_da).first()

    if not p1 or not p1.relazioni or id_a not in p1.relazioni:
        return {"errore": "Relazione non trovata"}

    relazione = p1.relazioni[id_a]
    relazione["fiducia"] = max(0, min(100, relazione["fiducia"] + variazione))
    p1.relazioni[id_a] = relazione

    db.commit()
    return {"msg": f"Fiducia aggiornata: {relazione['fiducia']}"}

@router.get("/personaggi/{id}/tratti")
def get_tratti(id: str, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}
    return {"nome": p.nome, "tratti": p.tratti}
