import requests
from requests.exceptions import Timeout

proxy_timeout =10



uids=[]
channels=[]
def fetchFirstPage(proxy=None):

    
    for pagenumber in range(0,100):
        print(pagenumber)
        
        url=f"https://www.aparat.com/api/fa/v1/video/video/list/tagid/1?page={pagenumber}"
        response=None
        included=[]
        try:
            if proxy==None:
                response = requests.request("GET", url, proxies=proxy, timeout=proxy_timeout)
            else:
                response = requests.request("GET", url, timeout=proxy_timeout)
            json_responce=response.json()
            included+=json_responce["included"]
        except Timeout:
            print(f"The request timed out after {proxy_timeout} seconds.")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")


        for includeditem in included:
            if includeditem["type"]=="channel":
                channels.append(includeditem["attributes"]["username"])
                
            if includeditem["type"]=="Video":
                uids.append(includeditem["attributes"]["uid"])

    return {"videos_uids":uids,"channels":list(set(channels))}


    
        
    
    

