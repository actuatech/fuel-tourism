# fuel-tourism
Aquest modul permet tractar l’Excel del Registre de vehicles i les seves dades respecte a les revisions ITV per tal de:
* Classificar els vehicles segons la seva categoria, utilitzant les classificacions de COPERT (és el estàndard de la Unió Europea pel càlcul d’emissions dels vehicles).
* Obtenció dels patrons d’activitat (km/any) segons la tipologia de vehicle (permetrà el càlcul del consum dels vehicles amb COPERT)
* Generació de gràfics per l’anàlisi de les dades.
* Generació de fitxer .log amb detalls de les operacions de neteja de dades i càlculs realitzats.

Tots els resultats i gràfics es guardaran automàticament a la carpeta `output`

## Environment
Utilitzar entorn Python amb les dependències segons fitxer ``Pipfile.lock``
Dependencies to read Excel files: ``pip install xlrd`` and ``pip install openpyxl``


## Configuració
Copiar l’Excel del registre de vehicles a la carpeta ``_data`` del repositori.

Canviar els paràmetres al fitxer ``settings.py``:

* MIN_YEAR: Any (integer) o data (datetime.date) de fabricació dels vehicles a partir del qual es tenen en compte pels càlculs. Defecte: *1990*
* MAX_DATE: Any (integer) o data (datetime.date) d’alta dels vehicles fins quan es tenen en compte pels càlculs. *2020*
* MIN_DAYS_BETWEEN_REVISIONS: número de dies (integer) mínims que tenen que passar entre dos revisions consecutives per tenir en compte el quilometratge entre revisions. Defecte: *300 dies*
* MIN_STOCK_FOR_MEAN_ACTIVITY_CALCULATION: mínim estoc (integer) per tipologia de vehicle perquè el càlcul de les estadístiques (mitjana, desviació estàndard es tinguin en compte.  Defecte: *50 vehicles per categoria*
* COVID_MILEAGE_ACTIVE: bool. Posar `True` si es vol calcular l'activitat només per revisions ITV per sota de la data COVID_START_DATE. Del contrari, `False`
* COVID_START_DATE: Data a partir de la qual no es tenen en compte els quilometratges de les revisions ITV Per defecte: *datetime(2019, 3, 1)*
* MAPPING_CATEGORY_LAST_EURO_STANDARD: Diccionari representat les últimes normatives Euro per cada una de les categories.
```
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
```     

***TODO Afegir MAPPING_CATEGORY_LAST_EURO_STANDARD al fitxer configuració***


## Ingesta

El mòdul “ingestion” és l’encarregat de carregar el fitxer Excel.
L’Excel té que tenir com a mínim les següents columnes:

  [‘TIPUS',
   ‘ANY_FABRICACIO',
   'DATA_ALTA',
  'DATA_BAIXA',
   'MARCA',
  'MODEL',
  ‘CARBURANT',
   'CV',
   ‘CC_CM3',
   ‘PES_BUIT',
  'DATA_DARRERA_ITV', 'KM_DARRERA_ITV',
   'DATA_DARRERA_ITV2', 'KM_DARRERA_ITV2',
  'DATA_DARRERA_ITV3',   'KM_DARRERA_ITV3',
  'DATA_DARRERA_ITV4', 'KM_DARRERA_ITV4',                           
  'DATA_DARRERA_ITV5', 'KM_DARRERA_ITV5']

## Neteja de dades

Aquest mòdul és l’encarregat de fer un primer filtre de les dades:
* Elimina vehicles anteriors a l’any MIN_YEAR definit per usuari.
* Eliminar vehicles donats de alta posteriorment a la data MAX_DATE definida per usuari.
* Eliminar vehicles donats de baixa.
* Eliminar vehicles sense dades de carburants associades (només 2 vehicles a data 2021).

## Classificació


El fitxer `ClassificationWrapper.py` encapsula les funcions realitzades per tot el mòdul.

La tipologia de vehicle es defineix a partir de 4 classificacions diferents:
1. **Category**:
	Definit a partir del TIPUS de vehicle es generen les següents categories definides per COPERT:
  CATEGORIES = ['Passenger Cars', 'Light Commercial Vehicles', 'Heavy Duty Trucks', 'Buses', 'L-Category', 'Off  Road’]
  Més detalls a `MappingConstants.py`

2. **Fuel**: En funció del tipus de Carburant. Més detalls a `MappingConstants.py`

3. **Segment**: En funció del pes en buit o de la cilindrada del vehicle es defineixen segments. Cada categoria té els seus segments definits per COPERT. Més detalls a `CopertSegmentIdentification.py`

4. **Euro Standard**: En funció de l’any de fabricació i la categoria del vehicle, es fa la classificació Euro de cada vehicle.
Més detalls a `EuroStandard.py`


**Re-classificació**
Les tipologies FURGONETES CAMIONETES i CAMIONS es solapen en certs casos amb les categories Light Commercial Vehicles (pes inferior a 3500kg) i Heavy Duty Trucks (pes superior o igual a 3500kg). Per tant es fa una verificació que la pre-classificació feta segons TIPUS vehicles correspongui realment a la Categoria establerta segons el pes.

D’altra banda, si a la descripció del model d’una moto apareix la paraula “trial” la categoria del vehicle es reclassificar a off road.

Més detall a `ReClassification.py`

**Redistribució Segment**
Degut a buits en les dades de pes i cilindrada no es possible determinar el segment de certs vehicles. Per poder tenir una classificació complerta, es fa una assignació del segment a vehicles sense aquesta dada segons la freqüència d’aparició del segment en la resta de vehicles (distribució normal)

Més detall a `SegmentRedistribution.py`

## Activitat
Per cada una de tipologia resultant (al voltant de 200) es fa el càlcul de l’activitat mitjana a partir de l’activitat de cada un dels vehicles individuals de la tipologia.

L’activitat del vehicle només es té en compte si és la diferencia entre dos revisions és superior a un mínim de dies (definit per usuari).Algunes diferències entre dates de ITV és només d'algun dies (en cas de ITV no passada). En aquests casos s'agafa la revisió següent.
En els casos en que l’activitat estigui fora de valors (superior a Q3 + 1.5 x IQR) o inferiors a 250km/any, no es tenen en compte pel càlcul de la mitjana i desviació estàndard.

Hi han certes tipologies de vehicles que no compleixen amb l’estoc mínim (definit per usuari).
En aquests casos, es fa una agrupació menys restrictiva per agrupar més vehicles fins a l’estoc mínim, i assignar llavors la mitjana, el mínim, el màxim i la desviació estàndard de l’agrupació a la tipologia corresponent.

Se segueix el següent ordre de prioritat fins a que s’assoleix l’estoc mínim:

1. Agrupació per Category, Fuel, Segment: No es té en compte Euro Standard, es a dir antiguitat del vehicle.
2. Agrupació per Category, Fuel, Euro Standard: No és té en compte Segment, es a dir tamany del vehicle.
3. Agrupació per  Category, Fuel: Només es té en compte Categoria i tipus de carburant del vehicle
4. Agrupació per Categoria i Segment:
5. Agrupació per Categoria: Només es té en compt categoria vehicles


En els casos de vehicles tipus híbrid (diesel o gasolina), és tenen en compte com si fossin tipus Diesel o Gasolina, mantenint categoria, segment i Euro Standard)

En els casos de vehicles de les dos últimes classificacions Euro, al no haver passat revisions ITV, no es tenen dades de quilometratge. En aquests casos s’assigna la mitjana de la mateix tipologia però de la classificació Euro anterior o anteriors que tinguin ja suficients vehicles amb revisions fetes. Per aquest punt és important actualitzar el diccionari que relaciona cada categoria amb la seva última classificació Euro al fitxer de configuració.

## Gràfics
Es generen els següents gràfics:
* Gràfic circular de l’estoc de vehicles en funció de la categoria
* Gràfics de barres de l’estoc de vehicles per any de fabricació i tipologia
* Gràfics circulars de l’estoc de vehicles per cada categoria segons la seva classificació Euro
* Gràfic de barres horitzontal de l’activitat mitjana en km/any per cada una de les tipologies de l’estoc de vehicles

També hi ha una funció auxiliar, histograma per anàlisis de dades que no s’utilitza en el programa.
