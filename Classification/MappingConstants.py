CATEGORY_MAPPING_DICT = {
    'TURISME': 'Passenger Cars',
    'FURGONETES': 'Light Commercial Vehicles',
    'CAMIONETES': 'Light Commercial Vehicles',
    'CAMIONS': 'Heavy Duty Trucks',
    'TRANSPORTS PASSATGER': 'Buses',
    'CICLOMOTORS': 'L-Category',
    'MOTOS': 'L-Category',
    'VEHICLES ESPECIALS': 'L-Category',  # Quads
    'VEHICLES AGRICOLS': None  
}

FUEL_MAPPING_DICT = {       # De moment no hi han vehicles amb Gas Natural, si al futur hi ha, s'ha d'afegir
    'GASOLINA': 'Petrol',
    'GAS-OIL': 'Diesel',
    'SENSE CARBURANT': None,  # Només Hi han 4 a a partir del 1990, 2 d'ells no tenen km ITV
    'HIBRID GASOLINA NO ENDOLLABLE': 'Petrol Hybrid',
    'ELECTRIC 100%': 'Battery electric',
    'HIBRID GASOIL NO ENDOLLABLE': 'Diesel Hybrid',
    'HIBRID GASOIL ENDOLLABLE': 'Diesel PHEV',
    'HIBRID GASOLINA ENDOLLABLE': 'Petrol PHEV',
    'ELEC. AUTO. ESTESA': 'Battery electric'  # Només hi ha el BMW I3 amb aquest carburant (elec)
}

TECHONOLOGY_MAPPING_DICT = {
    ''
}