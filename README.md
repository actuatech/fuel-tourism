# fuel-turism
Analisis of ITV data (Excel format) to estimate the vehicle activity per type. Allowing to estimate the fuel consumption

## Dependencies
Dependencies to read Excel files: ``pip install xlrd`` and ``pip install openpyxl``




## Taken into account
Algunes diferències entre dates de ITV és només d'algun dies (en cas de ITV no passada).
En aquests casos s'agafa la revisió següent.

El TIPUS de vehicle CAMIONETES inclouen Light Commercial Vehicle i Heavy Duty Trucks, facilment diferenciables pel pes
Light Commercial Vehicles <= 3500kg Només 3 en tot el dataset
