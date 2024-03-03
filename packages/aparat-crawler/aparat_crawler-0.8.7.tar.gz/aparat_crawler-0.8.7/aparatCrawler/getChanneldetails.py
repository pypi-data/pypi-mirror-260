import requests
from requests.exceptions import Timeout
from persian import convert_ar_characters
from datetime import datetime



def convert_numerical_string_to_int(numerical_string):
    converted = convert_ar_characters(numerical_string)
    if "میلیارد" in converted:
        return int(float(converted.replace(" میلیارد", "")) * 1000000000)
    if "میلیون" in converted:
        return int(float(converted.replace(" میلیون", "")) * 1000000)
    elif "هزار" in converted:
        return int(float(converted.replace(" هزار", "")) * 1000)
    else:
        data = ""
        try:
            data = int(converted)
        except:
            data = ""

        return data



def channelDetail(username,proxy=None):
    global response
    response=None
    url = "https://www.aparat.com/api/fa/v1/user/user/information/username/" + username
    print("--------------------")
    print(url)
    print(proxy)
    print("--------------------")

    try:
        response = requests.request("GET", url, proxies=proxy, timeout=10)
    except Timeout:
        print("The request timed out after 10 seconds.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    print()
    if response.status_code == 404:
        return 404
    data = response.json()
    data=data["data"]["attributes"]

    new_channel = {
        "_":"channel",
        "username": data["username"] if "username" in data else None,
        "userid": int(data["id"]) if "id" in data and data["id"] is not None else None,
        "avatar_thumbnail": data["pic_m"] if "pic_m" in data else None,
        "is_official": True if 'official' in data and data['official'] is not None else False,
        "name": data["name"] if "name" in data else None,
        "bio_links": [data["url"]] if "url" in data and data["url"] != '' else None,
        "description": data["description"] if "description" in data else None,
        "total_video_visit": int(convert_numerical_string_to_int(data["video_visit"])) if "video_visit" in data and data["video_visit"]!="" else 0,
        "video_count": int(data["video_cnt"]) if "video_cnt" in data and data["video_cnt"] is not None else None,
        "start_date": data["start_date"] if data["start_date"] else None,
        "start_date_timestamp": int(datetime.strptime(data["start_date"], "%Y-%m-%d").timestamp()),
        "followers_count":int(convert_numerical_string_to_int(data["follower_cnt"])) if "follower_cnt" in data and data["follower_cnt"] not in [None, ""] else None,
        "following_count": int(convert_numerical_string_to_int(data["follow_cnt"])) if "follow_cnt" in data and data["follow_cnt"] not in [None, ""] else None,
        "is_deleted": False,
        "country": "iran",
        "platform": "aparat"
    }

    return new_channel