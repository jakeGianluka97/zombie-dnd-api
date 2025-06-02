from sqlalchemy.orm import Session
from fastapi import Depends
from database import SessionLocal
from models_sql import PersonaggioDB
from fastapi import APIRouter, Depends

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/luoghi/")
def elenco_luoghi():
    return luoghi

@router.get("/luoghi/{nome}")
def vicini(nome: str):
    if nome not in luoghi:
        return {"errore": "Luogo non trovato"}
    return {"vicini": luoghi[nome]}

@router.post("/spostamento/")
def sposta_personaggio(id: str, destinazione: str, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}

    attuale = p.ultimo_luogo
    if attuale not in luoghi or destinazione not in luoghi.get(attuale, []):
        return {"errore": f"Spostamento non consentito da {attuale} a {destinazione}"}

    rischio = random.randint(1, 20)
    evento = "Viaggio sicuro"
    if rischio <= 5:
        p.salute = max(p.salute - 10, 0)
        evento = "Agguato! Il personaggio è stato ferito (-10 salute)"

    p.ultimo_luogo = destinazione
    db.commit()

    return {
        "personaggio": p.nome,
        "da": attuale,
        "a": destinazione,
        "evento": evento,
        "salute_attuale": p.salute
    }
