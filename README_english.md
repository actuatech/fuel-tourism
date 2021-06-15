# fuel-turism
Analisis of ITV data (Excel format) to estimate the vehicle activity per type. Allowing to estimate the fuel consumption

## Dependencies
Dependencies to read Excel files: ``pip install xlrd`` and ``pip install openpyxl``

## Activity
The function ``mean_activity_calculator_by_grouping`` calculates the Mean Activity for the vehicle partition types:
Category, Fuel, Segment and Euro Standard that do not have enough units by itself(minimum number 100 by default), 
by grouping by different partitions until one of them has enough vehicles in the grouping.
The assigment of Mean activity is done following the next order of groupings, and returns the Mean Activity if the minimum COUNT is reach, otherwise returns nan
It takes the following data by order:
- Same Euro Standard
- In case that there are no mileage for the same Euro Standard (new standards), the mean activity of previous 
  Euro Standard for category, segment and Fuel is taken into account
    - Same Segment 