import re
import netaddr
from bisect import bisect
import pandas as pd

with open("ip2location.csv") as f:
        df=pd.read_csv(f)
        
def lookup_region(ipaddr):
    ipaddr=re.sub("[a-z]","0",ipaddr)
    ipaddr=(int)(netaddr.IPAddress(ipaddr))
    index=bisect(df["low"],ipaddr)
    return df.iloc[index-1][3]

class Filing:
    def __init__(self,html):
        self.dates=self.getDates(html)
        listCodes=self.getCodes(html)
        if(len(listCodes)>0):
            self.sic=(int)(listCodes[0])
        else:
            self.sic=None
        self.addresses=self.getAddress(html)
    
    def getDates(self,file):
        return re.findall(r"(?<!\d)(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])(?!\d)",file)
    
    def getCodes(self,file):
        l=[]
        ls=re.findall(r"SIC=[\d]+",file)
        for element in ls:
            l.append((int)(element.split("=")[1]))
        return l
    
    
    def getAddress(self, text):
        addr_blocks = []
        # for each <div class="mailer">…</div>
        for block in re.findall(r'<div class="mailer">([\s\S]+?)</div>', text):
            # grab each span’s contents
            spans = re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', block)
            # strip whitespace and drop any blank strings
            lines = [s.strip() for s in spans if s.strip()]
            if lines:
                # join the lines with newlines
                addr_blocks.append("\n".join(lines))
        return addr_blocks
    def state(self):
        for address in self.addresses:
            cleaned_address = " ".join(address.split())
            match = re.search(r'\b([A-Z]{2})\s\d{5}\b', cleaned_address)
            if match:
                return match.group(1)
        return None
    
    

    
    
    



        
    
   
        
    
            

    

  
    
    
    
    