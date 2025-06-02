from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models_sql import PersonaggioDB
from database import SessionLocal
from utils.luoghi import aggiungi_o_espandi_luogo
from core.tratti import TRATTI
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calcola_modificatore(p, azione: str):
    return sum([TRATTI[t].get("bonus_azioni", {}).get(azione, 0) for t in p.tratti])

def tiro_dado(modificatore: int, difficolta: int):
    tiro = random.randint(1, 20)
    totale = tiro + modificatore
    esito = "successo" if totale >= difficolta else "fallimento"
    critico = "critico positivo" if tiro == 20 else "critico negativo" if tiro == 1 else "normale"
    return tiro, totale, esito, critico

@router.post("/azioni/percezione/")
def percezione(id: str, difficolta: int = 12, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    modificatore = calcola_modificatore(p, "percezione")
    tiro, totale, esito, critico = tiro_dado(modificatore, difficolta)

    return {
        "azione": "percezione",
        "personaggio": p.nome,
        "tiro": tiro,
        "modificatore": modificatore,
        "totale": totale,
        "esito": esito,
        "critico": critico
    }

@router.post("/azioni/diplomazia/")
def diplomazia(id: str, difficolta: int = 12, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    modificatore = calcola_modificatore(p, "diplomazia")
    tiro, totale, esito, critico = tiro_dado(modificatore, difficolta)

    return {
        "azione": "diplomazia",
        "personaggio": p.nome,
        "tiro": tiro,
        "modificatore": modificatore,
        "totale": totale,
        "esito": esito,
        "critico": critico
    }

@router.post("/azioni/esplorazione/")
def esplora(id: str, destinazione: str, difficolta: int = 12, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    bonus = calcola_modificatore(p, "esplorazione")
    chance_bonus = sum([TRATTI[t].get("effetti_passivi", {}).get("chance_scoperta", 1.0) for t in p.tratti])
    tiro, totale, esito, _ = tiro_dado(bonus, int(difficolta * chance_bonus))

    if esito == "successo":
        aggiungi_o_espandi_luogo(destinazione, p.ultimo_luogo, db)
        messaggio = f"Hai scoperto il luogo '{destinazione}'!"
    else:
        messaggio = "Non hai trovato nulla di utile."

    return {
        "azione": "esplorazione",
        "personaggio": p.nome,
        "tiro": tiro,
        "bonus": bonus,
        "totale": totale,
        "esito": messaggio
    }

@router.post("/azioni/intuito/")
def intuito(id: str, difficolta: int = 12, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    modificatore = calcola_modificatore(p, "intuito")
    tiro, totale, esito, critico = tiro_dado(modificatore, difficolta)

    return {
        "azione": "intuito",
        "personaggio": p.nome,
        "tiro": tiro,
        "modificatore": modificatore,
        "totale": totale,
        "esito": esito,
        "critico": critico
    }

@router.post("/azioni/intimidazione/")
def intimidazione(id: str, difficolta: int = 14, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    modificatore = calcola_modificatore(p, "intimidazione")
    tiro, totale, esito, critico = tiro_dado(modificatore, difficolta)

    return {
        "azione": "intimidazione",
        "personaggio": p.nome,
        "tiro": tiro,
        "modificatore": modificatore,
        "totale": totale,
        "esito": esito,
        "critico": critico
    }

@router.post("/azioni/combattimento/")
def combattimento(id: str, difficolta: int = 13, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    modificatore = calcola_modificatore(p, "combattimento")
    tiro, totale, esito, critico = tiro_dado(modificatore, difficolta)

    return {
        "azione": "combattimento",
        "personaggio": p.nome,
        "tiro": tiro,
        "modificatore": modificatore,
        "totale": totale,
        "esito": esito,
        "critico": critico
    }

@router.post("/azioni/sopravvivenza/")
def sopravvivenza(id: str, difficolta: int = 11, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    modificatore = calcola_modificatore(p, "sopravvivenza")
    tiro, totale, esito, critico = tiro_dado(modificatore, difficolta)

    return {
        "azione": "sopravvivenza",
        "personaggio": p.nome,
        "tiro": tiro,
        "modificatore": modificatore,
        "totale": totale,
        "esito": esito,
        "critico": critico
    }

@router.post("/azioni/fuga/")
def fuga(id: str, difficolta: int = 13, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    modificatore = calcola_modificatore(p, "fuga")
    tiro, totale, esito, critico = tiro_dado(modificatore, difficolta)

    return {
        "azione": "fuga",
        "personaggio": p.nome,
        "tiro": tiro,
        "modificatore": modificatore,
        "totale": totale,
        "esito": esito,
        "critico": critico
    }
