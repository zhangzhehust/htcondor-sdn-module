#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import csv
from time import mktime
from datetime import datetime
from matplotlib.ticker import MultipleLocator

# list the files need to be read
csv_file_1 = '/Users/zhezhang/Desktop/Current_Work/gridftp_file_transfer_150mbps.csv'
csv_file_2 = '/Users/zhezhang/Desktop/Current_Work/gridftp_file_transfer_100mbps.csv'
csv_file_3 = '/Users/zhezhang/Desktop/Current_Work/gridftp_file_transfer_50mbps.csv'

# first read the csv files
f1 = open(csv_file_1, 'rb')
f2 = open(csv_file_2, 'rb')
f3 = open(csv_file_3, 'rb')

reader1 = csv.reader(f1)
reader2 = csv.reader(f2)
reader3 = csv.reader(f3)

# define two array of data
# x represent time; y represent bandwidth
x1 = []
y1 = []

x2 = []
y2 = []

x3 = []
y3 = []

for row in reader1:
  x = row[0]
  y = row[1]
  if y != 'NaN':
    x1.append(x)
    y1.append(y)
f1.close()

for row in reader2:
  x = row[0]
  y = row[1]
  if y != 'NaN':
    x2.append(x)
    y2.append(y)
f2.close()

for row in reader3:
  x = row[0]
  y = row[1]
  if y != 'NaN':
    x3.append(x)
    y3.append(y)
f3.close()

x1.pop(0)
y1.pop(0)
x2.pop(0)
y2.pop(0)
x3.pop(0)
y3.pop(0)

x1 = x1[80:190]
y1 = y1[80:190]
x2 = x2[80:190]
y2 = y2[80:190]
x3 = x3[80:190]
y3 = y3[80:190]


# pre-process the time data
for i in range(len(x1)):
  lines = x1[i].split('T')
  date = lines[0]
  lines = lines[1].split('-')
  time = lines[0]
  date_time = datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M:%S")
  #unix_time = mktime(date_time.timetuple())
  x1[i] = date_time

# pre-process the time data
for i in range(len(x2)):
  lines = x2[i].split('T')
  date = lines[0]
  lines = lines[1].split('-')
  time = lines[0]
  date_time = datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M:%S")
  #unix_time = mktime(date_time.timetuple())
  x2[i] = date_time
  
# pre-process the time data
for i in range(len(x3)):
  lines = x3[i].split('T')
  date = lines[0]
  lines = lines[1].split('-')
  time = lines[0]
  date_time = datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M:%S")
  #unix_time = mktime(date_time.timetuple())
  x3[i] = date_time

# convert bandwidth Value to Mbps
# (bytes/second * 8 ) / 1000000 (divide by 1M)
for i in range(len(y1)):
  y1[i] = (float(y1[i]))*8/1000000
for i in range(len(y2)):
  y2[i] = (float(y2[i]))*8/1000000
for i in range(len(y3)):
  y3[i] = (float(y3[i]))*8/1000000
  
y4 = []
for i in range(len(y1)):
    y4.append(y1[i]+y2[i]+y3[i])

dates1 = md.date2num(x1)
dates2 = md.date2num(x2)
dates3 = md.date2num(x3)

#ax = plt.gca()
fig, ax = plt.subplots()
xfmt = md.DateFormatter('%H:%M')

byminute = (0,10,20,30,40,50)
majorLocator = md.MinuteLocator(byminute)
minorLocator = md.MinuteLocator(interval=2)

ax.xaxis.set_major_locator(majorLocator)
ax.xaxis.set_major_formatter(xfmt)
#ax.xaxis.set_minor_locator(minorLocator)
#ax.xaxis.grid(True, which='major')
#ax.xaxis.grid(True, which='minor')
ax.yaxis.grid(True)

for tick in ax.xaxis.get_major_ticks(): 
      tick.label.set_fontsize(5)

# set the y ticks range and interval
y_ticks = np.arange(0,1001,50)
ax.set_yticks(y_ticks)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(15)

ax.plot_date(dates1, y1, linewidth = 2, linestyle='-', color='r', 
            marker='', label='Job traffic with 200Mbps')
plt.fill_between(dates1, y1, 0, facecolor='red', alpha=0.2)
plt.plot_date(dates2, y2, linewidth = 2, linestyle='-', color='b', 
            marker='', label='Job traffic with 800Mbps')
plt.fill_between(dates2, y2, 0, facecolor='blue', alpha=0.2)
ax.plot_date(dates3, y3, linewidth = 2, linestyle='-', color='g', 
            marker='', label='Job traffic with 200Mbps')
plt.fill_between(dates3, y3, 0, facecolor='green', alpha=0.2)
#plt.grid(True)
#ax.plot_date(dates1, y4, linewidth = 2, linestyle='--', color='k', 
#            marker='', label='Total traffic rate at Interface')
plt.xlabel('Time (HH:MM)', fontsize=15)
plt.ylabel('GridFTP File Transfer Traffic Rate (Mbps)', fontsize=15)
plt.legend(('150Mbps-Client 1','100Mbps-Client 2','50Mbps-Client 3', 'Total'), loc = 'upper right')
plt.ylim((0,200))
plt.show()
