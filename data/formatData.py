import json


f1 = open("expenses1.csv", "r")
lines = f1.readlines()
dictionary ={}

for i in range(0, len(lines)):
    lines[i]=lines[i][0:-2]
line1=lines[0].split(',')
lines=lines[1::]    
for line in lines:
    y=line.split(',')
    dictionary[y[0]]={}
    for i in range(1,len(y)):
        dictionary[y[0]][line1[i]]=y[i]

f1.close()

f3=open("minwage.csv","r")
lines=f3.readlines()

for i in range(0, len(lines)):
    lines[i]=lines[i][0:-2]
line1=lines[0].split(',')
lines=lines[1::] 
for line in lines:
    y=line.split(',')
    dictionary[y[0]][y[1]]=[y[2],y[3]]

f3.close()
print(dictionary)


#Save the json object to a file
f2 = open("data.json", "w")
json.dump(dictionary, f2, indent = None)

print(f2)
f2.close()
