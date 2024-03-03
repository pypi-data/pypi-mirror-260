import requests
from datetime import datetime
timeout_seconds=10



nub=0
included=[]
def fetchSearchResult(url,proxy=None):
    global nub
    global included

    if proxy==None:
        response = requests.request("GET", url,proxies=proxy, timeout=timeout_seconds)
    else:
        response = requests.request("GET", url, timeout=timeout_seconds)

    json_responce=response.json()
    if json_responce["data"][0]["attributes"]["link"] != None:
        nextpage=json_responce["data"][0]["attributes"]["link"]["next"]
        
        
        
        nub+=1
        print(nub)
        if nextpage != None and nextpage!="":
            included+=json_responce["included"]
            fetchSearchResult(nextpage)
    else:
        print(f"fetching done in {nub} pages.")
        print(type(included))
    
    return included


def searchByKeyword(keyword,uploadedIn=None,proxy=None):
    timeout_seconds=10

    if len(keyword)<3:
        raise ValueError(f"keyword input: must me in range of 3 to 512 character")

    valid_uploadedIn=["today","year","week",None]
    if uploadedIn not in valid_uploadedIn:
        raise ValueError(f"Invalid input: {uploadedIn}. Expected one of {valid_uploadedIn}")
    url=None
    if uploadedIn==None:
        url=f"https://www.aparat.com/api/fa/v1/video/video/search/text/{keyword}/?type_search=search"
    else:
        url=f"https://www.aparat.com/api/fa/v1/video/video/search/text/{keyword}/?type_search=search&uploadedIn={uploadedIn}"


    raw_results=fetchSearchResult(url)

    uids=[]
    channels=[]
    for raw_result in raw_results:
        if raw_result["type"]=="channel":
            channels.append(raw_result["attributes"]["username"])
             


        if raw_result["type"]=="Video":
            uids.append(raw_result["attributes"]["uid"])


    

    return {"raw_results":raw_results,"videos_uids":uids,"channels":channels}

