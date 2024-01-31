import requests
import random

def get(url):
    return requests.get(url).json()

userid = input("Enter a roblox userid: ")

check = int(input("How many requests do u wanna do eg. 50: "))
if check == None:
    check = 50
    print("Invalid Check its now 50")

followers = get(f"https://friends.roblox.com/v1/users/{userid}/followers/count")["count"]

print(f"{userid} has {followers} followers")

print("Scanning for bots")

fc = check
if check > followers:
    print("You will check with 100% Accuracy this may take a while")
    fc = followers / 100
    check = followers

userids = []
cursor = ""
loaded = 0
while True:
    newestf = get(f"https://friends.roblox.com/v1/users/{userid}/followers?limit=100&sortOrder=Desc&cursor={cursor}")
    loaded += 1
    for i in newestf["data"]:
        userids.append(i["id"])
    cursor = newestf["nextPageCursor"]
    if cursor is None:
        break
    if loaded > fc:
        break
    print("Loading Followers List " + str((loaded / fc) * 100) + "%")

randomchecks = random.sample(userids, min(check, len(userids)))

samplespace = len(randomchecks)
bots = 0

whoarebots = []

for index, user_id in enumerate(randomchecks):
    url = f"https://badges.roblox.com/v1/users/{user_id}/badges?sortOrder=Desc&limit=10"
    b = get(url)
    amount = len(b["data"])

    if amount < 1:
        bots += 1
        whoarebots.append(user_id)
    print("Checking if Users are Bots " + str((index / samplespace) * 100) + "%")


if samplespace != 0:
    bots_percentage = (bots / samplespace) * 100
    real_percentage = ((samplespace - bots) / samplespace) * 100
else:
    bots_percentage = 0
    real_percentage = 100

rf = round(followers * (real_percentage / 100))
rp = round(followers * (bots_percentage / 100))

print(f"Real Followers: {rf}")
print(f"Bot Followers: {rp}")
print("----")
print(f"Percentage of Botted Followers: {bots_percentage:.2f}%")
print(f"Percentage of Real Followers: {real_percentage:.2f}%")


print(str(len(whoarebots)) + " bots were found")
input("Press Enter to view the userid's of the bots")

print(whoarebots)

input("Press Enter again to close")
