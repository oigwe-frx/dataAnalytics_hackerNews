# Hacker News

**Premise:**
 Hacker News is a site started by the startup incubator Y Combinator, where user-submitted stories ( "posts") are voted and commented upon. Hacker News is extremely popular in tech and startup circles, and posts that make it to the top of Hacker News' listings can get hundreds of thousands of visitors as a result.

**Goal:**
 Our goal for this project is to analyze data to learn:
* Which posts receive more comments on average - posts whose titles begin with "Ask HN" or posts whose titles begin with "Show HN"?
* Do posts created at a certain time receive more comments on average?
 

**Language:**
 Python

**Tools:**
 Originally run in Jupyter Notebook

**Data Sets:**
 * The data set is of 12 months of Hacker News posts (up to September 26 2016) The data set has been reduced from almost 300,000 rows to approximately 20,000 rows by removing all submissions that did not receive any comments, and then randomly sampling from the remaining submissions. Below are descriptions of the columns:
    * **id**: The unique identifier from Hacker News for the post
    * **title**: The title of the post
    * **url**: The URL that the posts links to, if it the post has a URL
    * **num_points**: The number of points the post acquired, calculated as the total number of upvotes minus the total number of downvotes
    * **num_comments**: The number of comments that were made on the post
    * **author**: The username of the person who submitted the post
    * **created_at**: The date and time at which the post was submitted
      
* File: *HN_posts_year_to_Sep_26_2016*

---

## Opening CSV Files

```
from csv import reader 

### Hacker News Post Year to September 16, 2006 ###

opened_file = open('/data_sets/HN_posts_year_to_Sep_26_2016.csv')
read_file = reader(opened_file) 
hn = list(read_file)


```
**Initial Exploration of Data**

```
print("First 5 rows of the data set", hn[:5])


First 5 rows of the data set 

[
    ['id', 'title', 'url', 'num_points', 'num_comments', 'author', 'created_at',

    ['12224879', 'Interactive Dynamic Video', 'http://www.interactivedynamicvideo.com/', '386', '52', 'ne0phyte', '8/4/2016 11:52'],

    ['10975351', 'How to Use Open Source and Shut the Fuck Up at the Same Time', 'http://hueniverse.com/2016/01/26/how-to-use-open-source-and-shut-the-fuck-up-at-the-same-time/', '39', '10', 'josep2', '1/26/2016 19:30'],
    
    ['11964716', "Florida DJs May Face Felony for April Fools' Water Joke", 'http://www.thewire.com/entertainment/2013/04/florida-djs-april-fools-water-joke/63798/', '2', '1', 'vezycash', '6/23/2016 22:20'],
    
    ['11919867', 'Technology ventures: From Idea to Enterprise', 'https://www.amazon.com/Technology-Ventures-Enterprise-Thomas-Byers/dp/0073523429', '3', '1', 'hswarna', '6/17/2016 0:01']
]
```
```
headers = hn[0]
print("Header ", headers)

Header ['id', 'title', 'url', 'num_points', 'num_comments', 'author', 'created_at']

```
```
hn = hn[1:]
print("Data set without header row", hn)


Data set without header row [
    ['12224879', 'Interactive Dynamic Video', 'http://www.interactivedynamicvideo.com/', '386', '52', 'ne0phyte', '8/4/2016 11:52'], 

    ['10975351', 'How to Use Open Source and Shut the Fuck Up at the Same Time', 'http://hueniverse.com/2016/01/26/how-to-use-open-source-and-shut-the-fuck-up-at-the-same-time/', '39', '10', 'josep2', '1/26/2016 19:30'],
    
    ['11964716', "Florida DJs May Face Felony for April Fools' Water Joke", 'http://www.thewire.com/entertainment/2013/04/florida-djs-april-fools-water-joke/63798/', '2', '1', 'vezycash', '6/23/2016 22:20'],
    
    ['11919867', 'Technology ventures: From Idea to Enterprise', 'https://www.amazon.com/Technology-Ventures-Enterprise-Thomas-Byers/dp/0073523429', '3', '1', 'hswarna', '6/17/2016 0:01']
]
```

Number of rows:  20099

Number of columns: 7


---
## Analysis 

### Filtering
We are only concerned with post titles beginning with "Ask HN" or "Show HN". We will create a new list of lists containing just the data for those titles.

```
ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    if title.lower().startswith("ask hn"):
        ask_posts.append(row)
    elif title.lower().startswith("show hn"):
        show_posts.append(row)
    else: other_posts.append(row)
```
---

### Does title choice affect comment count?

Let's determine if "Ask HN" posts or "Show HN" posts receive more comments on average
```
total_ask_comments = 0

for entry in ask_posts:
    num_comments = int(entry[4])
    total_ask_comments += num_comments

avg_ask_comments = total_ask_comments/len(ask_posts)
print("Avg Ask Comments:", avg_ask_comments)

Avg Ask Comments: 14.038417431192661

```
```
total_show_comments = 0

for entry in show_posts:
    num_comments = int(entry[4])
    total_show_comments += num_comments

avg_show_comments = total_show_comments/len(show_posts)
print("Avg Show Comments:", avg_show_comments)

Avg Show Comments: 10.31669535283993

```
**Conclusion:** 

