"""
Downloads all favorite posts of the logged in user
"""

from pr0gramm import *

import logging
import time
import urllib.request
import socket

socket.setdefaulttimeout(30)  # this timeout is set for urlretrieve
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

try:
    import getpass
except Exception as e:
    logging.warning("WARNING Could not import getpass -> ignoring")


print("[!] type in your username:")
username = input("username: ")
pw = ""
try:
    pw = getpass.getpass()
except Exception as e:
    pw = input("password: ")

api = Api(username, pw)

favorite_posts = Posts()

logging.info("Started crawling")

for posts in api.get_collection_items_iterator(flag=api.calculate_flag(sfw=True, nsfp=True, nsfw=True, nsfl=True)):
    favorite_posts.extend(posts)
    time.sleep(0.2)
    logging.info("crawling -> got total of " + str(len(favorite_posts)) + " posts")

logging.info("Found a total of " + str(len(favorite_posts)) + " favorite posts")

logging.info("Extracting urls")
posts = [(post["id"], post["image"]) for post in favorite_posts]
logging.info("Done")

logging.info("[!] Starting download")
logging.info("[!] press CTRL-C if you want to stop the downloads")

try:
    try:
        os.mkdir("downloads")
    except FileExistsError:
        pass
    os.chdir("downloads")
except Exception as e:
    logging.warning("Could not mkdir download directory -> using current dir instead")

try:
    download_counter = 0
    for id, url in posts:
        logging.info("downloading post -> {}, number {} out of {},"
                     "total progress: {}%".format(id, download_counter, len(favorite_posts),
                                                  round(download_counter / len(favorite_posts) * 100, 2)))

        download_counter += 1

        try:
            downloads_path = os.path.join(os.getcwd(), str(id) + "." + url.split(".")[-1])
            if os.path.exists(downloads_path):
                logging.warning("post {} has already been downloaded -> skipping".format(id))
                continue

            if url.endswith(".mp4"):
                urllib.request.urlretrieve("https://vid.pr0gramm.com/" + url, downloads_path)
            else:
                urllib.request.urlretrieve("https://img.pr0gramm.com/" + url, downloads_path)
        except Exception as e:
            logging.warning("Downloading post with id {} failed because of error {}".format(id, str(e)))
            if posts.count((id, url)) <= 5:
                posts.append((id, url))
                logging.warning("--> Failed download will be re-added to queue for another try")
                time.sleep(2)
            else:
                logging.error("--> Post with id {} failed after 5 download attempts -> not trying again".format(id))

except KeyboardInterrupt:
    logging.info("[!] interrupt, stopping downloads")
    try:
        os.remove(os.path.join(os.getcwd(), str(id) + "." + url.split(".")[-1]))
    except Exception as e:
        logging.warning("Could not remove last downloaded post -> this can generally be ignored")
