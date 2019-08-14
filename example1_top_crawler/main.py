from pr0gramm import *
from pr0gramm import sql_manager
import time

# pip install statistics
import statistics

api = Api()
manager = sql_manager.Manager("example.db")

print "Type in the number of days you want to crawl back"
time_days = 1
try:
    time_days = float(raw_input("?: "))
except:
    print "[!] input has to be a number (using standard => 1 day)"

top_posts = Posts()
max_date = None
for posts in api.get_items_iterator(promoted=1):
    top_posts.extend(posts)

    if max_date is None:
        max_date = top_posts.maxDate()

    if max_date - top_posts.minDate() >= 86400*time_days:
        break

    time.sleep(0.1)
    print "crawling"

posts = top_posts
top_posts = Posts()
for post in posts:
    if post["created"] > max_date - 86400*time_days:
        top_posts.append(post)

upvote_list = [post["up"]-post["down"] for post in top_posts]
print "Number of Posts: " + str(len(top_posts))
print "Total Benis in Posts: " + str(sum(upvote_list))
print "Mean points: " + str(statistics.mean(upvote_list))
print "Median points: " + str(statistics.median(upvote_list))
print "Standard deviation: " + str(statistics.stdev(upvote_list))

manager.insert(top_posts)
manager.safe_to_disk()

print manager.manual_command("select id, up-down, user"
                             "  from posts"
                             " where up-down > 300;", wait=True)
manager.sql_connection.close()