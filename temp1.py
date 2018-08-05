import pandas as pd
from datetime import datetime
from pandas.tseries.holiday import USFederalHolidayCalendar
import math  
from math import sqrt,radians,sin,cos
import numpy as np

class NYpreprocess:

    
    cal = USFederalHolidayCalendar()
    def cartesian_x(self,lat,lon):
        lat=radians(lat)
        lon=radians(lon)
        R=6371.0
        x = R * cos(lat) * cos(lon)
        return x

    def cartesian_y(self,lat,lon):
        lat=radians(lat)
        lon=radians(lon)
        R=6371.0
        y = R * cos(lat) * sin(lon)
        return y


    def bearing_array(self,lat1, lng1, lat2, lng2):
        AVG_EARTH_RADIUS = 6371  # in km
        lng_delta_rad = np.radians(lng2 - lng1)
        lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
        y = np.sin(lng_delta_rad) * np.cos(lat2)
        x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(lng_delta_rad)
        return np.degrees(np.arctan2(y, x))

    def check_holiday(self,str1):
        holidays = self.cal.holidays(start=str(str1.year)+'-01-01', end=str(str1.year)+'-12-31').to_pydatetime()
        if datetime.strptime(str(str1), '%Y-%m-%d') in holidays:
            return 1
        else:
            return 0
    
    def check_peek(self,temp):
        if((temp>=15 and temp<=19) or temp==8 or temp==9):
               return 1
        return 0

        

    
    
    def start_preprocess(self,data):
        data['datetime']=pd.to_datetime(data['pickup_datetime'])
        #Extracting date from date time
        data["date"]=data['datetime'].dt.date

        data["time"]=data["datetime"].dt.time

        #extracting hour of pickup
        data['hour_pick']=data.datetime.dt.hour

        #extracting day of week, 0-sunday,1-monday.....
        data['day_of_week']=data.datetime.dt.dayofweek

        #Extracting Day of the Month
        data['day_of_month']=data.datetime.dt.month

        #Extracting month number , 1-January 2-February...
        data['month']=data.datetime.dt.month

        #if the time of pickup was night or day
        data['is_night_time']=[1 if (i==0 or i>=19)  else 0 for i in data['datetime'].dt.hour]

        #Extracting Week of the year
        data['week']=data['datetime'].dt.week

        #Extracting minute of pickup
        data['min_of_pick']=data['datetime'].dt.minute
       
        #Extracting weather info in numeric form
        data['weather']=[1 if (i in [1,2,3,4]) else(2 if (i in [5,6,7,8]) else 3) for i in data['month']]

        #Extracting quarter-hour of pickup
        data['quarter']=data.datetime.dt.quarter
        data["peak_hours"]=data["hour_pick"].apply(self.check_peek)
        

        data["isHoliday"]=data["datetime"].dt.date.map(self.check_holiday)

        data.loc[:, 'direction'] = self.bearing_array(float(data['pickup_latitude'].values), 
                                          float(data['pickup_longitude'].values), 
                                          float(data['dropoff_latitude'].values),
                                          float(data['dropoff_longitude'].values))
        data['x1']=[self.cartesian_x(i,j) for i,j in zip(data['pickup_latitude'],data['pickup_longitude'])]
        data['y1']=[self.cartesian_y(i,j) for i,j in zip(data['pickup_latitude'],data['pickup_longitude'])]
        data['x2']=[self.cartesian_x(i,j) for i,j in zip(data['dropoff_latitude'],data['dropoff_longitude'])]
        data['y2']=[self.cartesian_y(i,j) for i,j in zip(data['dropoff_latitude'],data['dropoff_longitude'])]


        #Manhattan Distance
        data['Manhattan_dist'] =(data['x1'] - data['x2']).abs() +(data['y1'] - data['y2']).abs() 
        #Chebyshev Distance
        data['Chebyshev_dist']=[max(abs(i-j),abs(k-l)) for i,j,k,l in zip(data['x1'],
                                                                                   data['y1'],data['x2'],
                                                                                  data['y2'])]
        dict_flag={"Y":1,"N":0}

        data["store_and_fwd_flag"]=data["store_and_fwd_flag"].map(lambda x: dict_flag[x])
        data.drop(["datetime","pickup_datetime","date","time"],axis=1,inplace=True)


        return data







