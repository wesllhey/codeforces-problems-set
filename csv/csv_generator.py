import csv, requests

USER_RATED_ENDPOINT = 'https://codeforces.com/api/user.ratedList?activeOnly=true&includeRetired=false'

USER_STATUS_ENDPOINT = 'https://codeforces.com/api/user.status?handle={handle}'

res = requests.get(url = USER_RATED_ENDPOINT)

users_rated_json = res.json()

all_users = users_rated_json['result']

MIN_RATING = 2800

users_filtered = []

for u in all_users:
    if 'rating' in u and u['rating'] >= MIN_RATING:
        users_filtered.append(u)

problems_count = dict()
problems_by_rating = dict()

for u in users_filtered:
    res = requests.get(url = USER_STATUS_ENDPOINT.format(handle = u['handle']))
    submissions_by_user_json = res.json()

    all_submissions = submissions_by_user_json['result']

    for s in all_submissions:
        if 'problem' not in s:
            continue

        problem = s['problem']

        if 'rating' not in problem:
            continue

        rating = problem['rating']
        key = str(problem['contestId']) + str(problem['index'])

        if rating not in problems_by_rating:
            problems_by_rating[rating] = []

        if key not in problems_count:
            problems_count[key] = 0
            problems_by_rating[rating].append(problem)

        problems_count[key] += 1

fields = ['name', 'rating', 'users_count', 'tags', 'link']

result = []

for rating, value in problems_by_rating.items():

    for p in value:
        tag = ', '.join(p['tags'])

        link = 'https://codeforces.com/problemset/problem/{contestId}/{index}'\
            .format(contestId = p['contestId'], index = p['index'])

        problem_key = str(p['contestId']) + str(p['index'])

        problem = []

        problem.append(p['name'])
        problem.append(rating)
        problem.append(problems_count[problem_key])
        problem.append(tag)
        problem.append(link)

        result.append(problem)

with open('out.csv', 'w') as f:
    write = csv.writer(f)

    write.writerow(fields)
    write.writerows(result)