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

    line=round(float(data[state]["cpi"]['Index']),1)
    bars=[(round(float(data[state]["cpi"][key]),1), key) for key in data[state]["cpi"]][1::]
    #data --> state --> cpi --> index/grocery/housing/util/tarnspo/health/misc
    #microDataB --> index/grocery/housing/util/tarnspo/health/misc --> val  
    

    gen=[]
    temp, temp1, avgN=0,0,0
    for i in range(1968,1996): temp+=float(microDataY[str(i)][0])
    for i in range(1996,2023): temp1+=float(microDataY[str(i)][0])

    #from 1968 to 2022, the state's minimum wage has, on average, [0]
    if temp>temp1: gen.append('decreased')
    elif temp<temp1:gen.append('increased')
    else: gen.append('stayed the same')
    #as the federal minimum wage has decreased.
    #0

    avgS=round((temp+temp1)/55,2)
    for i in range(1968,2023): avgN+=float(microDataY[str(i)][1])
    avgN=round(avgN/55,2)

    #the state minimum wage is [1]
    if avgN>avgS: 
        gen.append('less than')
        gen.append("low") #2!!!!
    elif avgN<avgS:
        gen.append('greater than')
        gen.append("high")
    else: 
        gen.append('equal to')
        gen.append("standard (equal to federal rate)")
    
    #the federal minimum wage -- 
    gen.append(avgS)
    gen.append(avgN)
    #$[3]/hour as compared to $[4]/hour
    
    #state has a coli of [5]
    gen.append(line)
    # meaning it is 
    if (100-line)<0: 
        gen.append(f"{round(abs(100-line),1)}% more")
        gen.append("high")
    else: 
        gen.append(f"{round((100-line),1)}% less")
        gen.append("low")
    # [6] expensive to live here than in the average U.S. city. 
    print(gen)

    #The [7] cost of living
    if gen[2] =='equal to' and abs(100-line)<=1: gen.append('does correlate')
    elif gen[7]==gen[2]: gen.append('does correlate')
    else: gen.append('does not correlate')
    # with the [2] minimum wage



    return render_template('micro.html', state=state,states=states, ptsState=ptsState, ptsUS=ptsUS, line=line, bars=bars, gen=gen)

app.run(debug=True)
