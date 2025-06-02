from fastapi import APIRouter
import random

router = APIRouter()

eventi_possibili = {
    "zombie": [
        "Attacco improvviso durante la notte",
        "Zombie mutato con artigli affilati",
        "Orda avvistata in lontananza",
        "Zombie nascosto tra i rottami",
        "Cadavere si risveglia all'improvviso",
        "Trappola sonora attiva uno sciame",
        "Uno zombie si finge morto",
        "Combattimento in un corridoio stretto",
        "Zombie radioattivo emana calore",
        "Attacco sincronizzato da due lati"
    ],
    "npc": [
        "Richiesta d'aiuto da una madre con un neonato",
        "Gruppo di sopravvissuti ostili intercetta la radio",
        "Vecchio amico del passato appare ferito",
        "Viandante solitario offre cure in cambio di protezione",
        "Ragazzina furba tenta di derubarti",
        "Sopravvissuti armati chiedono armi o scorte",
        "Un traditore tra i tuoi compagni ti minaccia",
        "NPC amichevole ti regala un oggetto raro",
        "Straniero con conoscenze scientifiche offre supporto",
        "Mercante ambulante compare con uno strano carretto"
    ],
    "ambiente": [
        "Frana blocca la via di fuga",
        "Pioggia acida costringe a rifugiarsi",
        "Tempesta di sabbia offusca la visuale",
        "Blackout totale nel rifugio",
        "Esplosione sismica smuove le fondamenta",
        "Sirena automatica attira zombie",
        "Vecchio ponte crolla improvvisamente",
        "Nebbia fitta ostacola ogni movimento",
        "Contaminazione nel fiume vicino",
        "Zona irraggiungibile a causa di incendio chimico"
    ],
    "scorte": [
        "Scoperta una scorta militare nascosta",
        "Cibo contaminato causa febbre alta",
        "Munizioni rare trovate in un cassetto nascosto",
        "Borsa rotta, perdi parte dell’inventario",
        "Scambio di scorte riuscito con un gruppo pacifico",
        "Bottiglia d'acqua radioattiva ingerita per errore",
        "Recuperato kit medico intatto",
        "Bussola danneggiata disorienta il gruppo",
        "Crollo del magazzino distrugge viveri",
        "Zaino misterioso abbandonato sotto un ponte"
    ],
    "psicologico": [
        "Allucinazione: qualcuno del passato ti parla",
        "Attacco d'ansia paralizza le tue azioni",
        "Ricordo traumatico mina la tua concentrazione",
        "Litigio acceso con un compagno di viaggio",
        "Notte insonne ti lascia vulnerabile",
        "Pensiero suicida affiora durante una veglia",
        "Sogno lucido suggerisce una direzione",
        "Voce nella radio parla direttamente a te",
        "Tensione crescente nel gruppo",
        "Silenzio opprimente genera panico improvviso"
    ],
    "clima": [
        "Grandinata improvvisa distrugge parte dell'accampamento",
        "Fulmine colpisce un albero vicino e provoca incendio",
        "Alluvione sommerge l’ingresso del rifugio",
        "Tempesta magnetica interferisce con la bussola",
        "Terremoto fa crollare un piano della struttura",
        "Scioglimento del ghiaccio rivela un cadavere",
        "Bufera costringe a fermarsi per ore",
        "Caldo estremo causa disidratazione veloce",
        "Vento fortissimo spazza via le tende",
        "Neve contaminata copre ogni traccia"
    ],
    "animali": [
        "Branco di cani selvatici circonda il gruppo",
        "Uccello mutato emette suoni disorientanti",
        "Ratto infetto morde un compagno",
        "Lupi in lotta con zombie attirano attenzione",
        "Insetti velenosi invadono l'accampamento",
        "Animale morto si muove ancora",
        "Cinghiale mutato distrugge una barriera",
        "Serpente velenoso trovato nel sacco a pelo",
        "Cavallo fuggito conduce a un rifugio abbandonato",
        "Volpe mutante sembra seguire il gruppo"
    ],
    "rovine": [
        "Muro crollato rivela passaggio segreto",
        "Tomba antica nascosta in un seminterrato",
        "Vecchia scuola con scritte sulle lavagne",
        "Tracce recenti in una casa distrutta",
        "Rifugio nascosto dietro un supermercato",
        "Sotterranei pieni di strani simboli",
        "Ascensore funzionante conduce a un piano sigillato",
        "Biblioteca distrutta contiene ancora libri leggibili",
        "Città sommersa accessibile solo con respiratori",
        "Tempio abbandonato pieno di graffiti criptici"
    ],
    "malattia": [
        "Rash cutaneo si diffonde tra i membri del gruppo",
        "Vomito improvviso dopo aver bevuto acqua",
        "Membro del gruppo inizia a delirare",
        "Ferita apparentemente guarita si infetta",
        "Strani sintomi dopo esposizione al fumo nero",
        "Contagio misterioso mette in quarantena l’intero gruppo",
        "Parassiti intestinali rilevati negli escrementi",
        "Febbre altissima costringe al riposo forzato",
        "Morsicatura non infetta... per ora",
        "Analisi rivelano sostanze chimiche nel sangue"
    ],
    "meccanica": [
        "Veicolo si ferma nel mezzo del nulla",
        "Generatore smette di funzionare durante la notte",
        "Porta blindata si chiude dietro di voi",
        "Un pezzo cruciale dell’attrezzatura si rompe",
        "Scatola nera trovata in un veicolo militare",
        "Forno rudimentale esplode durante la cottura",
        "Motosega si inceppa nel momento critico",
        "Cavo tranciato provoca corto circuito",
        "Attrezzo perso in un tombino",
        "Protesi artigianale cede sotto stress"
    ],
    "morale": [
        "Due membri del gruppo discutono violentemente",
        "Un compagno vuole abbandonare un ferito",
        "Scorta rubata da qualcuno del gruppo",
        "Viene proposta una scelta crudele per la sopravvivenza",
        "Qualcuno minaccia di andarsene se non si cambia direzione",
        "Tradimento: una mappa segreta viene nascosta",
        "Tentativo di omicidio durante la notte",
        "Si scopre una bugia sul passato di un alleato",
        "Discussione sul comando del gruppo",
        "Offerta di scorte in cambio di un compagno"
    ]
}


@router.get("/evento-casuale/")
def evento_casuale():
    tipo = random.choice(list(eventi_possibili.keys()))
    evento = random.choice(eventi_possibili[tipo])
    genera_testo_evento("combattimento", {
    "nome": "sconosciuto",
    "evento": "Attacco improvviso",
    "esito": "sopravvissuto per miracolo"
    })
    if tipo == "morale":
        modifica_coesione_gruppo(personaggio_id, -5, db)

    return {"tipo": tipo, "evento": evento}
