import requests
import json

conf = {
    "myFid": "",  # your fid
    "barier": "",  # tokenBarier
    "fidTarget": ""  # fidTarget
}

# Dapatkan informasi konfigurasi
tokenBarier = conf["barier"]
myFid = conf["myFid"]

print("get fid", myFid)
print("get barier", tokenBarier)

threshold = 1000

urlGetFollowers = "https://client.warpcast.com/v2/followers?fid={}&limit={}"
urlGetFollowerCount = "https://client.warpcast.com/v2/profile-casts?fid={}&limit=1"
urlFollow = "https://client.warpcast.com/v2/follows"

headers = {
    'authority': 'client.warpcast.com',
    'accept': '*/*',
    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer ' + tokenBarier,
    'content-type': 'application/json; charset=utf-8',
    'fc-amplitude-device-id': 'RHcQ1GzjH-9qsvlnMlVriG',
    'fc-amplitude-session-id': '1707233061257',
    'if-none-match': 'W/"J+6FScokLa8cs2EWfP+Ka3mLI0A="',
    'origin': 'https://warpcast.com',
    'referer': 'https://warpcast.com/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}


def get_list_user_by_fid(myFid):
    getFollowerCount = setup_request("GET", urlGetFollowerCount.replace("{}", myFid), headers)
    fidUser = getFollowerCount["result"]["casts"][0]["author"]["displayName"]
    print("jumlah follower", fidUser, getFollowerCount["result"]["casts"][0]["author"]["followerCount"])
    detailFollowers = setup_request("GET", urlGetFollowers.replace("{}", myFid).replace("{}", str(getFollowerCount["result"]["casts"][0]["author"]["followerCount"])), headers)
    return detailFollowers["result"]["users"]


def setup_request(method, url, headers):
    response = requests.request(method, url, headers=headers)
    return response.json()


def do_loop(users, followFollowing, unfollowNotFollow, followFidFollower):
    for user in users:
        isFollowing = user["viewerContext"]["following"]
        isFollowedBy = user["viewerContext"]["followedBy"]

        if unfollowNotFollow:
            if isFollowing and not isFollowedBy:
                print(user["displayName"], "not follow you")
                if user["followerCount"] < threshold:
                    print("unfollow not airdrop project owner")
                    payload = {"targetFid": user["fid"]}
                    response = requests.put(urlFollow, data=json.dumps(payload), headers=headers)
                    print(response.json())

        elif followFollowing:
            if not isFollowing and isFollowedBy and myFid == "239815":
                print("you didn't follow", user["displayName"])
                payload = {"targetFid": user["fid"]}
                response = requests.put(urlFollow, data=json.dumps(payload), headers=headers)
                print(response.json())

        elif followFidFollower:
            if not isFollowing:
                print("you didn't follow", user["displayName"])
                payload = {"targetFid": user["fid"]}
                response = requests.put(urlFollow, data=json.dumps(payload), headers=headers)
                print(response.json())

        if isFollowing and isFollowedBy:
            print("you're mutual", user["displayName"])


def run_automation(menu):
    try:
        if menu == 1:
            print("using Fid", conf["myFid"])
            users = get_list_user_by_fid(myFid)
            do_loop(users, True, False, False)
        elif menu == 2:
            print("using Fid", conf["myFid"])
            users = get_list_user_by_fid(myFid)
            do_loop(users, False, True, False)
        elif menu == 3:
            print("using Fid", conf["fidTarget"])
            users = get_list_user_by_fid(myFid)
            do_loop(users, False, False, True)
        else:
            print("do nothing")
    except Exception as e:
        print("masuk except", e)
