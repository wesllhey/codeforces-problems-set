import csv, os
from genericpath import isfile

from flask import Flask, render_template, request

class Problem:
    def __init__(self, name, rating, users_count, tags, link):
        self.name = name
        self.rating = rating
        self.users_count = users_count
        self.tags = tags
        self.link = link
    def __str__(self): 
        return "Problems: name={name}, rating={rating}, users_count={users_count}, tags={tags}, link={link}"\
            .format(name = self.name, rating = self.rating, users_count = self.users_count, tags = self.tags, link = self.link)

class Tag:
    def __init__(self, name, count):
        self.name = name
        self.count = count

all_problems = []
all_tags = []
tags_count = dict()

CSV_PATH = './csv/out.csv'

if os.path.isfile(CSV_PATH):
    with open(CSV_PATH) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            tags = set(row['tags'].split(', '))

            for tag in tags:
                if len(tag) == 0:
                    tag = 'empty'
                
                if tag not in tags_count:
                    tags_count[tag] = 0
                
                tags_count[tag] += 1

            problem = Problem(row['name'], int(row['rating']), int(row['users_count']), tags, row['link'])
            all_problems.append(problem)

for key, value in tags_count.items():
    all_tags.append(Tag(key, int(value)))

all_problems.sort(key=lambda p : (p.rating, -p.users_count))

all_tags.sort(key=lambda t : t.count, reverse=True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rating_start = request.form['rating_start']
        rating_end = request.form['rating_end']
        tags = set(request.form.getlist('tags'))

        has_rating_filter = False
        
        if rating_start and rating_end:
            rating_start = int(rating_start)
            rating_end = int(rating_end)
            has_rating_filter = True

        if not has_rating_filter and not tags:
            return render_template('index.html', problems=all_problems, tags_count=all_tags)    

        filtered_problems = []

        for p in all_problems:
            if has_rating_filter:
                if p.rating < rating_start or p.rating > rating_end:
                    continue
                    
            if tags:
                can_skip = True

                for t in tags:
                    if t in p.tags:
                        can_skip = False
                        break
                
                if can_skip:
                    continue
            
            filtered_problems.append(p)

        return render_template('index.html', problems=filtered_problems, tags_count=all_tags)

    return render_template('index.html', problems=all_problems, tags_count=all_tags)

app.run()