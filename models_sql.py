from sqlalchemy import Column, String, Integer, Boolean, JSON, ForeignKey, Float, DateTime
from datetime import datetime
from database import Base

class PersonaggioDB(Base):
    __tablename__ = "personaggi"
    id = Column(String, primary_key=True, index=True)
    nome = Column(String)
    eta = Column(Integer)
    ruolo = Column(String)
    lingua = Column(String)
    stato = Column(String, default="vivo")
    salute = Column(Integer, default=100)
    sanita_mentale = Column(Integer, default=100)
    inventario = Column(JSON, default={})
    relazioni = Column(JSON, default={})
    competenze = Column(JSON, default=[])
    ultimo_luogo = Column(String, default="sconosciuto")
    tratti = Column(JSON, default=[]) 
    traumi = Column(JSON, default=[])
    memorie = Column(JSON, default=[])
    intenzioni = Column(JSON, default=[]) 
    ultima_intenzione = Column(String, default=None)
    storico_intenzioni = Column(JSON, default=[])  # Lista cronologica




class LuogoDB(Base):
    __tablename__ = "luoghi"

    id = Column(String, primary_key=True)  # es. "Napoli/Scampia"
    nome = Column(String, nullable=False)
    descrizione = Column(String)
    tipo = Column(String)
    pericoli = Column(String)
    latitudine = Column(Float)
    longitudine = Column(Float)

class CollegamentoDB(Base):
    __tablename__ = "collegamenti"

    id = Column(String, primary_key=True)
    da_id = Column(String, ForeignKey("luoghi.id"))
    a_id = Column(String, ForeignKey("luoghi.id"))
    distanza = Column(Float)

class EventoSocialeDB(Base):
    __tablename__ = "eventi_sociali"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    protagonista = Column(String)
    bersaglio = Column(String)
    tipo = Column(String)
    esito = Column(String)

class TraumaMemoriaDB(Base):
    __tablename__ = "traumi_memorie"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo = Column(String)  # trauma o memoria
    codice = Column(String, index=True)  # es. "morte_alleato"
    nome = Column(String)
    descrizione = Column(String)
    effetti = Column(JSON)  # es. {"sanita_mentale": -10}

class MissioneDB(Base):
    __tablename__ = "missioni"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    titolo = Column(String)
    descrizione = Column(String)
    tipo = Column(String)  # "gruppo" o "personale"
    creatore = Column(String)  # id personaggio
    assegnata_a = Column(JSON)  # lista di id
    completata = Column(Boolean, default=False)

class EventoNarratoDB(Base):
    __tablename__ = "eventi_narrati"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    personaggio_id = Column(String, nullable=True)
    testo = Column(String)
    categoria = Column(String)  # es. "combattimento", "relazione", "luogo", "psicologia"
    importanza = Column(Integer, default=1)
    timestamp = Column(DateTime, default=datetime.utcnow)

class GruppoDB(Base):
    __tablename__ = "gruppi"
    id = Column(String, primary_key=True)
    nome = Column(String)
    leader_id = Column(String)
    membri = Column(JSON, default=[])  # Lista di ID
    ruoli = Column(JSON, default={})   # Esempio: {"abc123": "medico"}
    coesione = Column(Integer, default=100)



