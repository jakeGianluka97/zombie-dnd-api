from fastapi import APIRouter
from models import Personaggio
from database.memoria import personaggi, gioco_stato

router = APIRouter()

@router.post("/personaggi/")
def crea_personaggio(p: Personaggio):
    p.set_id()
    personaggi[p.id] = p.dict()
    return {"msg": f"Creato '{p.nome}'", "id": p.id}

@router.get("/personaggi/")
def lista():
    return personaggi

@router.get("/personaggi/{id}")
def get_p(id: str):
    return personaggi.get(id, {"errore": "Non trovato"})

@router.post("/relazione/")
def aggiorna_relazione(id_da: str, id_a: str, tipo: str, fiducia: int = 50):
    if id_da in personaggi and id_a in personaggi:
        personaggi[id_da]["relazioni"][id_a] = {"tipo": tipo, "fiducia": min(max(fiducia, 0), 100)}
        return {"msg": f"Relazione {tipo} (fiducia {fiducia}) tra {id_da} e {id_a}"}
    return {"errore": "ID non validi"}

@router.put("/relazione/fiducia/")
def modifica_fiducia(id_da: str, id_a: str, variazione: int):
    if id_da in personaggi and id_a in personaggi and id_a in personaggi[id_da]["relazioni"]:
        r = personaggi[id_da]["relazioni"][id_a]
        r["fiducia"] = max(0, min(100, r["fiducia"] + variazione))
        return {"msg": f"Fiducia aggiornata: {r['fiducia']}"}
    return {"errore": "Relazione non trovata"}
