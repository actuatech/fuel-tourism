import pandas as pd
from pathlib import Path
from Ingestion import register_ingestor_function

# Define the current working directory
cwd = Path.cwd()

# Registre vehicles data
filename_registre_vehicles = '01FEB2021_Historic_vehicles_amb_ITVs.xlsx'
path_registre_vehicles = cwd / '_data' / filename_registre_vehicles

print('Loading registre de vehicles')
registres = register_ingestor_function(path_registre_vehicles)

print('end')
