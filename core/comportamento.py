import random

def genera_intenzione(evento: str, fiducia: int, sanita: int):
    if "tradimento" in evento or fiducia < 30:
        return random.choice(["tradire", "abbandonare compagno", "scappare"])
    elif "zombie" in evento:
        return random.choice(["attaccare zombie", "nascondersi", "difendere"])
    elif "ferito" in evento or sanita < 40:
        return random.choice(["proteggere ferito", "guarire un alleato", "scappare"])
    elif "scorte" in evento:
        return "cercare scorte"
    elif sanita > 80 and fiducia > 70:
        return random.choice(["allearsi", "seguire", "prendere il comando"])
    else:
        return random.choice(["negoziare", "spiare il gruppo", "rivelare un segreto"])
