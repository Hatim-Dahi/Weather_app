import requests
from datetime import datetime
from flask import *  
app = Flask(__name__)  



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/result', methods=['POST', 'GET'])
def result():
    name=request.form.get("cityname")

    weather_url="http://api.openweathermap.org/data/2.5/weather?q={}&APPID=f49a8b48b1b3014bf86ffb8b5d5c742a"
    
    w_response=requests.get(weather_url.format(name))
    w_response_data=w_response.json()
    if w_response_data['cod']!='404':
        try: 
            weather_dic={
        'city': name.capitalize(),
        'temp': (w_response_data['main']['temp']-273),
        'description': w_response_data['weather'][0]['description'].upper(),
        'humidity': w_response_data['main']['humidity'],
        'timezone': w_response_data['timezone'],
        'sunrise': w_response_data['sys']['sunrise'],
        'sunset': w_response_data['sys']['sunset'],
        }
            sunrise=datetime.utcfromtimestamp(weather_dic['sunrise']+weather_dic['timezone'])
            sunrise=sunrise.time()
        
            sunset=datetime.utcfromtimestamp(weather_dic['sunset']+weather_dic['timezone'])
            sunset=sunset.time()

            icon= w_response_data['weather'][0]['icon']
            
        except:
            weather_dic={}
            sunrise=""
            sunset=""
            url=""

        url= "http://openweathermap.org/img/w/{}.png".format(icon)
        return render_template("result.html", Weather=weather_dic, url=url, sunrise=sunrise, sunset=sunset,)  
    msg="Enter correct city name"
    return render_template('index.html', msg=msg)

if __name__ == '__main__':  
   app.run(debug = True)    