Based on the data analyzed, posts that begin with "Ask HN" receive on average more comments. Since ask posts are more likely to receive comments, we'll focus our remaining analysis just on these posts.

---

### Does time of the day affect comment count?

Next, we will determine if ask posts created at a certain time are more likely to attract comments. We'll use the following steps to perform this analysis:

* Calculate the amount of ask posts created in each hour of the day, along with the number of comments received.
* Calculate the average number of comments ask posts receive by hour created.

```
import datetime as dt

result_list = [["created_at", "num_comments"]]

for row in ask_posts:
    result_list.append([row[6], int(row[4])])

counts_by_hour = {}
comments_by_hour = {}

for row in result_list[1:]:
    date_time_str = row[0]
    date_time_obj = dt.datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")
    parsed_hour = date_time_obj.hour

    if parsed_hour not in counts_by_hour:
        counts_by_hour[parsed_hour] = 1

        comments_by_hour[parsed_hour] = row[1]

    else: 
        counts_by_hour[parsed_hour] += 1
        comments_by_hour[parsed_hour] += row[1]
```
```
print("Number of Posts per hour", counts_by_hour)
Note: The hour key is denoted in military time (24 hour). Ex. 1pm = 13

Number of Posts per hour {0: 55, 1: 60, 2: 58, 3: 54, 4: 47, 5: 46, 6: 44, 7: 34, 8: 48, 9: 45, 10: 59, 11: 58, 12: 73, 13: 85, 14: 107, 15: 116, 16: 108, 17: 100, 18: 109, 19: 110, 20: 80, 21: 109, 22: 71, 23: 68}

```
```
print("Number of Comments per hour", comments_by_hour)
Note: The hour key is denoted in military time (24 hour). Ex. 1pm = 13

Number of Comments per hour {0: 447, 1: 683, 2: 1381, 3: 421, 4: 337, 5: 464, 6: 397, 7: 267, 8: 492, 9: 251, 10: 793, 11: 641, 12: 687, 13: 1253, 14: 1416, 15: 4477, 16: 1814, 17: 1146, 18: 1439, 19: 1188, 20: 1722, 21: 1745, 22: 479, 23: 543}
```

Next, we'll use these two dictionaries to calculate the average number of comments for posts created during each hour of the day.

```
avg_by_hour = [["hour", "avg"]]

for hour in comments_by_hour:
    avg_by_hour.append([hour, (comments_by_hour[hour]/counts_by_hour[hour])])
```
```
print("Average number of comments each hour", avg_by_hour) 

```
```
Average number of comments each hour [
    ['hour', 'avg'],
    [0, 8.127272727272727], 
    [1, 11.383333333333333], 
    [2, 23.810344827586206], 
    [3, 7.796296296296297], 
    [4, 7.170212765957447], 
    [5, 10.08695652173913], 
    [6, 9.022727272727273], 
    [7, 7.852941176470588], 
    [8, 10.25], 
    [9, 5.5777777777777775], 
    [10, 13.440677966101696], 
    [11, 11.051724137931034], 
    [12, 9.41095890410959], 
    [13, 14.741176470588234], 
    [14, 13.233644859813085], 
    [15, 38.5948275862069], 
    [16, 16.796296296296298], 
    [17, 11.46], 
    [18, 13.20183486238532], 
    [19, 10.8], 
    [20, 21.525], 
    [21, 16.009174311926607], 
    [22, 6.746478873239437], 
    [23, 7.985294117647059]
]
```
Although we now have the results we need, this list of list format is difficult to read and identify the hours with the highest values. We will finish by sorting the list of lists and printing the five highest values in a format that's easier to read.

```
print("Top 5 Hours for Ask Posts Comments")

for row in sorted_swap[:5]:
    hour_conversion=dt.datetime.strptime(str(row[1]), "%H").strftime("%H:00")
    conclusion = "{hour}: {average:.2f} average comments per post".format(average=row[0], hour=hour_conversion)
    print(conclusion)

```
```
Top 5 Hours for Ask Posts Comments
15:00: 38.59 average comments per post
02:00: 23.81 average comments per post
20:00: 21.52 average comments per post
16:00: 16.80 average comments per post
21:00: 16.01 average comments per post

```
**Conclusion:** 

According to the data analyzed, time posted does affect the average number of comments a post can receive. The best time to post is between 15:00 and 16:00 hours (between 3-4pm). Posts made during this time receive on average 38.59 comments. The worst time to post is between 23:00 and 0:00 hours (11pm-12am). Posts made during this time receive on average 7.99 average comments. 




