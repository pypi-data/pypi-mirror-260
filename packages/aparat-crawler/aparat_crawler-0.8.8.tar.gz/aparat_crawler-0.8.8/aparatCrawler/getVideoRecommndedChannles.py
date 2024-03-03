import requests


def get_video_recom(videouid,proxy=None):
    
    url = "https://www.aparat.com/api/fa/v1/video/recom/list_v2/videohash/"+videouid
    response=None
    timeout_seconds=10
    
    if proxy==None:
        response = requests.request("GET", url, timeout=timeout_seconds)
    else:
        response = requests.request("GET", url, proxies=proxy, timeout=timeout_seconds)

    json_responce=response.json()
    attribute=json_responce["data"]["attributes"]["video_recom"]
    channels=[]
    videos=[]
    for attribute in json_responce["data"]["attributes"]["video_recom"]:
        channels.append(attribute["username"])
        videos.append(attribute["uid"])

            
    return {"videos_uids":videos,"channels":list(set(channels))}