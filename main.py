from fastapi import FastAPI
from routes import personaggi, tiri, eventi, mappa, eventi_sociali, azioni
from database import Base, engine


app = FastAPI()
@app.get("/")
def home():
    return {"msg": "API Zombie D&D attiva"}
    from fastapi.responses import FileResponse

@app.get("/openapi.yaml", include_in_schema=False)
def serve_openapi():
    return FileResponse("openapi.yaml", media_type='application/yaml')

app.include_router(personaggi.router, tags=["personaggi"])
app.include_router(eventi.router, tags=["eventi"])
app.include_router(mappa.router, tags=["mappa"])
app.include_router(azioni.router, tags=["azioni"])
app.include_router(eventi_sociali.router, tags=["eventi-sociali"])
Base.metadata.create_all(bind=engine)
