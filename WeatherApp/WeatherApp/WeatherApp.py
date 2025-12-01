# -*- coding: utf-8 -*-

import json
import requests
from configparser import ConfigParser
from tkinter import *
from datetime import datetime

# Inits config file
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['slakin']['api']

# API URL
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

# Flags for toggle states
toggleStateWeather = False
toggleStateWind = False
toggleStateTemp = False

# Init API results
APIresults = {}

# Images for weather
weather_images = {
    'Clouds': 'img/cloudy.png',
    'Drizzle': 'img/rainy.png',
    'Clear': 'img/sunny.png',
    'Haze': 'img/haze.png',
    'Tornado': 'img/tornado.png',
    'Fog': 'img/fog.png',
    'Mist': 'img/fog.png',
    'Thunder': 'img/thunder.png',
    'Rain': 'img/heavy_rain.png',
    'Snow': 'img/snowy.png'
}

# Gets the weather from city search
def getWeather(city):
    global APIresults 
    # Gets API request
    APIresults = requests.get(url.format(city, api_key))

    if(APIresults):
        # Sorts API results
        json = APIresults.json()
        city=json['name']
        country=json['sys']
        temp_k = json['main']['temp']
        temp_feels = json['main']['feels_like']
        temp_c = temp_k - 273
        temp_feels = temp_feels - 273
        weather = json['weather'][0]['main']
        wind_speed = json['wind']['speed']
        results = [city, country, temp_c, weather, temp_feels, wind_speed]
        return results 
    else:
        print('No Content of ', city, ' found')

# Converts Unix time
def convertUnixToUTC(time):
    dt = datetime.utcfromtimestamp(time)
    formatted_time = dt.strftime('%H:%M')
    return formatted_time

def search():
    # Calls weather
    city = city_text.get()
    weather = getWeather(city)
    city = weather[0]
    countryInfo = weather[1]
    temp = weather[2]
    condition = weather[3]
    temp_feels_like = weather[4]
    wind_speed = weather[5]

    # If found results
    if(weather):

        # Adds text to app
        location_label['text'] = city + ' Weather:'
        temperature_label['text'] = 'Temperature: ' + str(round(temp))+' °C'
        temperature_feels_label['text'] = 'Feels like: ' + str(round(temp_feels_like))+' °C'
        weather_label['text'] = condition
        sunrise_label['text'] = 'Sunrises at ' + convertUnixToUTC(countryInfo['sunrise'])
        sunset_label['text'] = 'Sunsets at ' +convertUnixToUTC(countryInfo['sunset'])
        wind_speed_label['text'] = 'Wind speed: ' + str(wind_speed) + ' m/s'
        show_more_info_wind['text'] = 'Show More'
        show_more_info_temp['text'] = 'Show More'

        # Sorts through weather images to find correct image
        if condition in weather_images:
            show_more_info_weather['text'] = 'Show More'
            cloudy_img = PhotoImage(file=weather_images[condition])
            image_label.config(image=cloudy_img)
            image_label.image = cloudy_img
       
    else:
        # Shows error in console if not
        print('ERROR')

# Shows more weather if Show More pressed
def showMoreWeather():
    global toggleStateWeather
    
    json = APIresults.json()

    weather = json['weather'][0]['main']
    if not toggleStateWeather:
        more_weather_description_label.pack()
        more_weather_info_label.pack()
        if(weather == 'Clouds'):
            more_weather_info_label['text'] ='Coverage :' + str(json['clouds']['all']) + '%'
            show_more_info_weather['text'] = 'Show Less'
            toggleStateWeather = True
        elif(weather == 'Rain' or weather == 'Snow'):
             more_weather_info_label['text'] = str(json['rain']['1h']) + 'mm/h'
             show_more_info_weather['text'] = 'Show Less'
             toggleStateWeather = True
        else:
            toggleStateWeather = True
        
        more_weather_description_label['text'] = 'Description: ' + json['weather'][0]['description']

    else:
         more_weather_info_label['text'] = ''
         show_more_info_weather['text'] = 'Show More'
         more_weather_description_label['text'] = ''
         toggleStateWeather = False
         more_weather_description_label.pack_forget()
         more_weather_info_label.pack_forget()

