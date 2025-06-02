import uuid
from models_sql import LuogoDB, CollegamentoDB
from sqlalchemy.orm import Session

def aggiungi_o_espandi_luogo(nome: str, provenienza: str, db: Session):
    if not db.query(LuogoDB).filter(LuogoDB.id == nome).first():
        nuovo = LuogoDB(
            id=nome,
            nome=nome.split("/")[-1],
            descrizione="Luogo inesplorato",
            tipo="sconosciuto",
            pericoli="variabili",
            latitudine=0.0,
            longitudine=0.0
        )
        db.add(nuovo)
    
    collegamento_esiste = db.query(CollegamentoDB).filter_by(da_id=provenienza, a_id=nome).first()
    if not collegamento_esiste:
        link = CollegamentoDB(
            id=str(uuid.uuid4()),
            da_id=provenienza,
            a_id=nome,
            distanza=1.0
        )
        db.add(link)

    db.commit()
