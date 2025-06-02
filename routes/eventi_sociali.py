from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models_sql import PersonaggioDB
from core.tratti import TRATTI
import datetime
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

TRATTI_CONFLITTUALI = [
    ("empatico", "cinico"),
    ("leader", "solitario"),
    ("ottimista", "ansioso"),
    ("altruista", "egoista"),
    ("curioso", "ossessivo")
]

TRATTI_SINERGICI = [
    ("empatico", "altruista"),
    ("diplomatico", "leader"),
    ("curioso", "razionale"),
    ("resiliente", "ottimista"),
    ("compassionevole", "empatico")
]

@router.get("/eventi-sociali/log/")
def leggi_log(limit: int = 20, db: Session = Depends(get_db)):
    eventi = db.query(EventoSocialeDB).order_by(EventoSocialeDB.timestamp.desc()).limit(limit).all()
    return [{"timestamp": e.timestamp, "protagonista": e.protagonista, "bersaglio": e.bersaglio, "tipo": e.tipo, "esito": e.esito} for e in eventi]


@router.post("/eventi/interazione-sociale/")
def interazione_sociale(id: str, gruppo: list[str], db: Session = Depends(get_db)):
    protagonista = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not protagonista:
        return {"errore": "Personaggio non trovato"}

    eventi = []

    for target_id in gruppo:
        if target_id == id:
            continue
        bersaglio = db.query(PersonaggioDB).filter(PersonaggioDB.id == target_id).first()
        if not bersaglio:
            continue

        rel = protagonista.relazioni.get(target_id, {})
        fiducia = rel.get("fiducia", 50)

        conflitto = any((t1 in protagonista.tratti and t2 in bersaglio.tratti) or
                        (t2 in protagonista.tratti and t1 in bersaglio.tratti)
                        for t1, t2 in TRATTI_CONFLITTUALI)

        sinergia = any((t1 in protagonista.tratti and t2 in bersaglio.tratti) or
                       (t2 in protagonista.tratti and t1 in bersaglio.tratti)
                       for t1, t2 in TRATTI_SINERGICI)

        evento_tipo = None
        esito_descrizione = ""

        if fiducia < 40 and (conflitto or random.random() < 0.25):
            protagonista.relazioni[target_id]["fiducia"] = max(0, fiducia - 10)
            evento_tipo = "conflitto"
            esito_descrizione = f"Fiducia -10 tra {protagonista.nome} e {bersaglio.nome}"

        elif fiducia > 70 and (sinergia or random.random() < 0.2):
            protagonista.relazioni[target_id]["fiducia"] = min(100, fiducia + 10)
            evento_tipo = "alleanza"
            esito_descrizione = f"Fiducia +10 tra {protagonista.nome} e {bersaglio.nome}"

        if evento_tipo:
            db.add(EventoSocialeDB(
                protagonista=protagonista.nome,
                bersaglio=bersaglio.nome,
                tipo=evento_tipo,
                esito=esito_descrizione
            ))
            db.commit()
            eventi.append({
                "tipo": evento_tipo,
                "protagonista": protagonista.nome,
                "bersaglio": bersaglio.nome,
                "esito": esito_descrizione
            })

    if not eventi:
        return {"msg": "Nessuna interazione significativa nel gruppo."}
    return {"eventi": eventi}
