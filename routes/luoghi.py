from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models_sql import LuogoDB, CollegamentoDB
import uuid
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LuogoIn(BaseModel):
    nome: str
    descrizione: Optional[str] = None

@router.post("/luoghi/", response_model=dict)
def crea_luogo(luogo_in: LuogoIn, db: Session = Depends(get_db)):
    # 2) Genera un nuovo UUID per il luogo
    new_id = str(uuid.uuid4())

    # 3) Se vuoi impedire la duplicazione basata sullo stesso nome,
    #    controlla prima: (opzionale)
    esistente = db.query(LuogoDB).filter(LuogoDB.nome == luogo_in.nome).first()
    if esistente:
        raise HTTPException(status_code=400, detail="Nome luogo già esistente")

    # 4) Crea l’oggetto ORM valorizzando il nuovo ID e i campi mandatori.
    #    Se nel tuo modello LuogoDB hai colonne JSON o altri campi "non null",
    #    inizializzale qui. Supponiamo che LuogoDB abbia almeno (id, nome, descrizione, collegamenti).
    try:
        nuovo_luogo = LuogoDB(
            id=new_id,
            nome=luogo_in.nome,
            descrizione=luogo_in.descrizione or "",
            # Se hai colonne JSON, ad esempio:
            collegamenti=[]   # lista vuota per i collegamenti iniziali
        )
        db.add(nuovo_luogo)
        db.commit()
        db.refresh(nuovo_luogo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore creazione Luogo: {e}")

    return {
        "id": nuovo_luogo.id,
        "nome": nuovo_luogo.nome,
        "descrizione": nuovo_luogo.descrizione
    }
    
@router.post("/collegamento/")
def crea_collegamento(da_id: str, a_id: str, distanza: float, db: Session = Depends(get_db)):
    if not db.query(LuogoDB).filter(LuogoDB.id == da_id).first() or not db.query(LuogoDB).filter(LuogoDB.id == a_id).first():
        return {"errore": "Uno o entrambi i luoghi non esistono"}
    
    link = CollegamentoDB(
        id=str(uuid.uuid4()),
        da_id=da_id,
        a_id=a_id,
        distanza=distanza
    )
    db.add(link)
    db.commit()
    return {"msg": f"Collegamento creato tra {da_id} e {a_id}"}

@router.get("/luoghi/")
def lista_luoghi(db: Session = Depends(get_db)):
    return db.query(LuogoDB).all()

@router.get("/luoghi/{id}/collegamenti")
def collegamenti(id: str, db: Session = Depends(get_db)):
    conn = db.query(CollegamentoDB).filter(CollegamentoDB.da_id == id).all()
    return [{"a_id": c.a_id, "distanza": c.distanza} for c in conn]
