from csv import reader 

opened_file = open('hacker_news.csv')
read_file = reader(opened_file) 
hn = list(read_file)

print(hn[:5])

headers = hn[0]
hn = hn[1:]
print(headers)
print(hn[:4])
print("length",len(hn))

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

print(len(ask_posts))
print(len(show_posts))
print(len(other_posts))