from models_sql import GruppoDB

def modifica_coesione_gruppo(personaggio_id: str, variazione: int, db):
    gruppi = db.query(GruppoDB).all()
    for gruppo in gruppi:
        if personaggio_id in gruppo.membri:
            gruppo.coesione = max(0, min(100, gruppo.coesione + variazione))
            db.commit()
            return f"Coesione del gruppo '{gruppo.nome}' aggiornata a {gruppo.coesione}"
    return "Nessun gruppo coinvolto"
