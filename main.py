# main.py

from fastapi import FastAPI
from fastapi.responses import FileResponse
import yaml

from database import Base, engine

# Import di tutti i router definiti in routes/
from routes import (
    personaggi,
    tiri,
    eventi,
    mappa,
    luoghi,
    azioni,
    eventi_sociali,
    traumi,
    missioni,
    npc,
    narratore,
    gruppi,
)

app = FastAPI(title="API Zombie D&D")

@app.get("/")
def home():
    return {"msg": "API Zombie D&D attiva"}

@app.get("/openapi.yaml", include_in_schema=False)
def serve_openapi():
    # Serve il file YAML generato
    return FileResponse("openapi.yaml", media_type="application/yaml")

# Inclusione di ogni router
app.include_router(personaggi.router,    tags=["personaggi"])
app.include_router(tiri.router,          tags=["tiri"])
app.include_router(eventi.router,        tags=["eventi"])
app.include_router(mappa.router,         tags=["mappa"])
app.include_router(luoghi.router,        tags=["luoghi"])
app.include_router(azioni.router,        tags=["azioni"])
app.include_router(eventi_sociali.router, tags=["eventi-sociali"])
app.include_router(traumi.router,        tags=["traumi"])
app.include_router(missioni.router,      tags=["missioni"])
app.include_router(npc.router,           tags=["npc"])
app.include_router(narratore.router,     tags=["narratore"])
app.include_router(gruppi.router,        tags=["gruppi"])

# Crea le tabelle nel DB (se non esistono già)
Base.metadata.create_all(bind=engine)

# All’avvio, genera il file openapi.yaml aggiornato
@app.on_event("startup")
def scrivi_openapi_yaml():
    schema = app.openapi()
    with open("openapi.yaml", "w", encoding="utf-8") as f:
        # sort_keys=False mantiene l’ordine leggibile
        yaml.dump(schema, f, sort_keys=False, allow_unicode=True)
