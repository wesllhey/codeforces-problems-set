# codeforces-problems-set
The main idea of this project is an attempt to observe the patterns of problems solved by users with rating >= 2800 on codeforces. In this way, divide and categorize all problems by rating, tags and the number of users who solve the same problem.

With this, generating an optimized and smart list of problems based on the pattern of the path of the grandmasters on codeforces.

# install dependencies
```
$ pip3 install -r requirements.txt   
```

# run
```
$ python3 main.py
```

As the framework used is flask, by default the port is `5000`, just open your favorite browser and enter on `http://127.0.0.1:5000/` url. 

# update csv
The project is based on the `/csv/out.csv` which is generated by the `csv/csv_generator.py` if you want to keep the csv updated, just run.
```
$ cd ./csv/
$ python3 csv_generator.py
```
# csv generator
On the `csv/csv_generator.py` file, has a constant called `MIN_RATING` by default the value is 2800 which means that the behavior will take a look only for users with rating >= 2800, be free to update this value.

# ui
The ui is very simple, just a table with the problems, by default, sorted by rating (ask) and the number of users which solve the problem (desc).

![alt text](./blob/ui.png?raw=true)

# filters
- Tags, e.g.: dsu, trees, dp, graph, math
- Rating range e.g.: 1500-2000
- Min users count e.g.: 30 (will return only problems with at least 30 users which solved it)
