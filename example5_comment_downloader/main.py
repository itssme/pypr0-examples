import logging
import time

from pr0gramm import *

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

all_comment = Comments()

logging.info("Started crawling")

# change username accordingly if you want to crawl comments from someone else
for comments in api.get_user_comments_iterator(username, flag=api.calculate_flag(True)):
    all_comment.extend(comments)
    time.sleep(0.3)

    logging.info(f"crawling already found {len(all_comment)} comments")

logging.info(f"Found a total of {len(all_comment)} comments")

with open("all_comments.json", "w") as writer:
    writer.write(str(all_comment))

logging.info("Done crawling, wrote all comments in json format to file 'all_comments.json'")
