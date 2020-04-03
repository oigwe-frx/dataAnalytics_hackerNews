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
 Original run in Jupyter Notebook

**Data Sets:**
 * The data set is of 12 months of Hacker News posts (up to September 26 2016) The data set has been reduced from almost 300,000 rows to approximately 20,000 rows by removing all submissions that did not receive any comments, and then randomly sampling from the remaining submissions. Below are descriptions of the columns:

    ```
    id: The unique identifier from Hacker News for the post
    title: The title of the post
    url: The URL that the posts links to, if it the post has a URL
    num_points: The number of points the post acquired, calculated as the total number of upvotes minus the total number of downvotes
    num_comments: The number of comments that were made on the post
    author: The username of the person who submitted the post
    created_at: The date and time at which the post was submitted
    ```     
    * File: *HN_posts_year_to_Sep_26_2016*

---
## Functions

**explore_data()** - Built to explore rows in a more readable way. There is an option in our function to show the number of rows and columns for any data set.

```
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

```
**is_app_English()** - We are not interested in analyzing non-English apps. Some of the apps have non-English names/titles. Our assumption is that a non-English names indicates a non-English app. This function is built to loop through the app names and find at least 3 characters with ASCII values over 127.

```
def is_app_English(string):
    ascii_greater_127 = []
    for character in string:
        value = ord(character)
        if value > 127:
            ascii_greater_127.append(character)
    if len(ascii_greater_127) > 3:
        return False
    else: 
        return True
```
**freq_table() & display_table()** - Two functions used to analyze the frequency tables:

* One function to generate frequency tables that show percentages
* Another function that we can use to display the percentages in a descending order

```
def freq_table(data_set, index):
    frequency_table = {}
    for app in data_set:
        data_point = app[index]
        if data_point in frequency_table:
            frequency_table[data_point] += 1
        else:
            frequency_table[data_point] = 1
    for key in frequency_table:
        frequency_table[key] = (frequency_table[key]/len(data_set))*100
    
    return frequency_table

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
```
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
print(hn[:5])

[['id', 'title', 'url', 'num_points', 'num_comments', 'author', 'created_at'], ['12224879', 'Interactive Dynamic Video', 'http://www.interactivedynamicvideo.com/', '386', '52', 'ne0phyte', '8/4/2016 11:52'], ['10975351', 'How to Use Open Source and Shut the Fuck Up at the Same Time', 'http://hueniverse.com/2016/01/26/how-to-use-open-source-and-shut-the-fuck-up-at-the-same-time/', '39', '10', 'josep2', '1/26/2016 19:30'], ['11964716', "Florida DJs May Face Felony for April Fools' Water Joke", 'http://www.thewire.com/entertainment/2013/04/florida-djs-april-fools-water-joke/63798/', '2', '1', 'vezycash', '6/23/2016 22:20'], ['11919867', 'Technology ventures: From Idea to Enterprise', 'https://www.amazon.com/Technology-Ventures-Enterprise-Thomas-Byers/dp/0073523429', '3', '1', 'hswarna', '6/17/2016 0:01']]
```
```
headers = hn[0]
print(headers)

['id', 'title', 'url', 'num_points', 'num_comments', 'author', 'created_at']
```
```
hn = hn[1:]
print(hn[:4])

[
    ['12224879', 'Interactive Dynamic Video', 'http://www.interactivedynamicvideo.com/', '386', '52', 'ne0phyte', '8/4/2016 11:52'], 

    ['10975351', 'How to Use Open Source and Shut the Fuck Up at the Same Time', 'http://hueniverse.com/2016/01/26/how-to-use-open-source-and-shut-the-fuck-up-at-the-same-time/', '39', '10', 'josep2', '1/26/2016 19:30'],
    
    ['11964716', "Florida DJs May Face Felony for April Fools' Water Joke", 'http://www.thewire.com/entertainment/2013/04/florida-djs-april-fools-water-joke/63798/', '2', '1', 'vezycash', '6/23/2016 22:20'],
    
    ['11919867', 'Technology ventures: From Idea to Enterprise', 'https://www.amazon.com/Technology-Ventures-Enterprise-Thomas-Byers/dp/0073523429', '3', '1', 'hswarna', '6/17/2016 0:01']
]


Number of rows:  20099
Number of columns: 7
```

---
## Data Cleaning

### Cleaning Goal 1: Incorrect Entry
The googleplaystore.csv has an error in row 10473 (counting header) 

```
print(google_apps_Data[10473])  # incorrect row
print('\n')
print(google_header)  # header
```
```
['Life Made WI-Fi Touchscreen Photo Frame', '1.9', '19', '3.0M', '1,000+', 'Free', '0', 'Everyone', '', 'February 11, 2018', '1.0.19', '4.0 and up']


