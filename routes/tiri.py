from fastapi import APIRouter
from database.memoria import personaggi, gioco_stato
import random

router = APIRouter()

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
