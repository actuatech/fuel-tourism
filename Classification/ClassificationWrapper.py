import pandas as pd
import logging

from .CopertSegmentIdentification import segment_identification_for_each_category
from .EuroStandard import euro_standard_identification_by_year_of_manufacturing
from .ReClassification import (
    reclassification_light_commercial_to_heavy_duty_trucks,
    reclassification_heavy_duty_trucks_to_light_commercial_vehicles,
    reclassification_trial_bikes_to_off_road
                               )
from .MappingFunctions import category_mapper_itv_copert, fuel_mapper_itv_copert
from .SegmentRedistribution import fill_nan_with_frequency
from .MappingConstants import NON_ELECTRIC_FUEL_TYPES, ELECTRIC_TYPES

logger = logging.getLogger('logger' + '.ClassificationWrapper')


def category_fuel_segment_euro_classification_wrapper_function(register_df: pd.DataFrame) -> pd.DataFrame:
    """Return the input itv register df with the columns Category, Fuel, Segment, Euro Standard for each vehicle(row)"""
    logger.info('Starting Vehicle Classification')
    df = category_mapper_itv_copert(register_df)
    df = fuel_mapper_itv_copert(df)
    df = reclassification_light_commercial_to_heavy_duty_trucks(df)
    df = reclassification_heavy_duty_trucks_to_light_commercial_vehicles(df)
    df = reclassification_trial_bikes_to_off_road((df))

    df['Segment'] = df.apply(lambda row: segment_identification_for_each_category(row), axis=1)
    df['Euro Standard'] = df.apply(lambda row: euro_standard_identification_by_year_of_manufacturing(row), axis=1)

    # For non electric vehicles with erroneous weight or CC_M3 data, assigns Segment by normal distribution
    df_only_electric = df[df['Fuel'].isin(ELECTRIC_TYPES)]
    df_without_electric = df[~df['Fuel'].isin(ELECTRIC_TYPES)]
    fill_nan_with_frequency(df_without_electric, 'Segment')
    df = pd.concat([df_only_electric, df_without_electric])
    
    # Assign Segment value of Electrical and Off Road vehicles to None
    df.loc[~df['Fuel'].isin(NON_ELECTRIC_FUEL_TYPES + ELECTRIC_TYPES), 'Segment'] = None
    df.loc[df['Category'] == 'Off Road', 'Segment'] = None

    # Addapt Segment results not present in Copert Stock Configuration
    # There is no Mini segment below Euro 4
    df.loc[(df['Category'] == 'Passenger Cars') &
           (df['Segment'] == 'Mini') &
           ((df['Euro Standard'] == 'Euro 3') | (df['Euro Standard'] == 'Euro 1') |
            (df['Euro Standard'] == 'Conventional') | (df['Euro Standard'] == 'ECE 15/04') |
            (df['Euro Standard'] == 'ECE 15/02') | (df['Euro Standard'] == 'ECE 15/03')), 'Segment'] = 'Small'
    # There is no Small, Medium or small segments in L-Category nor Light Commercial Vehicles
    df.loc[(df['Category'] == 'L-Category') &
           ((df['Segment'] == 'Small') | (df['Segment'] == 'Medium') | (df['Segment'] == 'Large-SUV-Executive')),
           'Segment'] = 'Motorcycles 4-stroke <250 cm³'
    df.loc[(df['Category'] == 'Light Commercial Vehicles') &
           ((df['Segment'] == 'Small') | (df['Segment'] == 'Medium') | (df['Segment'] == 'Large-SUV-Executive')),
           'Segment'] = 'N1-III'
    # There is no mini segment below Euro 4, we assign them to Euro 4
    df.loc[(df['Category'] == 'Passenger Cars') &
           (df['Segment'] == 'Mini') &
           ((df['Euro Standard'] == 'Euro 3') | (df['Euro Standard'] == 'Euro 2') | (df['Euro Standard'] == 'Euro 1')),
           'Euro Standard'] = 'Euro 4'
    # There are no motorcycles other than Petrol
    df.loc[(df['Category'] == 'L-Category') &
           ((df['Fuel'] == 'Diesel') | (df['Fuel'] == 'Diesel Hybrid') | (df['Fuel'] == 'Diesel PHEV') |
            (df['Fuel'] == 'Petrol PHEV') | (df['Fuel'] == 'Petrol Hybrid')),
           'Fuel'] = 'Petrol'
    # There are no hybrid Heavy Duty Trucks, we assigned them a newer Euro Standard
    df.loc[(df['Category'] == 'Heavy Duty Trucks') &
           ((df['Fuel'] == 'Diesel Hybrid') | (df['Fuel'] == 'Diesel PHEV') |
            (df['Fuel'] == 'Petrol PHEV') | (df['Fuel'] == 'Petrol Hybrid')),
           'Fuel'] = 'Diesel'
    rows_to_reassgin = df.index[(df['Category'] == 'Heavy Duty Trucks') &
                                ((df['Fuel'] == 'Diesel Hybrid') | (df['Fuel'] == 'Diesel PHEV') |
                                 (df['Fuel'] == 'Petrol PHEV') | (df['Fuel'] == 'Petrol Hybrid'))]
    df.loc[rows_to_reassgin, 'Euro Standard'] = 'Euro VI D/E'
    # Disel PHEV Passenger Cars can only be Large-SUV-Executive
    df.loc[(df['Category'] == 'Passenger Cars') &
           (df['Fuel'] == 'Diesel PHEV'), 'Segment'] = 'Large-SUV-Executive'

    return df
