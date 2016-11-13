import os
from flask import Flask, render_template, request, url_for
from flask_cors import CORS, cross_origin
import json
import numpy as np
from urllib2 import Request, urlopen, URLError
from watson_developer_cloud import PersonalityInsightsV2

app = Flask(__name__)
CORS(app, resources = r'/*')
personality_insights = PersonalityInsightsV2(
    username='deb6b9e4-0853-4b73-aa17-71efddce9ab9',
    password='NM461uOwgTb8')

def destination(source, priors, dest_list, artistic):
    data = np.full((10,5),0.0)
    city_list = {}
    cities = []
    fin1 = open('dataset.txt','r')
    i=0
    for line in fin1:
        cols = line.split()
        city_list[i]=str(cols[0])
        cities.append(cols[0])
        j=1
        for k in range(5):
            data[i][k]=cols[j]
            j+=1
        i=i+1    
    data_user = np.full((5,1),0.0) 
    data_user[2]=priors[0]
    data_user[3]=priors[1]
    data_user[4]=priors[2]
    data_user[0]=artistic
    data_user[1]=1-artistic
    output=np.dot(data,data_user)
    city_prob = {}
    j = 0
    for i in city_list:
        city_prob[city_list[i]] = output[j]
        j = j + 1
    return city_prob,cities

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/response/', methods=['POST'])
def response():
    source = request.form['source']
    dep = request.form['departure']
    dur = request.form['duration']
    budget = request.form['budget']
    #travel = request.form['travel']
    req = Request('http://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin=' + source.upper() + '&departure_date=' + dep + '&duration=' + dur + '&max_price=' + budget + '&apikey=WOKmAmcIRrfN2G2ESJVgD1gzBG32ne8D')
    #print req
    #twit_req = Request("""https://e4e1fbbc-ff89-4f95-bd8f-27ce32389eb2:4O7bSNSVXE@cdeservice.mybluemix.net:443/api/v1/tracks
    #   HTTP/1.1 Content-Type: application/json{
    #      "endDate": "2015-10-03T10:23:00Z",
    #        "name": "My First Rule Track",
    #        "type": "Rule",
    #        "rules": [
    #            {"value": "Canada"},
    #            {"value": "sport hockey"}
    #        ]
    #}""")

    response = urlopen(req)
    result = response.read()
    parsed = json.loads(result)

    with open('personality.txt') as personality_text:
        profile = json.dumps(personality_insights.profile(text=personality_text.read()), indent=2)

    dest_list = []
    for flight in parsed["results"]:
        dest_list.append(flight["destination"])
    #profile = personality_insights.profile(text=travel)
    art = json.loads(profile)
    a = art["tree"]["children"][0]["children"][0]["children"][0]["children"]
    for i in range(len(a)):
        if a[i]['id'] == 'Artistic interests':
            artistic = a[i]['percentage']
    city_prob,cities = destination(source,[0.5263,0.2105,0.2632],dest_list,artistic)
    m,s = 0,''
    for flight in parsed["results"]:
        if flight["destination"] in cities:
            if city_prob[flight["destination"]] > m:
                m,s = city_prob[flight["destination"]],flight["destination"]
    #twit_res = urlopen(twit_req)
    #result = twit_res.read()
    #twit_parsed = json.loads(twit_res)
    return render_template('response.html', parsed=parsed, city_prob=city_prob, cities=cities, best=s)#, twit_parsed = twit_parsed)

if __name__ == '__main__':
    # Bind to PORT/HOST if defined, otherwise default to 5050/localhost.
    PORT = int(os.getenv('VCAP_APP_PORT', '5050'))
    HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))
    app.run(host=HOST, port=PORT) 