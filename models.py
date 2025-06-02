from pydantic import BaseModel
from typing import List, Dict
from uuid import uuid4

class Personaggio(BaseModel):
    id: str = None
    nome: str
    eta: int
    ruolo: str
    lingua: str
    stato: str = "vivo"
    relazioni: Dict[str, Dict[str, int | str]] = {}
    salute: int = 100
    sanita_mentale: int = 100
    inventario: Dict[str, int] = {}
    competenze: List[str] = []
    ultimo_luogo: str = "sconosciuto"

    def set_id(self):
        self.id = str(uuid4())
