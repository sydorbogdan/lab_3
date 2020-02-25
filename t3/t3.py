from flask import Flask, render_template, url_for, request
import tweepy
import geocoder
import folium
from random import randint


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
post = []


def get_users(nic: str) -> dict:
    '''
    return users data
    '''
    rez = {}
    CONSUMER_KEY = 'IfFqvMUJgQAyBOhYM6YX2cADQ'
    CONSUMER_SECRET = '4p0dVgKMut09t66wRnq7CIORrx4u7mbqlvYHXmpWFyjdT40len'
    ACCESS_TOKEN = '1230447514232463360-kvVlQ0LNP3gHbYkL43t0XgnLZamJMq'
    ACCESS_TOKEN_SECRET = 'gGqGV5LwCCrLmwBxFI9SZ1hiVrCkEAiiHgCvJB3jGLleN'
    auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    users = tweepy.Cursor(api.friends, screen_name=nic).items()
    for user in users:
        if user.location != '':
            rez[user.screen_name] = user.location
    return rez


def get_cord_(dct: dict) -> dict:
    '''
    return cord of users
    '''
    rez = {}
    for i in dct:
        try:
            rez[i] = point = geocoder.osm(dct[i]).osm
        except:
            continue
    return rez


def get_map(dct: dict):
    '''
    create map(HTML file)
    '''
    map_ = folium.Map()
    for mrk in dct:
        try:
            folium.Marker((dct[mrk]['y'] + randint(0,100)*0.0001, dct[mrk]['x'] + randint(0,100)*0.0001),popup='<i>' + str(mrk)+'</i>').add_to(map_)
        except:
            continue
    return map_



@app.route("/")
def home():
    '''
    run app
    '''
    return render_template('home.html', post = post)


@app.route('/', methods=['POST'])
def my_form_post():
    '''
    return html map
    '''
    try:
        text = request.form['text']
        dt = get_cord_(get_users(text))
        mp = get_map(dt)
        return mp._repr_html_()
    except:
        return 'Input error'

if __name__ == '__main__':
    app.run(debug=True)

