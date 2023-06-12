# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json
import sys

app = Flask(__name__, static_url_path='', static_folder='static')

states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont', 'Virginia','Washington','West Virginia','Wisconsin','Wyoming']
ids = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "Puerto Rico": "PR"
}

codes=list(ids.values())


@app.route("/")
@app.route('/about')
def about():
    return render_template('about.html', states=states)


@app.route("/macro")
def macro():
    
    f = open("data/data.json", "r")
    data = json.load(f)
    f.close()  

    #data --> state --> years --> year --> state/fed
    #data --> state --> cpi --> index/grocery/housing/util/tarnspo/health/misc
    
    legend=[2*i for i in range(1,10)]
    #colors=[f"hsla(136, 54%, {90-8*i}%, 1)" for i in range(8)]
    colors=[f"hsla(43, 70%, {90-8*i}%, 1)" for i in range(8)]
    #print(colors)

    # print(data)
    colorDict={}
    for fiftyS in data:
        #state min wage in 2022
        temp=ids[fiftyS]
        #print(temp)
        #if fiftyS=="Oregon": print(data[fiftyS]["years"]["2022"][0])
        if float(data[fiftyS]["years"]["2022"][0]) == 0: colorDict[temp]="#787875"
        else:
            for i in range(len(legend)):
                if float(data[fiftyS]["years"]["2022"][0]) < legend[i]: 
                    colorDict[temp]=colors[i-1]
                    #colorset.append(colors[i-1])
                    break
    print(colorDict['CA'])

    return render_template('macro.html', states=states, colors=colors, legend=legend, colorDict=colorDict)

@app.route("/micro/<state>")
def micro(state):

    f = open("data/data.json", "r")
    data = json.load(f)
    f.close()  

    microDataY=data[state]["years"]

    #cprint(microDataY)
    #data --> state --> years --> year --> state/fed
        #microDataY --> year --> state/fed

    ptsState, ptsUS=[], []
    for i in range(1968, 2022):
        #print(microDataY[str(i)][0])
        start= float(microDataY[str(i)][0])
        stop=float(microDataY[str(i+1)][0])
        ptsState.append([start,stop])
    for i in range(1968, 2022):
        start1= float(microDataY[str(i)][1])
        stop1=float(microDataY[str(i+1)][1])
        ptsUS.append([start1,stop1])

    
    bars=[(round(float(data[state]["cpi"][key]),1), key) for key in data[state]["cpi"]]
    #data --> state --> cpi --> index/grocery/housing/util/tarnspo/health/misc
    #microDataB --> index/grocery/housing/util/tarnspo/health/misc --> val  
    print(bars)

    return render_template('micro.html', state=state,states=states, ptsState=ptsState, ptsUS=ptsUS, bars=bars)

app.run(debug=True)
