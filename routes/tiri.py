from sqlalchemy.orm import Session
from fastapi import Depends
from database import SessionLocal
from models_sql import PersonaggioDB
import random


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dado/")
def tira(lati: int = 20, modificatore: int = 0):
    tiro = random.randint(1, lati)
    totale = tiro + modificatore
    critico = "Critico positivo" if tiro == 20 else "Critico negativo" if tiro == 1 else "Normale"
    return {"tiro": tiro, "modificatore": modificatore, "totale": totale, "esito": critico}

@router.get("/duello/")
def duello(mod_utente: int = 0, mod_nemico: int = 0):
    u = random.randint(1, 20) + mod_utente
    n = random.randint(1, 20) + mod_nemico
    vincitore = "utente" if u > n else "nemico" if n > u else "pareggio"
    return {"utente": u, "nemico": n, "esito": vincitore}

@router.post("/azione/")
def azione_narrativa(id: str, tipo: str, abilita: str, difficolta: int = 15, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    bonus = 3 if abilita in (p.competenze or []) else 0
    tiro = random.randint(1, 20)
    totale = tiro + bonus
    esito = "successo" if totale >= difficolta else "fallimento"
    critico = "Critico positivo" if tiro == 20 else "Critico negativo" if tiro == 1 else "Normale"
    effetti = []

    if esito == "successo" and tipo == "attacco":
        effetti.append("Il colpo va a segno")
    elif esito == "fallimento" and tipo == "fuga":
        effetti.append("Il personaggio inciampa")

    return {
        "tiro": tiro,
        "totale": totale,
        "esito": esito,
        "critico": critico,
        "effetti": effetti
    }

