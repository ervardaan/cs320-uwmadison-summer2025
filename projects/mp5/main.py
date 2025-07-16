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
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

"""
I chose national long term water quality monitoring data from the government of canada
https://data-donnees.az.ec.gc.ca/data/substances/monitor/national-long-term-water-quality-monitoring-data/Water-Qual-Eau-Sites-National.csv
"""

app=Flask(__name__)
last_visit=0
ip_list=[]
count=0
version_visit={}
num_subscribed=0
email_list={}

@app.route("/")
def homePage():
    global count
    with open("index.html") as f:
        count+=1
        htmlFileRead=f.read()
        if(count<11):
            if(count%2==0):
                htmlFileRead=htmlFileRead.replace("Donate","Please Donate for hungry kids around the world and help alleviate hunger crisis and child trafficking")
                htmlFileRead=htmlFileRead.replace("from=A","from=B")
        else:
            if("A" in version_visit and "B" in version_visit):
                if(version_visit["A"]<version_visit["B"]):
                    htmlFileRead=htmlFileRead.replace("Donate","Please Donate for hungry kids around the world and help alleviate hunger crisis and child trafficking")
                    htmlFileRead=htmlFileRead.replace("from=A","from=B")
            elif("B" in version_visit):
                htmlFileRead=htmlFileRead.replace("Donate","Please Donate for hungry kids around the world and help alleviate hunger crisis and child trafficking")
                htmlFileRead=htmlFileRead.replace("from=A","from=B")
            else:
                pass            
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
        htmlFileRead=f.read()
    return htmlFileRead
    

@app.route("/email",methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    if len(re.findall(r"^[A-Za-z0-9_]+@[A-Za-z0-9_]+\.[A-Za-z]{3}$", email)) > 0: # 1
        if email in email_list:
            return jsonify(f"thanks, your subscriber number was {email_list[email]} because you had already subscribed!") 
        num_subscribed+=1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        email_list[email]=num_subscribed
        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")
    return jsonify("Please stop being so careless—enter a valid email!") # 3


@app.route("/dashboard1.svg")
def dashboard1():
    # read data
    df = pd.read_csv("main.csv")

    # get bins from query string (default 10)
    bins = int(request.args.get("bins", 10))

    # create histogram of the SAME columns/axes every time
    fig, ax = plt.subplots()
    df["LATITUDE"].hist(bins=bins, ax=ax)
    ax.set_title("Latitude Distribution")
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Number of Sites")

    # decide output filename
    if "bins" in request.args:
        out_file = "dashboard1-query.svg"
    else:
        out_file = "dashboard1.svg"

    # save, close, and return
    fig.savefig(out_file)
    plt.close(fig)
    with open(out_file, "rb") as f:
        return Response(f.read(), mimetype="image/svg+xml")


@app.route("/dashboard2.svg")
def dashboard2():
    # read data
    df = pd.read_csv("main.csv")

    # create scatterplot of two DIFFERENT columns
    fig, ax = plt.subplots()
    ax.scatter(df["LONGITUDE"], df["LATITUDE"], alpha=0.7)
    ax.set_title("Site Locations (Longitude vs. Latitude)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    out_file = "dashboard2.svg"
    fig.savefig(out_file)
    plt.close(fig)
    with open(out_file, "rb") as f:
        return Response(f.read(), mimetype="image/svg+xml")

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,threaded=False)
    