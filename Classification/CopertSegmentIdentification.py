import pandas as pd
import logging

from .MappingConstants import NON_ELECTRIC_FUEL_TYPES

info_logger = logging.getLogger('info_logger' + '.CopertSegmentIdentification')


def segment_identification_for_each_category(row: pd.Series) -> str:
    """
    Function that identifies the Segment type of each vehicle given it's Category, Fuel, weight and engine.

    :param row: row of a pd.DataFrame that contains itv register data
    :return: Segment type
    """
    if row['Category'] == 'Off Road':
        return None
    if row['Fuel'] in NON_ELECTRIC_FUEL_TYPES:
        # Segment classification of Passenger Cars Category
        if row['Category'] == 'Passenger Cars':
            if 560 < row['CC_CM3'] < 800:
                # Acording to Copert there is no Petrol PHEV or Diesel Mini, assigned to small
                if row['Fuel'] != 'Petrol':
                    return 'Small'
                return 'Mini'
            if 800 <= row['CC_CM3'] < 1400:
                return 'Small'
            if 1400 <= row['CC_CM3'] <= 2000:
                return 'Medium'
            if 2000 < row['CC_CM3'] <= 8500:
                return 'Large-SUV-Executive'
            else:
                return None

        # Segment classification of Light Commercial Vehicles
        elif row['Category'] == 'Light Commercial Vehicles':
            if 500 < row['PES_BUIT'] <= 1305:
                return 'N1-I'
            elif 1305 < row['PES_BUIT'] <= 1760:
                return 'N1-II'
            elif 1760 < row['PES_BUIT'] <= 3500:
                return 'N1-III'
            else:
                return None

        # Segment classification of Heavy Duty Trucks
        elif row['Category'] == 'Heavy Duty Trucks':   # Articulated trucks cannot be diferenciated with available data
            if 3500 <= row['PES_BUIT'] <= 7500:
                return 'Rigid <=7,5 t'
            elif 7500 < row['PES_BUIT'] < 12000:
                return 'Rigid 7,5 - 12 t'
            elif 12000 <= row['PES_BUIT'] < 14000:
                return 'Rigid 12 - 14 t'
            elif 14000 <= row['PES_BUIT'] < 20000:
                return 'Rigid 14 - 20 t'
            elif 20000 <= row['PES_BUIT'] < 26000:
                return 'Rigid 20 - 26 t'
            elif 26000 <= row['PES_BUIT'] < 28000:
                return 'Rigid 26 - 28 t'
            elif 28000 <= row['PES_BUIT'] <= 32000:
                return 'Rigid 28 - 32 t'
            elif row['PES_BUIT'] > 32000:
                return 'Rigid >32 t '
            else:
                return None

        # Segment classification for Buses
        elif row['Category'] == 'Buses':  # Articulated buses not taken into account, cannot be differenciated with data
            if row['Fuel'] == 'Diesel Hybrid':  # Just one segment for Diesel Hybrid according to Copert
                return 'Urban Buses Diesel Hybrid'
            if 1000 < row['PES_BUIT'] <= 15000:
                return 'Urban Buses Midi <=15 t'
            elif 15000 < row['PES_BUIT'] <= 18000:
                return 'Urban Buses Standard 15 - 18 t'
            elif row['PES_BUIT'] > 18000:
                return 'Urban Buses Articulated >18 t'
            else:
                return None

        # Segment classification for Motorcycles
        elif row['Category'] == 'L-Category':
            if 40 < row['CC_CM3'] <= 50:  # Mopeds & Motorcycles of 2 & 4 strokes cannot be differenciated with available data
                return 'Mopeds 2-stroke <50 cm³'
            elif 50 < row['CC_CM3'] < 250:
                return 'Motorcycles 4-stroke <250 cm³'
            elif 250 <= row['CC_CM3'] <= 750:
                return 'Motorcycles 4-stroke 250 - 750 cm³'
            elif row['CC_CM3'] > 750:
                return 'Motorcycles 4-stroke >750 cm³'

            # Some errors detected that can be solved looking into CV column
            elif (0.4 < row['CV'] <= 0.5) and row['Fuel'] != 'Battery Electric':
                return 'Mopeds 2-stroke <50 cm³'
            elif 0.5 < row['CV'] < 2.5 and row['Fuel'] != 'Battery Electric':
                return 'Motorcycles 4-stroke <250 cm³'
            elif 2.5 < row['CV'] <= 7.5 and row['Fuel'] != 'Battery Electric':
                return 'Motorcycles 4-stroke 250 - 750 cm³'

            else:
                return None
        else:
            info_logger.warning('Vehicle with no Category:')
            info_logger.warning(row)
    else:
        return None
