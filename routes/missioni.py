from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models_sql import MissioneDB
from core.generatore_missioni import genera_missione_dinamica
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/missioni/genera-dinamica/")
def genera_dinamica(evento: str, personaggio: str = None, luogo: str = None, relazione: str = None, tipo: str = "personale", assegnata_a: list[str] = [], db: Session = Depends(get_db)):
    titolo, descrizione = genera_missione_dinamica(evento, personaggio, luogo, relazione)

    missione = MissioneDB(
        titolo=titolo,
        descrizione=descrizione,
        tipo=tipo,
        creatore=personaggio,
        assegnata_a=assegnata_a,
        completata=False
    )
    db.add(missione)
    db.commit()
    return {"msg": f"Missione dinamica '{titolo}' generata", "id": missione.id, "descrizione": descrizione}
