# -*- coding: utf-8 -*-

import fitbit
import datetime
import pandas as pd
from ast import literal_eval

CLIENT_ID     = "22D57J" # 自分のやつを入れる。
CLIENT_SECRET = "347337575c81c401d78f4fd22af2a104" # 自分のやつを入れる。
TOKEN_FILE    = "token.txt"

tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
access_token = token_dict['access_token']
refresh_token = token_dict['refresh_token']

print access_token
print refresh_token

def updateToken(token):
    f = open(TOKEN_FILE, 'w')
    f.write(str(token))
    f.close()
    return

def pound_to_kg(pound):
    kg = pound * 0.454
    return kg

client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET,
    access_token = access_token, refresh_token = refresh_token, refresh_cb = updateToken)

print client

TODAY = datetime.date.today()
TODAY = "2018-11-21"
#bodyweight = client.get_bodyweight(base_date=TODAY)
#weight = bodyweight["weight"][0]["weight"]
#print(pound_to_kg(weight), "kg")
#print client.intraday_time_series('activities/steps', base_date="2018-11-02", detail_level='1min', start_time="09:00", end_time="15:00")

data_min = client.intraday_time_series('activities/heart', TODAY, detail_level='1min') #'1sec', '1min', or '15min'
heart_beat = data_min["activities-heart-intraday"]["dataset"]
heart_df = pd.DataFrame.from_dict(heart_beat)
heart_df.index = pd.to_datetime([TODAY + " " + t for t in heart_df.time])
heart_df.drop(["time"], axis=1, inplace=True)

#plot
heart_df.plot(y="value", figsize=(20, 5))

#export csv
heart_df.to_csv("heartbeat.csv")

#print heart_sec[:10]