def showMoreTemp():
    global toggleStateTemp
    json = APIresults.json()
    pressure = str(json['main']['pressure'])
    humidity = str(json['main']['humidity'])

    if not toggleStateTemp:
        more_temp_info_humidity.pack()
        more_temp_info_pressure.pack()
        more_temp_info_humidity['text'] = 'Humidity: ' + humidity + '%'
        more_temp_info_pressure['text'] = 'Pressure: ' + pressure + ' hPa'
        toggleStateTemp = True 
        show_more_info_temp['text'] = 'Show Less'
    
    else:
        toggleStateTemp = False
        more_temp_info_humidity['text'] = ''
        more_temp_info_pressure['text'] = ''
        show_more_info_temp['text'] = 'Show More'
        more_temp_info_humidity.pack_forget()
        more_temp_info_pressure.pack_forget()

# Calculates compass direction depending on angle
def calc_wind_dir(deg):
    directions = [
        (22.5,  'North'),
        (67.5,  'North East'),
        (112.5, 'East'),
        (157.5, 'South East'),
        (202.5, 'South'),
        (247.5, 'South West'),
        (292.5, 'West'),
        (337.5, 'North West'),
        (360.0, 'North')]

    for limit, name in directions:
        if deg < limit:
            return name


def showMoreWind():
    global toggleStateWind
    json = APIresults.json()
    wind_data = json['wind']

    if not toggleStateWind:
        more_wind_info_direction.pack()
        deg = calc_wind_dir(wind_data['deg'])
        more_wind_info_direction['text'] = 'Wind Direction: ' + deg
        show_more_info_wind['text'] = 'Show Less'

        toggleStateWind = True
    else:
         more_wind_info_direction.pack_forget()
         more_wind_info_direction['text'] = ''
         show_more_info_wind['text'] = 'Show More'

         toggleStateWind = False

# Inits app
app = Tk()

# creates title and size
app.title('Weather App')
app.geometry('400x500')

# City input section
city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

Search_button = Button(app, text='Search', width=12, command=search)
Search_button.pack()

location_label = Label(app, text='', font = 70)
location_label.pack()

image_label = Label(app, image=None)
image_label.pack()


# Weather frame section
weather_frame = Frame(app)
weather_frame.pack(pady=10)

weather_label = Label(weather_frame, text='', font = 35)
weather_label.pack()

show_more_info_weather = Label(weather_frame, text='', fg='blue', cursor='hand2')
show_more_info_weather.pack()
show_more_info_weather.bind('<Button-1>', lambda e: showMoreWeather())

more_weather_description_label = Label(weather_frame, text='')
more_weather_info_label = Label(weather_frame, text='')


#Temp frame section
temp_frame = Frame(app)
temp_frame.pack(pady=10)

temperature_label = Label(temp_frame, text='', font = 30)
temperature_label.pack()

temperature_feels_label = Label(temp_frame, text='', font = 30)
temperature_feels_label.pack()

show_more_info_temp = Label(temp_frame, text='', fg='blue', cursor='hand2')
show_more_info_temp.pack()
show_more_info_temp.bind('<Button-1>', lambda e: showMoreTemp())

more_temp_info_humidity = Label(temp_frame, text='')
more_temp_info_pressure = Label(temp_frame, text='')

# Wind frame section
wind_frame = Frame(app)
wind_frame.pack(pady=5)

wind_speed_label = Label(wind_frame, text='', font = 30)
wind_speed_label.pack()

show_more_info_wind = Label(wind_frame, text='', fg='blue', cursor='hand2')
show_more_info_wind.pack()
show_more_info_wind.bind('<Button-1>', lambda e: showMoreWind())

more_wind_info_direction = Label(wind_frame, text='')

# Sun frame section
sun_frame = Frame(app)
sun_frame.pack(pady=5)

sunrise_label = Label(sun_frame, text='', font = 30)
sunrise_label.pack()

sunset_label = Label(sun_frame, text='', font = 30)
sunset_label.pack()

app.mainloop()
