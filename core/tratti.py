TRATTI = {
    # Positivi
    "empatico": {
        "categoria": "positivo",
        "descrizione": "Capace di comprendere e condividere le emozioni degli altri.",
        "bonus_azioni": {"diplomazia": 2},
        "effetti_passivi": {}
    },
    "altruista": {
        "categoria": "positivo",
        "descrizione": "Disposto a sacrificarsi per gli altri.",
        "bonus_azioni": {},
        "effetti_passivi": {"fiducia_base": 1}
    },
    "ottimista": {
        "categoria": "positivo",
        "descrizione": "Mantiene alto il morale, anche nei momenti più bui.",
        "bonus_azioni": {},
        "effetti_passivi": {"morale_gruppo": 1}
    },
    "risoluto": {
        "categoria": "positivo",
        "descrizione": "Non si arrende facilmente davanti agli ostacoli.",
        "bonus_azioni": {"combattimento": 1},
        "effetti_passivi": {}
    },
    "diplomatico": {
        "categoria": "positivo",
        "descrizione": "Abile a negoziare e mediare i conflitti.",
        "bonus_azioni": {"diplomazia": 1},
        "effetti_passivi": {}
    },
    "leader": {
        "categoria": "positivo",
        "descrizione": "Trascina e ispira gli altri membri del gruppo.",
        "bonus_azioni": {"motivazione": 2},
        "effetti_passivi": {"fiducia_base": 1}
    },
    "razionale": {
        "categoria": "positivo",
        "descrizione": "Pensa con logica anche in situazioni critiche.",
        "bonus_azioni": {"intuito": 1},
        "effetti_passivi": {}
    },
    "resiliente": {
        "categoria": "positivo",
        "descrizione": "Recupera salute e sanità mentale più rapidamente.",
        "bonus_azioni": {},
        "effetti_passivi": {"sanita_bonus": 1}
    },
    "silenzioso": {
        "categoria": "positivo",
        "descrizione": "Muove con discrezione, utile negli spostamenti.",
        "bonus_azioni": {"fuga": 1},
        "effetti_passivi": {}
    },
    "compassionevole": {
        "categoria": "positivo",
        "descrizione": "Si prende cura degli altri, aumentando la coesione.",
        "bonus_azioni": {},
        "effetti_passivi": {"morale_gruppo": 1}
    },

    # Negativi
    "paranoico": {
        "categoria": "negativo",
        "descrizione": "Sempre in allerta, ma difficile da avvicinare.",
        "bonus_azioni": {"percezione": 2},
        "effetti_passivi": {"fiducia_base": -1}
    },
    "impulsivo": {
        "categoria": "negativo",
        "descrizione": "Agisce prima di pensare, rischia spesso.",
        "bonus_azioni": {},
        "effetti_passivi": {"aggro": 1.2}
    },
    "egoista": {
        "categoria": "negativo",
        "descrizione": "Pensa solo a sé stesso.",
        "bonus_azioni": {},
        "effetti_passivi": {"fiducia_base": -2}
    },
    "vendicativo": {
        "categoria": "negativo",
        "descrizione": "Non dimentica i torti subiti.",
        "bonus_azioni": {"combattimento": 1},
        "effetti_passivi": {}
    },
    "cinico": {
        "categoria": "negativo",
        "descrizione": "Freddo e diretto, non mostra empatia.",
        "bonus_azioni": {"intuito": 1, "diplomazia": -1},
        "effetti_passivi": {}
    },
    "egocentrico": {
        "categoria": "negativo",
        "descrizione": "Crede che il mondo ruoti attorno a sé.",
        "bonus_azioni": {},
        "effetti_passivi": {"morale_gruppo": -1}
    },
    "ansioso": {
        "categoria": "negativo",
        "descrizione": "Va facilmente nel panico.",
        "bonus_azioni": {},
        "effetti_passivi": {"morale_gruppo": -1}
    },
    "indeciso": {
        "categoria": "negativo",
        "descrizione": "Ha difficoltà a prendere decisioni.",
        "bonus_azioni": {},
        "effetti_passivi": {}
    },
    "provocatore": {
        "categoria": "negativo",
        "descrizione": "Tende a scatenare litigi e conflitti.",
        "bonus_azioni": {"intimidazione": 1},
        "effetti_passivi": {}
    },
    "solitario": {
        "categoria": "negativo",
        "descrizione": "Sta meglio da solo, fatica nei gruppi.",
        "bonus_azioni": {},
        "effetti_passivi": {"morale_gruppo": -1}
    },

    # Neutri
    "curioso": {
        "categoria": "neutro",
        "descrizione": "Spinto a esplorare, anche a rischio.",
        "bonus_azioni": {"esplorazione": 1},
        "effetti_passivi": {"chance_scoperta": 1.1}
    },
    "diretto": {
        "categoria": "neutro",
        "descrizione": "Dice sempre ciò che pensa, anche a costo di ferire.",
        "bonus_azioni": {"intimidazione": 1},
        "effetti_passivi": {}
    },
    "instabile": {
        "categoria": "neutro",
        "descrizione": "Ha reazioni estreme, critici amplificati.",
        "bonus_azioni": {},
        "effetti_passivi": {"critico_bonus": 1}
    },
    "taciturno": {
        "categoria": "neutro",
        "descrizione": "Parla poco, difficile da comprendere.",
        "bonus_azioni": {},
        "effetti_passivi": {}
    },
    "ossessivo": {
        "categoria": "neutro",
        "descrizione": "Tende a ripetere azioni fino all'ossessione.",
        "bonus_azioni": {"ripetizione": 1},
        "effetti_passivi": {"consumo_oggetti": 1.2}
    }
}