race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "5": "White",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander"
}
import json
import csv
from io import TextIOWrapper
from zipfile import ZipFile
import pandas as pd
with open("banks.json","r") as f:
    bankDict=json.load(f)
class Applicant:
    def __init__(self,age,race):
        self.age=age
        self.race=set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])# appending textual representation of the race to self.race instance attribute
                
    def __repr__(self):
        l=list(self.race)
        l.sort()
        return f"{type(self).__name__}({self.age!r}, {l})"
    def lower_age(self):
        ageRange=self.age.replace("<","").replace(">","")
        return (int)(ageRange.split("-")[0])
    def __lt__(self,other):
        return self.lower_age()<other.lower_age()
    
class Loan:
    def __init__(self,values):
        self.loan_amount=self.float_extract(values['loan_amount'])
        self.property_value=self.float_extract(values['property_value'])
        self.interest_rate=self.float_extract(values['interest_rate'])
        self.applicants=[]
        #step1 find all keys with a particular prefix
        candidate_keys=[key for key in values.keys() if "applicant_race-" in key]
        raceApplicant1=[]
        raceApplicant2=[]
        for key in candidate_keys:
            raceNumber=values[key]
            if("co-" in key):
                raceApplicant2.append(raceNumber)
            else:
                raceApplicant1.append(raceNumber)
        applicant1=Applicant(values["applicant_age"],raceApplicant1)
        self.applicants.append(applicant1)
        if "co-applicant_age" in values.keys() and values["co-applicant_age"]!='9999':
            applicant2=Applicant(values["co-applicant_age"],raceApplicant2)
            self.applicants.append(applicant2)
            
    def __str__(self):
        return f"<{type(self).__name__}: {self.interest_rate}% on ${self.loan_amount} with {len(self.applicants)} applicant(s)>"
    
    
    def __repr__(self):
        return f"<{type(self).__name__}: {self.interest_rate}% on ${self.loan_amount} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self,yearly_payment):
        assert self.interest_rate>0 and self.loan_amount>0
        amt=self.loan_amount
        while amt>0:
            yield amt
            amt+=(self.interest_rate)/100*amt
            amt-=yearly_payment             
                
    def float_extract(self,string):
        if string=="NA" or string=="Exempt":
            return -1
        return float(string)

class Bank:
    def __init__(self,name):
        self.loan_list=[]#an empty list to contain a list of loans associated with this current bank with this particular lei id
        self.name=name# name of the bank-so a particular instance attribute
        for bank in bankDict:
            if bank["name"]==self.name:
                self.lei=bank["lei"]#initialize lei id value to the bank if we could find it in the database of unique banks
                with ZipFile("wi.zip") as zf:
                    with zf.open("wi.csv","r") as csvfile:
                        # first make an IOWrapper to convert bytes sequence to string sequence
                        tio=TextIOWrapper(csvfile)
                        # now instead of fassing a file object csvfile to DictReader(which is composed of bytes) we pass in TEXTIOWRAPPER object which is composed of string characters
                        reader = csv.DictReader(tio)
                        for row in reader:
                            # each row is a loan pertaining to some bank so get all lones of this particular bank with this lei id
                            if row["lei"]==self.lei:
                                obj=Loan(row)
                                # make a loan object by this particular row(each row represents a loan)
                                self.loan_list.append(obj)                                           
                break
    def __getitem__(self,index):
        return self.loan_list[index]
    def __len__(self):
        return len(self.loan_list)
        
                        
                        
                    
        
        