import requests
from datetime import datetime
from requests.exceptions import Timeout
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

timeout_seconds=10

def getchannelvideocount(username,proxy=None):
    response=None
    url = "https://www.aparat.com/api/fa/v1/user/user/information/username/" + username
    try:
        if proxy==None:
            response = requests.request("GET", url, proxies=proxy, timeout=10)
        else:
            response = requests.request("GET", url, timeout=10)
    except Timeout:
        print("The request timed out after 10 seconds.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

    if response.status_code == 404:
        return 404
    data = response.json()
    video_cnt=int(data["data"]["attributes"]["video_cnt"])

    return video_cnt


def get_video_commnets(video_uid,proxy=None):
    comment_list=[]
    url = "https://www.aparat.com/api/fa/v1/video/comment/list/videohash/"+video_uid
    querystring = {"perpage":"999999999999999"}
    payload = ""
    response=""
    
    if proxy != None:
        response = requests.request("GET", url, data=payload,proxies=proxy, timeout=timeout_seconds)
    else:
        response = requests.request("GET", url, timeout=10)
    data=response.json()
    
    if data["data"]:
       pass
    else:
        #print("no commnet")
        return {"uid":video_uid ,"data":None}
    comment_list=[]
    for comment in data["data"]:
        userid=comment["relationships"]["channel"]["data"]["id"]
        comment_owner_username=""
        comment_owner_name=""
        username_list=[]

        for item in data["included"]:
            if item.get("id") == userid:
                found_object = item
                comment_owner_username=found_object["attributes"]["username"]
                comment_owner_name=found_object["attributes"]["name"]
                comment_owner_avatar=found_object["attributes"]["avatar"]
                break

        cmnt={
            "uid": video_uid,
            "id":  comment["attributes"]["id"] if "id" in comment["attributes"] else None,
            "body": comment["attributes"]["body"] if "body" in comment["attributes"]else None,
            "reply": comment["attributes"]["reply"] if "reply" in comment["attributes"]else None,
            "date_gregorian": comment["attributes"]["sdate_gregorian"] if "sdate_gregorian" in comment["attributes"]else None,
            "timestamp": int(datetime.strptime(comment["attributes"]["sdate_gregorian"], "%Y-%m-%d %H:%M:%S").timestamp()) if "sdate_gregorian" in comment["attributes"]else None,
            "like_count": int(comment["attributes"]["like_cnt"]) if "like_cnt" in comment["attributes"] else None,
            "reply_count": int(comment["attributes"]["reply_cnt"]) if "reply_cnt" in comment["attributes"] else None,
            "owner_id": userid,
            "owner_username": comment_owner_username,
            "owner_name": comment_owner_name,
            "owner_avatar": comment_owner_avatar
        }
        comment_list.append(cmnt)

    data={"uid":video_uid,
                "data":comment_list}

    return data




def getvideos(usrname,pagenumber,proxy=None):

    payload = ""
    headers = {"cookie": "playIconOnHover_1=new; AFCN=169320560431281; apr_lb_id=m25","User-Agent": "firefox/2023.5.3"}
    videos=[]

    print(f"printing {pagenumber} page")

    url = f"https://www.aparat.com/api/fa/v1/user/video/list/username/{usrname}/page/{pagenumber}/perpage/40/isnextpage/true"
    response = requests.request("GET", url, data=payload,proxies=proxy, headers=headers, timeout=10)
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

        comment_data=get_video_commnets(included["attributes"]["uid"],proxy)

        video={
            "platform": "Aparat",
            "_":"video",
            "id":included["id"] if "id" in included else None,
            "owner_username":included["attributes"]["username"] if "username" in included["attributes"] else None,
            "owner_id":int(included["attributes"]["userid"]) if "userid" in included["attributes"] else 0,
            "title":included["attributes"]["title"] if "title" in included["attributes"] else None,
            "tags":included["attributes"]["tags"] if "tags" in included["attributes"] else None,
            "uid":included["attributes"]["uid"] if "uid" in included["attributes"] else None,
            "visit_count":int(included["attributes"]["visit_cnt_int"]) if "visit_cnt_int" in included["attributes"] and included["attributes"]["visit_cnt_int"].isdigit() else 0,
            "owner_name":included["attributes"]["sender_name"] if "sender_name" in included["attributes"] else None,
            "poster":included["attributes"]["big_poster"] if "big_poster" in included["attributes"] else None,
            "owner_avatar":included["attributes"]["profilePhoto"] if "profilePhoto" in included["attributes"] else None,
            "duration":int(included["attributes"]["duration"]) if "duration" in included["attributes"] else 0,
            "posted_date":included["attributes"]["sdate_rss"] ,
            "posted_timestamp":int(datetime.strptime(included["attributes"]["sdate_rss"], "%Y-%m-%d %H:%M:%S").timestamp()) ,#2015-05-17 12:12:51
            
            "sdate_rss":included["attributes"]["sdate_rss"] ,
            "sdate_rss_tp":int(datetime.strptime(included["attributes"]["sdate_rss"], "%Y-%m-%d %H:%M:%S").timestamp()) ,#2015-05-17 12:12:51
            "comments":comment_data["data"],
            "frame":included["attributes"]["frame"] if "frame" in included["attributes"] else None,
            "like_count":int(included["attributes"]["like_cnt"]) if "like_cnt" in included["attributes"] and included["attributes"]["like_cnt"] != None else 0,
            "description":included["attributes"]["description"] if "description" in included["attributes"]  else None,
            "is_deleted": False,

        }
        videos.append(video)

    return videos

def run_in_threads(usrname,pagenumbers,proxy, max_workers=10):
    # This function takes an array of arguments and runs `your_function`
    # on each element, using multiple threads.
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create a list of future tasks
        futures = [executor.submit(getvideos,usrname, pagenumber,proxy) for pagenumber in pagenumbers]

        # Wait for all futures to complete and collect results
        results = []
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error in thread: {e}")

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
    print(videos)
    return videos

    