['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type', 'Price', 'Content Rating', 'Genres', 'Last Updated', 'Current Ver', 'Android Ver']

```
The data for column 'Category' (which should be index 1 ([1])) was excluded.
We will remove the row.

`del apps_data_google[10473]`

### Cleaning Goal 2: Duplicates
The googleplaystore.csv has multiple entries for some apps. 

First we must figure out which apps have multiple entries.

```
        duplicate_apps = []
        unique_apps = []

        for app in apps_data_google:
            name = app[0]
            if name in unique_apps:
                duplicate_apps.append(name)
            else: 
                unique_apps.append(name)
```
```
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])

Number of duplicate apps: 1181


Examples of duplicate apps: ['Quick PDF Scanner + OCR FREE', 'Box', 'Google My Business', 'ZOOM Cloud Meetings', 'join.me - Simple Meetings', 'Box', 'Zenefits', 'Google Ads', 'Google My Business', 'Slack', 'FreshBooks Classic', 'Insightly CRM', 'QuickBooks Accounting: Invoicing & Expenses', 'HipChat - Chat Built for Teams', 'Xero Accounting Software']
```

We do not want to remove the duplicate entries at random. If we look at the multiple entries for the instagram app, we can see that the entries have different 'user ratings' count.

```
for app in google_apps_data:
    name = app[0]
    if name == 'Instagram':
        print(app)
```
```
['Instagram', 'SOCIAL', '4.5', '66577313', 'Varies with device', '1,000,000,000+', 'Free', '0', 'Teen', 'Social', 'July 31, 2018', 'Varies with device', 'Varies with device']
['Instagram', 'SOCIAL', '4.5', '66577446', 'Varies with device', '1,000,000,000+', 'Free', '0', 'Teen', 'Social', 'July 31, 2018', 'Varies with device', 'Varies with device']
['Instagram', 'SOCIAL', '4.5', '66577313', 'Varies with device', '1,000,000,000+', 'Free', '0', 'Teen', 'Social', 'July 31, 2018', 'Varies with device', 'Varies with device']
['Instagram', 'SOCIAL', '4.5', '66509917', 'Varies with device', '1,000,000,000+', 'Free', '0', 'Teen', 'Social', 'July 31, 2018', 'Varies with device', 'Varies with device']
```
We have decided to find and use the entry with the highest user rating count, per duplicate app.

```
        reviews_max = {}

        for app in apps_data_google[1:]:
            name = app[0]
            n_reviews = float(app[3])
            
            if name in reviews_max and reviews_max[name] < n_reviews:
                reviews_max[name] = n_reviews
            elif name not in reviews_max: 
                reviews_max[name] = n_reviews
```

We will remove any duplicate that has a user rating count that is lower than the count listed in the dictionary above 

```
google_clean = []
already_added = []

for app in apps_data_google[1:]:
    name = app[0]
    n_reviews = float(app[3])
            
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        google_clean.append(app)
        already_added.append(name)
```
### Cleaning Goal 3: Non-English Apps

We have come across apps that have non-English names. Our assumption is that a non-English name is an indication that the app is an non-English app. We do not want to analyze non-English apps. The characters we commonly use in English generally have ASCII (American Standard Code for Information Interchange) values in the of range 0 to 127. If we loop through the characters in the app names, and search for characters with an ASCII greater than 127, we can guess whether or not an app is an English based app. 

If an app name has more than 3 characters with ASCII values over 127, we will exclude the app data. This logic is our best effort to avoid removing apps that may have English names, but symbols like emoticons. 

```
google_clean_english = []
apple_clean_english = []

for app in google_clean:
    if is_app_English(app[0]):
        google_clean_english.append(app)
        
for app in apps_data_apple:
    if is_app_English(app[1]):
        apple_clean_english.append(app)
```
```
print(is_app_English('Docs To Go™ Free Office Suite'))
print(is_app_English('Instachat 😜'))
print(is_app_English('爱奇艺PPS -《欢乐颂2》电视剧热播'))

True
True
False
```

### Cleaning Goal 4: Removing Non-Free Apps

We only want to analyze the data for free apps, and thus must removed any priced apps from out dataset.

```
google_final = []
apple_final = []

for app in google_clean_english:
    if app[7] == 'Free':
        google_final.append(app)

for app in apple_clean_english:
    if app[4] == '0.0':
        apple_final.append(app)
```
---
## Analysis

### Most Common Genre

To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:

* Build a minimal Android version of the app, and add it to Google Play.
* If the app has a good response from users, we then develop it further.
* If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.

Our goal is to find app profiles that are successful on both markets. We will begin our analysis by building a frequency table for the prime_genre column of the App Store data set, and the Genres and Category columns of the Google Play data set. This analysis will determine what it the most frequently app genre. 

We will use the freq_table() and display_table() functions. 
* freq_tables() - will generate frequency tables that show percentages
* display_table - will display the percentages in a descending order

```
print('Google - Category Frequency Table',display_table(google_final,1))

