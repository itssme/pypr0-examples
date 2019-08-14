"""
Downloads the image url of all posts tagged with "schmuserkadser" which appeared in top
"""

from pr0gramm import *
from pr0gramm import sql_manager
import time
import urllib

api = Api()
schmuser_posts = Posts()

for posts in api.get_items_by_tag_iterator(tags="schmuserkadser", promoted=1):
    schmuser_posts.extend(posts)
    time.sleep(0.1)
    print "crawling -> " + str(len(schmuser_posts)) + " posts"

print "Found a total of " + str(len(schmuser_posts)) + " schmuserkadser posts"

# for demo purposes the posts are now saved to the database
# and then a select statement retrieves the image or video url of the posts
database = sql_manager.Manager("schmuser.db")

# if you get an error "UNIQUE constraint failed: posts.id" here, that means the database already has the post saved
database.insert_posts(schmuser_posts)
database.safe_to_disk()

posts = [(url[0], url[1]) for url in database.manual_command("select id, image from posts order by id desc;", wait=True)]
print posts

print "[!] press CTRL-C if you want to stop the downloads"

try:
    for id, url in posts:
        print "downloading post -> " + str(id)
        if url.endswith(".mp4"):
            urllib.urlretrieve("https://vid.pr0gramm.com/" + url, os.path.join(os.getcwd(), str(id) + "." + url.split(".")[-1]))
        else:
            urllib.urlretrieve("https://img.pr0gramm.com/" + url, os.path.join(os.getcwd(), str(id) + "." + url.split(".")[-1]))
except KeyboardInterrupt:
    print "[!] interrupt, closing db connection"
    database.sql_connection.close()
