
# Import Python Libraries
import pandas as pd
import conf
import sys

# Read all the data sets necessary for computing the Time Table graph
df = pd.read_csv(conf.EZLINK_TRIP_DATA)
stn = pd.read_csv(conf.STATION_DATA)
bus = pd.read_csv(conf.BUSES)
stop = pd.read_csv(conf.BUS_STOPS)


stop = stop.drop(conf.DROP_FIRST_COLUMN,axis=1)

# Resets the index value numbering for the dataframe
stop = stop.reset_index()
del stop['index']

stn = stn.reset_index()
del stn['index']

df = df.reset_index()
del df['index']

stop.columns = conf.STOP_COLUMNS

df2 = pd.DataFrame()

# Compute the total number rows in the station dataset and bus data set
stop_len = stop.shape[0]
bus_len = bus.shape[0]

# Convert the column into integer data type
stop['Start_Stn'] = stop['Start_Stn'].apply(pd.to_numeric, errors='coerce')
stop['End_Stn'] = stop['End_Stn'].apply(pd.to_numeric, errors='coerce')


for i in range(0,stop_len):

    df1 = df[(df['Start_Stn'] == stop['Start_Stn'][i]) & 
             (df['End_Stn'] == stop['End_Stn'][i]) & 
             (df['Bus_Num'] == stop['Bus'][i]) ]
             
    df1 = df1.drop_duplicates(subset='temporal')
    
    df1['Start_minutes'] = df1['Start_minutes'] - (df1['Start_minutes'] % 5)
    df1['Start_time']    = df1['Start_hours']*3600 + df1['Start_minutes']*60
    df1['Duration']      = df1['Time_Taken'] - (df1['Time_Taken'] %5)
             
    df2 = pd.concat([df2,df1],axis=0)

df2 = df2.drop(conf.COLUMNS,axis=1)   
df2 = df2.drop(conf.DROP_FIRST_COLUMN,axis=1)
df2 = df2.reset_index()
del df2['index']

srt = df2['Start_Stn'].drop_duplicates()
srt = pd.DataFrame(srt)
srt = srt.sort_values(['Start_Stn'],ascending = [True])
srt = srt.reset_index()
del srt['index']

# MAPS THE EXISTING STATION RECORD TO A CONTINUOUS INDEX STARTING FROM 0

srt['Start_Stn_Key'] = srt.index

df2['Station'] = df2['End_Stn']
srt['Station'] = srt['Start_Stn']

df2 = pd.merge(df2,srt,on=['Station'],how='left')
df2 = df2[pd.notnull(df2['Start_Stn_Key'])]
          
df2 = df2.reset_index()
del df2['index']

LENGTH = srt.shape[0]

# TIME TABLE GRAPH FORMATION

orig_stdout = sys.stdout
file = open('singapore.txt', 'w')
sys.stdout = file

for i in range(0,LENGTH):
    LIST = []
    df3 = df2[df2['Start_Stn_x'] == srt['Start_Stn'][i]]

    # SOrts the list based on END STATION NUMBER and DEPARTURE TIME STAMP 
    df3 = df3.sort_values(['End_Stn','Start_time'],ascending = [True,True])
    df3 = df3.reset_index()
    del df3['index']
    
    # FOLLOWING THE EXACT FORMAT oF TTL Graph
    LIST = LIST + [srt['Start_Stn_Key'][i]] + [':']
    st_len = df3.shape[0]
    for j in range(0,st_len):

        SUBLIST = [int(df3['Start_Stn_Key'][j]),df3['Start_time'][j],
                df3['Duration'][j],int(df3['Bus_Num'][j])]
        LIST = LIST + SUBLIST
    LIST = LIST + [-1]
    print(*LIST,sep=' ')
    
sys.stdout = orig_stdout
file.close()    
       



    
    