FAMILY : 18.898792733837304
GAME : 9.725826469592688
TOOLS : 8.462146000225657
BUSINESS : 4.592124562789123
LIFESTYLE : 3.9038700214374367
PRODUCTIVITY : 3.8925871601038025 ...
```
```
print('Apple - prime_genre Frequency Table', display_table(apple_final, 11))

Games : 55.64595660749507
Entertainment : 8.234714003944774
Photo & Video : 4.117357001972387
Social Networking : 3.5256410256410255
Education : 3.2544378698224854 ...

```
In the Apple App Store, among the free English apps, more than a half (55%) are games. Entertainment apps are close to 8%.

At first glance games only make up 9% of apps, and it seems close to 19% of the apps are designed for family use. However, if we investigate this further, we can see that the family category means mostly games for kids.


### Most Installs

We will also attempt to analysize genre popularity, based on the number of installs. For the Google Play data set, we can find this information in the Installs column, but  the App Store data set does not have this specific data. We will use the total number of user ratings as a proxy, which we can find in the rating_count_tot app. 

```
apple_p_genres = freq_table(apple_final, 11)
google_Installs = freq_table(google_final,5)
```
#### Apple App Store

Below, we calculate the average number of user ratings per app genre on the App Store:
```
for genre in p_genres:
    total = 0
    len_genre = 0
    for app in apple_final:
        genre_app = app[11]
        if genre_app == genre:
            user_ratings_tot= float(app[5])
            total += user_ratings_tot
            len_genre += 1

    avg_user_ratings = total/len_genre
    print(genre, ':', avg_user_ratings)

```
```
Utilities : 14010.100917431193
News : 15892.724137931034
Food & Drink : 20179.093023255813
Reference : 67447.9
Book : 8498.333333333334 ...
```
The top three genres that have the highest number of average user reviews are:
```
Reference : 67447.9
Music : 56482.02985074627
Social Networking : 53078.195804195806

```
On further inspection, we have come to believe that the Music genre would not be the best direction for development. Approximately, 52% of the average reviews for apps in the music genre are for either the Pandora or the Spotify Music apps.

```
for app in apple_final:
    if app[11] == 'Music':
        print(app[1], ':', app[5])
```
```
Pandora - Music & Radio : 1126879
Spotify Music : 878563
Shazam - Discover music, artists, videos & lyrics : 402925
iHeartRadio – Free Music & Radio Stations : 293228
SoundCloud - Music & Audio : 135744
Magic Piano by Smule : 131695 ...
```
We can see a similar pattern of disproportionate distribution of reviews in the Social Networking genre. Apps such as Facebook, Pinterest, and Skype heavily influence the average number of reviews for the genre.

```
for app in apple_final:
    if app[11] == 'Social Networking':
        print(app[1], ':', app[5])
```
```
Facebook : 2974676
Pinterest : 1061624
Skype for iPhone : 373519
Messenger : 351466
Tumblr : 334293 ...
```
We can see a similar pattern of disproportionate distribution of reviews in the Reference genre. The Bible and Dictionary.com apps dominate; however, there does seem to be far less potential competition in the Reference genre compared to the Music and Social Networking genres. 
* Reference - 17 apps
* Music - 66 apps
* Social Networking - 103 apps

Also a 6 out of 17 reference apps were apps related to games. A reference app related to a popular game, may be successful. This idea coincides with the previously noted trend that the App Store is dominated by entertainment/for-fun apps.

```
for app in apple_final:
    if app[11] == 'Reference':
        print(app[1], ':', app[5])
