from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request as req
import ssl
from googletrans import Translator, constants
import geopy.geocoders
import certifi
import re


app = Flask(__name__)

translator = Translator()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    result = ''
    if request.method == 'POST':
        url = request.form['website_url']
        company_name, mails = get_name_from_url(url)
        if company_name != "Enter Valid Url":
            address = get_address(company_name)
            result = {'company_name':company_name, 'mail':mails, 'address':address}
            return render_template('result.html', result=result)
        else:
            result = {'company_name':"Enter Valid URl", 'mail':' ', 'address':' '}
            return render_template('result.html', result=result)

def get_name_from_url(url):
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        reqt = req(url, headers = {"User-Agent":"Mozilla/5.0"})
        webpage = urlopen(reqt).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        company_name = soup.find_all("title")[0].text
        company_name = translator.translate(company_name).text
        company_name = re.sub(r'[^A-Za-z]+', ' ', company_name)
        mail_list = re.findall('\w+@\w+\.{1}\w+', str(soup.text))
        mail_list
        return company_name, mail_list
    except:
        return "Enter Valid Url", " "

def get_address(company_name):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = geopy.geocoders.Nominatim(user_agent=company_name)
    company_name ="'"+company_name+ "'"
    address = geolocator.geocode(company_name)
    address = translator.translate(address).text
    return address
