import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models_sql import PersonaggioDB, CollegamentoDB, LuogoDB
from core.game_state import game_time
from utils.luoghi import aggiungi_o_espandi_luogo


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/spostamento/")
def sposta_personaggio(id: str, destinazione: str, db: Session = Depends(get_db)):
    p = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
    if not p:
        return {"errore": "Personaggio non trovato"}
    aggiungi_o_espandi_luogo(destinazione, p.ultimo_luogo, db)
    collegamenti = db.query(CollegamentoDB).filter(CollegamentoDB.da_id == p.ultimo_luogo).all()
    destinazioni_valide = [c.a_id for c in collegamenti]

    if destinazione not in destinazioni_valide:
        return {"errore": f"{destinazione} non è raggiungibile da {p.ultimo_luogo}"}

    evento = "Viaggio sicuro"
    if random.randint(1, 20) <= 5:
        p.salute = max(p.salute - 10, 0)
        evento = "Agguato! Il personaggio è stato ferito (-10 salute)"

    p.ultimo_luogo = destinazione
    db.commit()

    return {
        "personaggio": p.nome,
        "da": p.ultimo_luogo,
        "a": destinazione,
        "evento": evento,
        "salute_attuale": p.salute
    }

@router.post("/passa-tempo/")
def passa_tempo(ore: int = 1):
    game_time["ora"] += ore
    while game_time["ora"] >= 24:
        game_time["ora"] -= 24
        game_time["giorno"] += 1
    fase = "notte" if game_time["ora"] < 6 or game_time["ora"] >= 18 else "giorno"
    return {"ora": game_time["ora"], "giorno": game_time["giorno"], "fase": fase}


