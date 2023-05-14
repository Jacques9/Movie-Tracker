import json, pymongo
with open('Movie-Analytics/movies.json') as f:
    movies = json.load(f)

for movie in movies:
    print(movie['title'])

print('2212121212121')
