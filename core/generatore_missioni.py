import random

def genera_missione_dinamica(evento: str, personaggio: str = None, luogo: str = None, relazione: str = None):
    base = []

    if "ferito" in evento or "perdita" in evento:
        base.append(("Vendetta", f"{personaggio} vuole vendicarsi dopo l’evento: {evento}."))

    elif "scoperta" in evento or "radio" in evento or "luogo" in evento:
        base.append(("Esplorazione", f"Esaminare il luogo '{luogo}' dopo l’evento: {evento}."))

    elif "aiuto" in evento or "gruppo" in evento:
        base.append(("Alleanza", f"Tentare di unire le forze con chi è coinvolto in: {evento}."))

    elif "trauma" in evento or "paura" in evento:
        base.append(("Resilienza", f"Affrontare le conseguenze psicologiche dopo: {evento}."))

    else:
        base.append(("Sopravvivenza", f"Reagire al contesto: {evento}."))

    return random.choice(base)
