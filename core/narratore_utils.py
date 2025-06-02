import random

def genera_testo_evento(tipo: str, dati: dict) -> str:
    nome = dati.get("nome", "Qualcuno")
    luogo = dati.get("luogo", "un luogo non precisato")
    obiettivo = dati.get("obiettivo", "")
    vittima = dati.get("vittima", "")
    esito = dati.get("esito", "")
    evento = dati.get("evento", "")

    frasi = {
        "esplorazione": [
            f"{nome} si è avventurato verso {luogo}, alla ricerca di nuove risorse.",
            f"Un passo incerto ha portato {nome} a scoprire qualcosa di interessante vicino a {luogo}.",
            f"{nome} ha esplorato i confini di {luogo}, mettendo a rischio la propria sicurezza."
        ],
        "relazione": [
            f"{nome} ha avuto un confronto con {vittima}. Il legame sembra {esito}.",
            f"Un momento di tensione tra {nome} e {vittima} ha cambiato gli equilibri del gruppo.",
            f"{nome} ha fatto un passo verso la riconciliazione con {vittima}."
        ],
        "combattimento": [
            f"{nome} ha affrontato una minaccia improvvisa: {evento}. L'esito è stato {esito}.",
            f"Nel caos, {nome} si è lanciato contro un pericolo: {evento}.",
            f"{nome} ha combattuto duramente e ora porta le cicatrici di {evento}."
        ],
        "morale": [
            f"{nome} si è isolato dopo un momento difficile.",
            f"La decisione presa a {luogo} ha avuto forti ripercussioni emotive su {nome}.",
            f"{nome} ha trovato forza interiore nonostante le avversità recenti."
        ]
    }

    return random.choice(frasi.get(tipo, [f"{nome} ha vissuto un evento significativo."]))
