
BUS_PATH_1       = "var/One_Way_Bus.csv"
BUS_PATH_2       = "var/Two_Way_Bus.csv"
BUSES            = "var/Buses.csv"
EZLINK_TRIP_DATA = "var/TrainData.csv"
BUS_STOPS        = "var/Stops.csv"
STATION_DATA     = "Lat_Long_Data.csv"

COLUMNS = ['Start_hours','Start_minutes','Start_seconds','temporal','DayOfWeek',
        'Citizen_ecode','Peak','Direction','NumStops','total_dist','Start_Lat',
        'Start_Long','End_Long','End_Lat','Rainfall','Time_Taken']

STOP_COLUMNS = ['Start_Stn','Bus','End_Stn']

DROP_FIRST_COLUMN = ['Unnamed: 0']