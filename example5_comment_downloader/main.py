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

all_comments = Comments()

logging.info("Started crawling")

# change username accordingly if you want to crawl comments from someone else
for comments in api.get_user_comments_iterator(username, flag=api.calculate_flag(True)):
    all_comments.extend(comments)
    time.sleep(0.3)

    logging.info(f"crawling -> already found {len(all_comments)} comments")

logging.info(f"Found a total of {len(all_comments)} comments")

with open("all_comments.json", "w") as writer:
    writer.write(str(all_comments))

with open("all_comments_formatted.txt", "w") as writer:
    writer.write("\n\n------------\n\n".join([comment["content"] for comment in all_comments]))

logging.info(
    "Done crawling, wrote all comments in json format to file 'all_comments.json' "
    "and wrote comments in a readable format in 'all_comments_formatted.txt'")
