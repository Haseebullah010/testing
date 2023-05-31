import gather_keys_oauth2 as Oauth2
import fitbit
import pandas as pd 
import datetime
# You will need to put in your own CLIENT_ID and CLIENT_SECRET as the ones below are fake
CLIENT_ID='23QSXB'
CLIENT_SECRET='bc227371ce1cbcf52797df1b34ad1a0a'

server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
auth2_client=fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)
oneDate = pd.datetime(year = 2019, month = 10, day = 21)
oneDayData = auth2_client.intraday_time_series('activities/heart', oneDate, detail_level='1sec')