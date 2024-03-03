import aiohttp
import asyncio
import requests
from datetime import datetime

timeout_seconds=10
from aiohttp_socks import ProxyConnector
import aiohttp
from datetime import datetime
import asyncio

async def get_video_comments(video_uid, proxy=None):
    comment_list = []
    url = f"https://www.aparat.com/api/fa/v1/video/comment/list/videohash/{video_uid}"
    querystring = {"perpage": "999999999999999"}
    
    connector = ProxyConnector.from_url(proxy)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Aparat api error {response.status}")
            data = await response.json()
    
    if not data.get("data"):
        return {"uid": video_uid, "data": None}

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

    return comment_list


async def getVideoDetail(videouid,proxy=None):
    url = "https://www.aparat.com/api/fa/v1/video/video/show/videohash/"+videouid
    response=None
    global video

    connector = ProxyConnector.from_url(proxy)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Aparat api error {response.status}")
            data = await response.json()



    
    included=data["data"]
    
    
    

    
    video={
        "platform": "Aparat",
        "_":"video",
        "id":included["id"] if "id" in included else None,
        "owner_username":included["attributes"]["owner_username"] if "owner_username" in included["attributes"] else None,
        "owner_id":int(included["relationships"]["Channel"]["data"]["id"]) ,
        "title":included["attributes"]["title"] if "title" in included["attributes"] else None,
        "tags":included["attributes"]["tags"] if "tags" in included["attributes"] else None,
        "uid":included["attributes"]["uid"] if "uid" in included["attributes"] else None,
        "visit_count":int(included["attributes"]["visit_cnt_non_formatted"]),
        
        "owner_name":data["included"][0]["attributes"]["name"] ,
        
        "poster":included["attributes"]["big_poster"] if "big_poster" in included["attributes"] else None,
        "owner_avatar":data["included"][0]["attributes"]["avatar"],
        "duration":int(included["attributes"]["duration"]) if "duration" in included["attributes"] else 0,
        "posted_date":included["attributes"]["sdate_real"] ,
        "posted_timestamp":int(datetime.strptime(included["attributes"]["sdate_real"], "%Y-%m-%d %H:%M:%S").timestamp()) ,#2015-05-17 12:12:51
        
        "sdate_rss":included["attributes"]["sdate_real"] ,
        "sdate_rss_tp":int(datetime.strptime(included["attributes"]["sdate_real"], "%Y-%m-%d %H:%M:%S").timestamp()) ,#2015-05-17 12:12:51
        "comments":None,
        "frame":included["attributes"]["frame"] if "frame" in included["attributes"] else None,
        "like_count":int(included["attributes"]["like_cnt_non_formatted"]) if "like_cnt_non_formatted" in included["attributes"] and included["attributes"]["like_cnt_non_formatted"] != None else 0,
        "description":included["attributes"]["description"] if "description" in included["attributes"]  else None,
        "is_deleted": False,

    }
    return video



async def main(videouid, proxy=None):
    # asyncio.gather is used to run multiple tasks concurrently, and it needs to be awaited
    comment_data, video_data = await asyncio.gather(
        get_video_comments(videouid, proxy),
        getVideoDetail(videouid, proxy)
    )

    video_data["comments"] = comment_data
    return video_data

# Example usage:
# Assuming get_video_comments and getVideoDetail are defined elsewhere and are async functions

async def getVideoDetails(videouid,proxy):
    video_details = await main(videouid,proxy)
    return video_details

#asyncio.run(getVideoDetails("ZhRQG", None))

# print(main("ZhRQG", proxy=None))