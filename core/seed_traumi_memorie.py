from sqlalchemy.orm import Session
from database import SessionLocal
from models_sql import TraumaMemoriaDB

def seed_traumi_e_memorie():
    traumi = [
        {
            "tipo": "trauma",
            "codice": "morte_alleato",
            "nome": "Perdita traumatica",
            "descrizione": "Hai assistito alla morte di un alleato e non riesci a dimenticarlo.",
            "effetti": {"sanita_mentale": -10}
        },
        {
            "tipo": "trauma",
            "codice": "isolamento_estremo",
            "nome": "Solitudine debilitante",
            "descrizione": "Hai trascorso troppo tempo in isolamento.",
            "effetti": {"diplomazia": -2}
        },
        {
            "tipo": "trauma",
            "codice": "tradimento_subito",
            "nome": "Tradimento indelebile",
            "descrizione": "Qualcuno che stimavi ti ha voltato le spalle.",
            "effetti": {"fiducia": -15}
        }
    ]

    memorie = [
        {
            "tipo": "memoria",
            "codice": "salvato_dal_fuoco",
            "nome": "Coraggio nel fuoco",
            "descrizione": "Un salvataggio miracoloso ti ha ridato speranza.",
            "effetti": {"resistenza_paura": +2}
        },
        {
            "tipo": "memoria",
            "codice": "giuramento_ferreo",
            "nome": "Promessa sacra",
            "descrizione": "Hai giurato di proteggere qualcuno, e quella promessa ti guida.",
            "effetti": {"determinazione": +2}
        },
        {
            "tipo": "memoria",
            "codice": "ricordo_familiare",
            "nome": "Ricordo di famiglia",
            "descrizione": "Un oggetto o pensiero legato alla famiglia ti sostiene nei momenti difficili.",
            "effetti": {"sanita_mentale": +5}
        }
    ]

    db: Session = SessionLocal()
    for entry in traumi + memorie:
        if not db.query(TraumaMemoriaDB).filter_by(codice=entry["codice"]).first():
            db.add(TraumaMemoriaDB(**entry))
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_traumi_e_memorie()
    print("✅ Traumi e memorie inseriti nel database.")
