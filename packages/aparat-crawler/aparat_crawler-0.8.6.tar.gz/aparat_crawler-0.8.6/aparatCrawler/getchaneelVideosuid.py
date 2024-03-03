import requests
from datetime import datetime
from requests.exceptions import Timeout
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

timeout_seconds=10

def getchannelvideocount(username,proxy=None):
    response=None
    url = "https://www.aparat.com/api/fa/v1/user/user/information/username/" + username
    # try:
        
    response = requests.request("GET", url, proxies=proxy, timeout=10)
    print(response)
# except Timeout:
    #print("The request timed out after 10 seconds.")
# except requests.RequestException as e:
    #print(f"An error occurred: {e}")

    if response.status_code == 404:
        return 404
    data = response.json()
    video_cnt=int(data["data"]["attributes"]["video_cnt"])

    return video_cnt





def getvideos(usrname,pagenumber,proxy=None):

    payload = ""
    headers = {"cookie": "playIconOnHover_1=new; AFCN=169320560431281; apr_lb_id=m25","User-Agent": "firefox/2023.5.3"}
    videos_uids=[]

    print(f"printing {pagenumber} page")

    url = f"https://www.aparat.com/api/fa/v1/user/video/list/username/{usrname}/page/{pagenumber}/perpage/40/isnextpage/true"
    response = requests.request("GET", url, data=payload,proxies=proxy, headers=headers, timeout=10)
    print(response)

    data=response.json()

    total=data["data"][0]["attributes"]["total"]

    includeds=data["included"]

    for included in includeds:
        if "uid" in included["attributes"]:
            UID=included["attributes"]["uid"]  
        else:
            break
        

        if "id" not in included:
            break

        videos_uids.append(included["attributes"]["uid"])


    return videos_uids

def run_in_threads(usrname,pagenumbers,proxy, max_workers=10):
    # This function takes an array of arguments and runs `your_function`
    # on each element, using multiple threads.
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create a list of future tasks
        futures = [executor.submit(getvideos,usrname, pagenumber,proxy) for pagenumber in pagenumbers]

        # Wait for all futures to complete and collect results
        results = []
        for future in as_completed(futures):
            # try:
            result = future.result()
            results.append(result)
            # except Exception as e:
            #     print(f"Error in thread: {e}")

        return results

def main(usrname,video_count,proxy):
    if not video_count:
        video_count=getchannelvideocount(usrname,proxy)
        
    maxpage=math.ceil(video_count/40)+1
    print(f"channel {usrname} total pages is {maxpage}")
    pages=list(range(1,maxpage))
    if maxpage>15:
        max_workers=15
    else:
        max_workers=maxpage

    results = run_in_threads(usrname,pages,proxy,max_workers=max_workers)
    videos=[]
    for result in results:
        videos+=result
    #print(videos)
    return videos

    










