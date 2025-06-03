from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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

# Intenzioni possibili
INTENZIONI = [
    "allearsi", "tradire", "negoziare", "scappare", "difendere", "rubare", "seguire", "cercare scorte",
    "attaccare zombie", "contattare altri gruppi", "nascondersi", "espandere rifugio",
    "abbandonare compagno", "proteggere ferito", "prendere il comando", "spiare il gruppo",
    "convincere un altro PNG", "uccidere un nemico", "rivelare un segreto", "guarire un alleato"
]

@router.post("/npc/aggiorna-comportamento/")
def aggiorna_comportamento(id: str, db: Session = Depends(get_db)):
    npc = db.query(PersonaggioDB).filter(PersonaggioDB.id == id, PersonaggioDB.ruolo == "npc").first()
    if not npc:
        return {"errore": "NPC non trovato"}

    nuova_intenzione = random.choice(INTENZIONI)
    npc.ultima_intenzione = npc.intenzioni[0] if npc.intenzioni else None
    npc.intenzioni = [nuova_intenzione]
    if not npc.storico_intenzioni:
        npc.storico_intenzioni = []

        npc.storico_intenzioni.append({
            "precedente": npc.intenzioni[0] if npc.intenzioni else None,
            "nuova": nuova_intenzione,
            "evento": evento if "evento" in locals() else "aggiornamento casuale"
        })

    db.commit()

    return {"msg": f"{npc.nome} ora intende: {nuova_intenzione}"}

from core.comportamento_npc import genera_intenzione

@router.post("/npc/reagisci/")
def reagisci(id: str, evento: str, db: Session = Depends(get_db)):
    npc = db.query(PersonaggioDB).filter(PersonaggioDB.id == id, PersonaggioDB.ruolo == "npc").first()
    if not npc:
        return {"errore": "NPC non trovato"}

    fiducia_media = 50
    if npc.relazioni:
        fiducia_media = int(sum([r["fiducia"] for r in npc.relazioni.values()]) / len(npc.relazioni))

    nuova_intenzione = genera_intenzione(evento, fiducia_media, npc.sanita_mentale)
    nnpc.ultima_intenzione = npc.intenzioni[0] if npc.intenzioni else None
    npc.intenzioni = [nuova_intenzione]
    if not npc.storico_intenzioni:
        npc.storico_intenzioni = []

        npc.storico_intenzioni.append({
            "precedente": npc.intenzioni[0] if npc.intenzioni else None,
            "nuova": nuova_intenzione,
            "evento": evento if "evento" in locals() else "aggiornamento casuale"
        })

    genera_testo_evento("relazione", {
    "nome": npc.nome,
    "vittima": target_npc_nome,
    "esito": nuova_intenzione
    })


    db.commit()

    return {"msg": f"{npc.nome} ora intende: {nuova_intenzione}", "trigger": evento}


    @router.get("/npc/storia-intenzioni/{id}")
    def storia_intenzioni(id: str, db: Session = Depends(get_db)):
        npc = db.query(PersonaggioDB).filter(PersonaggioDB.id == id).first()
        if not npc:
            return {"errore": "NPC non trovato"}
        return npc.storico_intenzioni or []


