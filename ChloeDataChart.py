import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# sleep
sleepdf = pd.read_csv('Chloe_sleep_new.csv')
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
# pump
pumpdf = pd.read_csv('pump.csv')
pumpdf = pumpdf.drop(['Note'],1)
pumpdf['Date'], pumpdf['DayTime'] = pumpdf['Time'].str.split(',',1).str

pumpeddf['Amount'] = pumpeddf['Amount'].apply(lambda s: int(s[:-3]))
pumpdf['Amount'] = pumpdf['Amount'].apply(lambda s: int(s[:-3]))
sleepperdaydf = sleepdf.groupby('Date').sum().unstack()
pumpedperdaydf = pumpeddf.groupby('Date').sum().unstack()
diaperperdaydf = diaperdf.groupby('Date').count().unstack()
pumpperdaydf = pumpdf.groupby('Date').sum().unstack()


fig = plt.figure(1)
ax1 = plt.subplot(3,1,1)
# ax1.tight_layout()
plt.plot(sleepperdaydf['Duration(minutes)'])
plt.ylabel('min')
plt.title('sleep per day')
plt.subplot(3,1,2)
ax2 = plt.plot(diaperperdaydf['Status'], color='brown')
# ax2.tight_layout()
plt.title('diaper used per day')
plt.subplot(3,1,3)
ax3 = plt.plot(pumpedperdaydf['Amount'], color='orange', label='consumed')
plt.plot(pumpperdaydf['Amount'], color='magenta', label='produced')
# ax3.tight_layout()
plt.ylabel('ml')
plt.title('pumping & pumped amount per day')
plt.legend(bbox_to_anchor=(0.9, 0.5))
plt.show()