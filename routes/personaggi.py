import json
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from models_sql import PersonaggioDB
from database import SessionLocal

router = APIRouter()

@router.post("/personaggi/")
def crea_personaggio(p: dict, db: Session = Depends(get_db)):
    p["id"] = str(uuid.uuid4())
    personaggio = PersonaggioDB(**p)
    db.add(personaggio)
    db.commit()
    db.refresh(personaggio)
    return {"msg": f"Creato {personaggio.nome}", "id": personaggio.id}

@router.get("/personaggi/")
def lista():
    return personaggi

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


@router.post("/relazione/")
def aggiorna_relazione(id_da: str, id_a: str, tipo: str, fiducia: int = 50, db: Session = Depends(get_db)):
    p1 = db.query(PersonaggioDB).filter(PersonaggioDB.id == id_da).first()
    p2 = db.query(PersonaggioDB).filter(PersonaggioDB.id == id_a).first()

    if not p1 or not p2:
        return {"errore": "ID non validi"}

    relazioni = p1.relazioni or {}
    relazioni[id_a] = {"tipo": tipo, "fiducia": min(max(fiducia, 0), 100)}
    p1.relazioni = relazioni

    db.commit()
    return {"msg": f"Relazione {tipo} (fiducia {fiducia}) tra {id_da} e {id_a}"}


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
