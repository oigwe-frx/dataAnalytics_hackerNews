Opening CSV Files
from csv import reader 

opened_file = open('/data_sets/HN_posts_year_to_Sep_26_2016.csv')
read_file = reader(opened_file) 
apps_data = list(read_file)
