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


def Date2R(date):
    delta = datetime.datetime.strptime(date, '%m/%d/%y').date() - datetime.date(2017,2,17)
    return delta.days

sleepdf['radius'] = sleepdf['Date'].apply(Date2R)
formuladf['radius'] = formuladf['Date'].apply(Date2R)
pumpeddf['radius'] = pumpeddf['Date'].apply(Date2R)
diaperdf['radius'] = diaperdf['Date'].apply(Date2R)


def time2theta(time):
    delta = datetime.datetime.strptime('2017/01/01 '+time,'%Y/%m/%d %I:%M %p') - datetime.datetime(2017,1,1,0,0,0)
    deltamin = delta.total_seconds() / 60
    theta = (90 - deltamin / 4)
    if theta > 0:
        return theta / 360 * 2*np.pi
    else:
        return (360 + theta) / 360 * 2*np.pi
# print(time2theta('10:30 PM'))
sleepdf['startpoint'] = sleepdf['DayTime'].apply(time2theta)
formuladf['startpoint'] = formuladf['DayTime'].apply(time2theta)
pumpeddf['startpoint'] = pumpeddf['DayTime'].apply(time2theta)
diaperdf['startpoint'] = diaperdf['DayTime'].apply(time2theta)


sleepdf['length'] = sleepdf['Duration(minutes)'].apply(lambda x: x*np.pi/720)
formuladf['length'] = formuladf['Amount'].apply(lambda x: int(x[:-3])*np.pi/3000)
pumpeddf['length'] = pumpeddf['Amount'].apply(lambda x: int(x[:-3])*np.pi/3000)


# print(sleepdf.head())
# print(formuladf.head())
# print(pumpeddf.head())
# print(diaperdf.head())


# plot
fig = plt.figure(1)
ax = plt.subplot(111, projection='polar')
fig.add_subplot(ax)
ax.set_xlim(-50,200)
ax.set_ylim(-50,200)
ax.set_aspect('equal')
ax.set_rmax(200)
ax.set_xticklabels(['6', '3', '0', '21', '18', '15', '12', '9'])
ax.set_yticklabels(['1.5m','3m','4.5m','6m'])  
ax.set_rlabel_position(135)
for i in range(1,len(sleepdf.index)):
    theta = np.arange(sleepdf.loc[i,'startpoint'],sleepdf.loc[i,'startpoint']-sleepdf.loc[i,'length'],-0.01)
    r = np.repeat(sleepdf.loc[i,'radius'],int(sleepdf.loc[i,'length']/0.01)+1)
    ax.plot(theta, r, linewidth=2, color='blue', label='sleep' if i==1 else '')

for i in range(1,len(formuladf.index)):
    theta = np.arange(formuladf.loc[i,'startpoint'],formuladf.loc[i,'startpoint']-formuladf.loc[i,'length'],-0.01)
    r = np.repeat(formuladf.loc[i,'radius'],int(formuladf.loc[i,'length']/0.01)+1)
    ax.plot(theta, r, linewidth=2, color='green', label='formula' if i==1 else '')

for i in range(1,len(pumpeddf.index)):
    theta = np.arange(pumpeddf.loc[i,'startpoint'],pumpeddf.loc[i,'startpoint']-pumpeddf.loc[i,'length'],-0.01)
    r = np.repeat(pumpeddf.loc[i,'radius'],int(pumpeddf.loc[i,'length']/0.01)+1)
    ax.plot(theta, r, linewidth=2, color='red', label='pumped' if i==1 else '')

flag1 = 0
flag2 = 0
flag3 = 0
for i in range(1,len(diaperdf.index)):
    if diaperdf.loc[i,'Status'] == 'Wet':
        ax.scatter(diaperdf.loc[i,'startpoint'], diaperdf.loc[i,'radius'], s=20, color='orange', \
            label='wet diaper' if flag1==0 else '')
        flag1 = 1
    if diaperdf.loc[i,'Status'] == 'Dirty':
        ax.scatter(diaperdf.loc[i,'startpoint'], diaperdf.loc[i,'radius'], s=20, color='black', \
            label='dirty diaper' if flag2==0 else '')
        flag2 = 1
    if diaperdf.loc[i,'Status'] == 'Mixed':
        ax.scatter(diaperdf.loc[i,'startpoint'], diaperdf.loc[i,'radius'], s=20, color='grey', \
            label='mixed diaper' if flag3==0 else '')
        flag3 = 1
plt.legend(bbox_to_anchor=(1.35, 0.3))
plt.title('first six month of Chloe')
plt.show()


