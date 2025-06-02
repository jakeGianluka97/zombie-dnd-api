from fastapi import APIRouter
import random

router = APIRouter()

eventi_possibili = {
    "zombie": ["Attacco improvviso", "Zombie nascosto", "Inseguimento brutale"],
    "npc": ["Richiesta di aiuto", "NPC armato", "Scambio provviste"],
    "ambiente": ["Frana", "Pioggia intensa", "Blackout"],
    "scorte": ["Cibo trovato", "Munizioni perse", "Acqua contaminata"]
}

@router.get("/evento-casuale/")
def evento():
    tipo = random.choice(list(eventi_possibili))
    descrizione = random.choice(eventi_possibili[tipo])
    gioco_stato["eventi"].append(f"[{tipo.upper()}] {descrizione}")
    return {"tipo": tipo, "evento": descrizione}
