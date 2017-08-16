import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# sleep
sleepdf = pd.read_csv('Chloe_sleep.csv')
sleepdf = sleepdf.drop(['Baby','Note'],1)
sleepdf['Date'], sleepdf['DayTime'] = sleepdf['Time'].str.split(',',1).str
# formula
formuladf = pd.read_csv('Chloe_formula.csv')
formuladf = formuladf.drop(['Baby','Note'],1)
formuladf['Date'], formuladf['DayTime'] = formuladf['Time'].str.split(',',1).str
# pumped
pumpeddf = pd.read_csv('Chloe_pumped.csv')
pumpeddf = pumpeddf.drop(['Baby','Note'],1)
pumpeddf['Date'], pumpeddf['DayTime'] = pumpeddf['Time'].str.split(',',1).str
# diaper
diaperdf = pd.read_csv('Chloe_diaper.csv')
diaperdf = diaperdf.drop(['Baby','Note'],1)
diaperdf['Date'], diaperdf['DayTime'] = diaperdf['Time'].str.split(',',1).str

sleepperdaydf = sleepdf.groupby('Day').sum()