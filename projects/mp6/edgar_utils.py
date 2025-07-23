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

    
    
    
    