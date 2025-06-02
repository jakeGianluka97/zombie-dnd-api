from fastapi import FastAPI
from routes import personaggi, tiri, eventi, mappa
from database import Base, engine


app = FastAPI()
@app.get("/")
def home():
    return {"msg": "API Zombie D&D attiva"}

app.include_router(personaggi.router)
app.include_router(tiri.router)
app.include_router(eventi.router)
app.include_router(mappa.router)
Base.metadata.create_all(bind=engine)
