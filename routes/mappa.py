from fastapi import APIRouter
from database.memoria import personaggi, gioco_stato, luoghi
import random

router = APIRouter()

@router.get("/luoghi/")
def elenco_luoghi():
    return luoghi

@router.get("/luoghi/{nome}")
def vicini(nome: str):
    if nome not in luoghi:
        return {"errore": "Luogo non trovato"}
    return {"vicini": luoghi[nome]}

@router.post("/spostamento/")
def sposta_personaggio(id: str, destinazione: str):
    if id not in personaggi:
        return {"errore": "Personaggio non trovato"}

    attuale = personaggi[id]["ultimo_luogo"]
    if attuale not in luoghi or destinazione not in luoghi.get(attuale, []):
        return {"errore": f"Spostamento non consentito da {attuale} a {destinazione}"}

    rischio = random.randint(1, 20)
    evento = "Viaggio sicuro"
    if rischio <= 5:
        personaggi[id]["salute"] -= 10
        evento = "Agguato! Il personaggio è stato ferito (-10 salute)"

    personaggi[id]["ultimo_luogo"] = destinazione
    gioco_stato["luogo"] = destinazione
    gioco_stato["eventi"].append(f"{personaggi[id]['nome']} si è spostato a {destinazione}. {evento}")

    return {
        "personaggio": personaggi[id]["nome"],
        "da": attuale,
        "a": destinazione,
        "evento": evento,
        "salute_attuale": personaggi[id]["salute"]
    }
