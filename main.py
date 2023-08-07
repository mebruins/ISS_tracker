import requests
import datetime as dt
import smtplib
import time

my_lat = 37.700741
my_long = -77.844276
my_email = 'mebruins123@gmail.com'
g1_password = 'zazyhaeazowhacrk'

def is_night():
    param = {
        'lat':my_lat,
        'lng':my_long,
        'formatted':0
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=param)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    time_now = dt.datetime.now().hour

    if sunset <= time_now <= sunrise:
        return True


# if iss close to my position AND currently dark THEN send email


def iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()
    iss_long = float(data["iss_position"]['longitude'])
    iss_lat = float(data['iss_position']['latitude'])

    if (my_lat - 5) <= iss_lat <= (my_lat + 5) and (my_long - 5) <= iss_long <= (my_long + 5): 
        return True


while True:
    time.sleep(300)
    if iss_overhead() and is_night():
        connection = smtplib.SMTP('smtp.gmail.com', port=587)
        connection.starttls()
        connection.login(my_email, g1_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs='mebruins12@gmail.com',
            msg='Subject: LOOK UP!!\n\nThe ISS is now above you!'
        )