```
```
Bible : 985920
Dictionary.com Dictionary & Thesaurus : 200047
Dictionary.com Dictionary & Thesaurus for iPad : 54175
Google Translate : 26786
Muslim Pro: Ramadan 2017 Prayer Times, Azan, Quran : 18418
New Furniture Mods - Pocket Wiki & Game Tools for Minecraft PC Edition : 17588
Merriam-Webster Dictionary : 16849
Night Sky : 12122
City Maps for Minecraft PE - The Best Maps for Minecraft Pocket Edition (MCPE) : 8535
LUCKY BLOCK MOD ™ for Minecraft PC Edition - The Best Pocket Wiki & Mods Installer Tools : 4693
GUNS MODS for Minecraft PC Edition - Mods Tools : 1497
Guides for Pokémon GO - Pokemon GO News and Cheats : 826
WWDC : 762
Horror Maps for Minecraft PE - Download The Scariest Maps for Minecraft Pocket Edition (MCPE) Free : 718
VPN Express : 14
Real Bike Traffic Rider Virtual Reality Glasses : 8
Jishokun-Japanese English Dictionary & Translator : 0
```
#### Google Play Store

The Google Play Store dataset provides us with an approximate number of installations per app.  

`display_table(google_final, 5)`

```
1,000,000+ : 15.728308699086089
100,000+ : 11.55365000564143
10,000,000+ : 10.549475346947986
10,000+ : 10.199706645605326
1,000+ : 8.394448832223853
100+ : 6.916393997517771
5,000,000+ : 6.826131106848697
500,000+ : 5.562450637481666
50,000+ : 4.772650344127271
5,000+ : 4.513144533453684
10+ : 3.542818458761142
500+ : 3.2494640640866526
50,000,000+ : 2.3017037120613786
100,000,000+ : 2.1324607920568655
50+ : 1.9180864267178157
5+ : 0.7898002933543946
1+ : 0.5077287600135394
500,000,000+ : 0.270788672007221
1,000,000,000+ : 0.2256572266726842
0+ : 0.045131445334536835
```
On first glance, the inprecision of the data may seem like it would be a problem. But we do not believe that this is the case. Our goal is to get a general idea of which app genre performs the best. We will leave the numbers as they are - we will consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on. 

The installations are presented in the csv as a string. We must convert the strings into floats. 

```
for category in categories:
    total = 0
    len_category = 0
    for app in google_clean_english_free:
        category_app = app[1]
        if category_app == category:
            remove = ''
            if '+' in app[5]:
                remove = app[5].translate({ord('+'): None})
            if ',' in app[5]:
                remove = remove.translate({ord(','): None})
            installs = float(remove)
            total += installs
            len_category += 1
    avg_user_ratings = total/len_category
    print(category, ':', avg_user_ratings)
```
```
PERSONALIZATION : 5201482.6122448975
TOOLS : 10801391.298666667
TRAVEL_AND_LOCAL : 13984077.710144928
BOOKS_AND_REFERENCE : 8767811.894736841
NEWS_AND_MAGAZINES : 9549178.467741935
DATING : 854028.8303030303 ...
```
The top three genres that have the highest installations are:

```
COMMUNICATION : 38,456,119.167247385
VIDEO_PLAYERS : 24727872.452830188
SOCIAL : 23,253,652.127118643
PHOTOGRAPHY : 17,840,110.40229885
PRODUCTIVITY : 16,787,331.344927534
GAME : 15,588,015.603248259
TRAVEL_AND_LOCAL : 13,984,077.710144928
ENTERTAINMENT : 11,640,705.88235294
TOOLS : 10,801,391.298666667
NEWS_AND_MAGAZINES : 9549178.467741935
BOOKS_AND_REFERENCE : 8767811.894736841

```
On average, communication apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:

```
for app in google_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])
```
```
WhatsApp Messenger : 1,000,000,000+
imo beta free calls and text : 100,000,000+
Android Messages : 100,000,000+
Google Duo - High Quality Video Calls : 500,000,000+
Messenger – Text and Video Chat for Free : 1,000,000,000+
imo free video calls and chat : 500,000,000+
Skype - free IM & video calls : 1,000,000,000+
Who : 100,000,000+
GO SMS Pro - Messenger, Free Themes, Emoji : 100,000,000+
LINE: Free Calls & Messages : 500,000,000+
Google Chrome: Fast & Secure : 1,000,000,000+
Firefox Browser fast & private : 100,000,000+
UC Browser - Fast Download Private & Secure : 500,000,000+
Gmail : 1,000,000,000+
Hangouts : 1,000,000,000+
Messenger Lite: Free Calls & Messages : 100,000,000+
Kik : 100,000,000+
KakaoTalk: Free Calls & Text : 100,000,000+
Opera Mini - fast web browser : 100,000,000+
Opera Browser: Fast and Secure : 100,000,000+
Telegram : 100,000,000+
Truecaller: Caller ID, SMS spam blocking & Dialer : 100,000,000+
UC Browser Mini -Tiny Fast Private & Secure : 100,000,000+
Viber Messenger : 500,000,000+
WeChat : 100,000,000+
Yahoo Mail – Stay Organized : 100,000,000+
BBM - Free Calls & Messages : 100,000,000+
```
If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times:

```
under_100_m = []

for app in google_final:
    n_installs = app[5]
    remove = ''
            if '+' in app[5]:
                remove = app[5].translate({ord('+'): None})
            if ',' in app[5]:
                remove = remove.translate({ord(','): None})
    if (app[1] == 'COMMUNICATION') and (float(remove) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)
```
`3603485.3884615386`

We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).

Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.

The books and reference genre was almost fairly popular, with an average number of installs of 8,767,811. We found this genre had potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.




