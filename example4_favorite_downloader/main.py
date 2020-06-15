"""
Downloads all favorite posts of the logged in user
"""

from pr0gramm import *

import time
import getpass
import urllib.request

print("[!] type in your username:")
api = Api(input(), getpass.getpass())

favorite_posts = Posts()

print("Started crawling")

for posts in api.get_collection_items_iterator():
    favorite_posts.extend(posts)
    time.sleep(0.2)
    print("crawling -> got total of " + str(len(favorite_posts)) + " posts")

print("Found a total of " + str(len(favorite_posts)) + " favorite posts")

print("Extracting urls")
posts = [(post["id"], post["image"]) for post in favorite_posts]
print("Done")

print("[!] Starting download")
print("[!] press CTRL-C if you want to stop the downloads")

try:
    for id, url in posts:
        print("downloading post -> " + str(id))
        if url.endswith(".mp4"):
            urllib.request.urlretrieve("https://vid.pr0gramm.com/" + url, os.path.join(os.getcwd(), str(id) + "." + url.split(".")[-1]))
        else:
            urllib.request.urlretrieve("https://img.pr0gramm.com/" + url, os.path.join(os.getcwd(), str(id) + "." + url.split(".")[-1]))
except KeyboardInterrupt:
    print("[!] interrupt, stopping downloads")
