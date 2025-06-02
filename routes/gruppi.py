from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models_sql import GruppoDB, PersonaggioDB, EventoNarratoDB
from core.narratore_utils import genera_testo_evento
from datetime import datetime
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/gruppi/crea/")
def crea_gruppo(nome: str, leader_id: str, db: Session = Depends(get_db)):
    nuovo = GruppoDB(
        id=str(uuid.uuid4()),
        nome=nome,
        leader_id=leader_id,
        membri=[leader_id],
        ruoli={leader_id: "leader"},
        coesione=100
    )
    db.add(nuovo)
    db.commit()
    return {"msg": f"Gruppo '{nome}' creato con leader ID {leader_id}", "id": nuovo.id}

@router.post("/gruppi/aggiungi-membro/")
def aggiungi_membro(gruppo_id: str, personaggio_id: str, ruolo: str = "membro", db: Session = Depends(get_db)):
    gruppo = db.query(GruppoDB).filter(GruppoDB.id == gruppo_id).first()
    if not gruppo:
        return {"errore": "Gruppo non trovato"}

    if personaggio_id not in gruppo.membri:
        gruppo.membri.append(personaggio_id)
        gruppo.ruoli[personaggio_id] = ruolo
        db.commit()

    return {"msg": f"Aggiunto {personaggio_id} al gruppo '{gruppo.nome}' come {ruolo}"}

@router.put("/gruppi/cambia-leader/")
def cambia_leader(gruppo_id: str, nuovo_leader_id: str, db: Session = Depends(get_db)):
    gruppo = db.query(GruppoDB).filter(GruppoDB.id == gruppo_id).first()
    if not gruppo:
        return {"errore": "Gruppo non trovato"}
    if nuovo_leader_id not in gruppo.membri:
        return {"errore": "Il nuovo leader deve far parte del gruppo"}

    gruppo.leader_id = nuovo_leader_id
    gruppo.ruoli[nuovo_leader_id] = "leader"
    db.commit()

    return {"msg": f"{nuovo_leader_id} è ora il nuovo leader di {gruppo.nome}"}

@router.get("/gruppi/stato/")
def stato_gruppo(gruppo_id: str, db: Session = Depends(get_db)):
    gruppo = db.query(GruppoDB).filter(GruppoDB.id == gruppo_id).first()
    if not gruppo:
        return {"errore": "Gruppo non trovato"}
    return {
        "nome": gruppo.nome,
        "leader_id": gruppo.leader_id,
        "membri": gruppo.membri,
        "ruoli": gruppo.ruoli,
        "coesione": gruppo.coesione
    }

@router.post("/gruppi/verifica-coesione/")
def verifica_coesione(gruppo_id: str, db: Session = Depends(get_db)):
    gruppo = db.query(GruppoDB).filter(GruppoDB.id == gruppo_id).first()
    if not gruppo:
        return {"errore": "Gruppo non trovato"}

    crisi = None
    if gruppo.coesione < 40:
        tipo = random.choice(["tradimento", "litigio", "abbandono"])
        membro = random.choice([m for m in gruppo.membri if m != gruppo.leader_id])
        crisi = f"{membro} ha causato una crisi nel gruppo: {tipo}"

        gruppo.coesione -= 10  # peggiora
        if gruppo.coesione <= 20:
            gruppo.membri.remove(membro)
            gruppo.ruoli.pop(membro, None)
            crisi += " — il membro ha lasciato il gruppo."

        db.commit()

    return {
        "coesione": gruppo.coesione,
        "crisi": crisi or "Nessuna crisi attuale"
    }

def modifica_coesione_gruppo(personaggio_id: str, variazione: int, db: Session):
    gruppi = db.query(GruppoDB).all()
    for gruppo in gruppi:
        if personaggio_id in gruppo.membri:
            gruppo.coesione = max(0, min(100, gruppo.coesione + variazione))
            db.commit()
            return f"Coesione del gruppo '{gruppo.nome}' aggiornata a {gruppo.coesione}"
    return "Nessun gruppo coinvolto"

@router.post("/gruppi/genera-crisi/")
def genera_crisi(gruppo_id: str, db: Session = Depends(get_db)):
    gruppo = db.query(GruppoDB).filter(GruppoDB.id == gruppo_id).first()
    if not gruppo:
        return {"errore": "Gruppo non trovato"}
    if not gruppo.membri or len(gruppo.membri) < 2:
        return {"errore": "Gruppo troppo piccolo per avere crisi"}

    vittima = random.choice([m for m in gruppo.membri if m != gruppo.leader_id])
    tipo = random.choice(["tradimento", "conflitto aperto", "minaccia di abbandono"])
    gruppo.coesione = max(0, gruppo.coesione - random.randint(5, 15))
    db.commit()

    testo = genera_testo_evento("relazione", {
        "nome": gruppo.leader_id,
        "vittima": vittima,
        "esito": tipo
    })

    evento = EventoNarratoDB(
        id=str(uuid.uuid4()),
        personaggio_id=vittima,
        testo=testo,
        categoria="relazione",
        importanza=2,
        timestamp=datetime.utcnow()
    )
    db.add(evento)
    db.commit()

    return {
        "msg": "Crisi generata nel gruppo",
        "coesione_attuale": gruppo.coesione,
        "evento": testo
    }
