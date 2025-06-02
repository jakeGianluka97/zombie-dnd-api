from fastapi import FastAPI
from routes import personaggi, tiri, eventi, mappa

app = FastAPI()
app.include_router(personaggi.router)
app.include_router(tiri.router)
app.include_router(eventi.router)
app.include_router(mappa.router)
