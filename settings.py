from datetime import datetime
from pathlib import Path

cwd = Path.cwd()

# ITV original data filename (Parameter)
filename_registre_vehicles = '22APR2024_Historic_vehicles_amb_ITVs.xlsx'
path_registre_vehicles = cwd / '_data' / filename_registre_vehicles

# 22APR2024_Historic_vehicles_amb_ITVs
# Years between from which data is keeped
MIN_YEAR = 1990
MAX_DATE = datetime(2024, 1, 1)

MIN_DAYS_BETWEEN_REVISIONS = 150 # UNUSED
MIN_STOCK_FOR_MEAN_ACTIVITY_CALCULATION = 50  # Min numb of vehicles in a given grouping to take the mean activity valid

# To keep current stock but calculate activity before covid date
COVID_MILEAGE_ACTIVE = False
COVID_START_DATE = datetime(2019, 3, 1)

# Output folder for results:
OUTPUT_FOLDER = 'output/'

# Output filename of cleaned and categorized data:
filename_output_categorized_vehicle_data = OUTPUT_FOLDER + f'Registre_vehicles_{datetime.now().date()}.csv'
# Output filename for stock and activity dataframe
filename_output_stock_activity = OUTPUT_FOLDER + f'stock_activity_2024_{datetime.now().date()}.csv'