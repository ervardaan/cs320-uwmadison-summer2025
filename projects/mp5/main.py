'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 4 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP5
Student 1:vardaan kapoor, vkapoor5
'''
import pandas as pd
from flask import Flask,request,jsonify,Response
import csv
import json
import time

"""
I chose national long term water quality monitoring data from the government of canada
https://data-donnees.az.ec.gc.ca/data/substances/monitor/national-long-term-water-quality-monitoring-data/Water-Qual-Eau-Sites-National.csv
"""

app=Flask(__name__)
last_visit=0
ip_list=[]
count=0
version_visit={}

@app.route("/")
def homePage():
    global count
    with open("index.html") as f:
        count+=1
        htmlFileRead=f.read()
        if(count<11 and count%2==0):
            htmlFileRead=htmlFileRead.replace("Donate","Please Donate for hungry kids around the world and help alleviate hunger crisis and child trafficking")
            htmlFileRead=htmlFileRead.replace("from=A","from=B")
    print(version_visit)
    return htmlFileRead

@app.route("/browse.html")
def browseHTMLpage():
    contents=pd.read_csv('main.csv')
    return "<h1>{}</h1>".format("Browse")+contents.to_html()

@app.route("/browse.json")
def jsonContent():
    if(request.remote_addr not in ip_list):
        ip_list.append(request.remote_addr)
    global last_visit
    if time.time()-last_visit>60:
        last_visit=time.time()
    else:
        return Response("<b>go away</b>",status=429,headers={"Retry-After":60})
    
    with open('main.csv', mode='r', newline='', encoding='utf-8') as csvfile:             
        data = list(csv.DictReader(csvfile))
        
    return jsonify(data)

@app.route("/visitors")
def getVisitors():
    return ip_list

@app.route("/donate.html")
def donationPage():
    with open("donate_page.html") as f:
        #arguments=dict(request.args)
        #version=arguments["from"]
        version=request.args.get("from","unknown")
        if(version not in version_visit):
            version_visit[version]=1
        else:
            version_visit[version]+=1
        print(version_visit)
        htmlFileRead=f.read()
    return htmlFileRead
    

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,threaded=False)
    