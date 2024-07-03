CATEGORY_MAPPING_DICT = {
    'TURISME': 'Passenger Cars',
    'FURGONETES': 'Light Commercial Vehicles',
    'CAMIONETES': 'Light Commercial Vehicles',
    'CAMIONS': 'Heavy Duty Trucks',
    'TRANSPORTS PASSATGER': 'Buses',
    'CICLOMOTORS': 'L-Category',
    'MOTOS': 'L-Category',
    'VEHICLES ESPECIALS': 'Off Road',  # Quads
    'VEHICLES AGRICOLS': 'Off Road'
}

FUEL_MAPPING_DICT = {       # De moment no hi han vehicles amb Gas Natural, si al futur hi ha, s'ha d'afegir
    'GASOLINA': 'Petrol',
    'GAS-OIL': 'Diesel',
    'SENSE CARBURANT': None,  # Només Hi han 4 a a partir del 1990, 2 d'ells no tenen km ITV
    'HIBRID GASOLINA NO ENDOLLABLE': 'Petrol Hybrid',
    'HIB.GASOLINA NO ENDOLLABLE': 'Petrol Hybrid',
    'ELECTRIC 100%': 'Battery Electric',
    'HIBRID GASOIL NO ENDOLLABLE': 'Diesel Hybrid',
    'HIB.GASOIL NO ENDOLLABLE': 'Diesel Hybrid',
    'HIBRID GASOIL ENDOLLABLE': 'Diesel PHEV',
    'HIB.GASOIL ENDOLLABLE': 'Diesel PHEV',
    'HIBRID GASOLINA ENDOLLABLE': 'Petrol PHEV',
    'HIB.GASOLINA ENDOLLABLE': 'Petrol PHEV',
    'ELEC. AUTO. ESTESA': 'Battery Electric',  # Només hi ha el BMW I3 amb aquest carburant (elec)
    'GASOLINA-GPL': 'GPL'
}

MAPPING_CATEGORY_LAST_EURO_STANDARD = {
    'Passenger Cars': {
        'last_euro': 'Euro 6 d-temp',
        'second_last_euro': 'Euro 6 a/b/c',
        'third_last_euro': 'Euro 5'
                       },
    'Light Commercial Vehicles': {
            'last_euro': 'Euro 6 d-temp',
            'second_last_euro': 'Euro 6 a/b/c',
            'third_last_euro': 'Euro 5'
                           },
    'L-Category': {
        'last_euro': 'Euro 5',
        'second_last_euro': 'Euro 4',
        'third_last_euro': 'Euro 3'
    },
    'Heavy Duty Trucks': {
        'last_euro': 'Euro VI D/E',
        'second_last_euro': 'Euro VI A/B/C',
        'third_last_euro': 'Euro V'
    },
    'Buses': {
        'last_euro': 'Euro VI D/E',
        'second_last_euro': 'Euro VI A/B/C',
        'third_last_euro': 'Euro V'
        }
}
CATEGORIES = ['Passenger Cars', 'Light Commercial Vehicles', 'Heavy Duty Trucks', 'Buses', 'L-Category', 'Off Road']
HYBRID_PHEV_TYPES = ['Diesel Hybrid', 'Petrol Hybrid', 'Petrol PHEV', 'Diesel PHEV']
NON_ELECTRIC_FUEL_TYPES = ['Petrol', 'Diesel', 'Diesel Hybrid', 'Petrol Hybrid', 'Petrol PHEV', 'Diesel PHEV', 'GPL']
