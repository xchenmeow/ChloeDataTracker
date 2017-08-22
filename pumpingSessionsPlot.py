import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# sleep
pumpdf = pd.read_csv('pump.csv')
pumpdf = pumpdf.drop(['Note'],1)
pumpdf['Date'], pumpdf['DayTime'] = pumpdf['Time'].str.split(',',1).str

def Date2R(date):
    delta = datetime.datetime.strptime(date, '%m/%d/%y').date() - datetime.date(2017,2,17)
    return delta.days

pumpdf['radius'] = pumpdf['Date'].apply(Date2R)

def time2theta(time):
    delta = datetime.datetime.strptime('2017/01/01 '+time,'%Y/%m/%d %I:%M %p') - datetime.datetime(2017,1,1,0,0,0)
    deltamin = delta.total_seconds() / 60
    theta = (90 - deltamin / 4)
    if theta > 0:
        return theta / 360 * 2*np.pi
    else:
        return (360 + theta) / 360 * 2*np.pi
# print(time2theta('10:30 PM'))
pumpdf['startpoint'] = pumpdf['DayTime'].apply(time2theta)

pumpdf['length'] = pumpdf['Amount'].apply(lambda x: int(x[:-3])*np.pi/3000)

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

for i in range(1,len(pumpdf.index)):
    theta = np.arange(pumpdf.loc[i,'startpoint'],pumpdf.loc[i,'startpoint']-pumpdf.loc[i,'length'],-0.01)
    r = np.repeat(pumpdf.loc[i,'radius'],int(pumpdf.loc[i,'length']/0.01)+1)
    ax.plot(theta, r, linewidth=2, color='magenta', label='pump' if i==1 else '')

plt.legend(bbox_to_anchor=(1.25, 0.3))
plt.title('first six month of my pumping sessions')
plt.show()

