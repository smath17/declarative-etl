# This file was generated by PygramETL-DeclarativeSpecification in conformity with a given specification.
# Credit Simon Mathiasen 2023 (AAU)

import psycopg2
import pygrametl
from pygrametl.datasources import SQLSource, CSVSource
from pygrametl.tables import CachedDimension, FactTable

Customer_dimension = CachedDimension(
    name='Customer',
    key='CustomerKEY',
    attributes=['name' 'address'])


Part_dimension = CachedDimension(
    name='Part',
    key='PartKEY',
    attributes=['name' 'manufacturer'])


Date_dimension = CachedDimension(
    name='Date',
    key='DateKEY',
    attributes=['day' 'month' 'year'])


Lineorder_fact_table = FactTable(
    name='Lineorder',
    keyrefs=[Customer, Part, Date],
    measures=['quantity', 'price'])


