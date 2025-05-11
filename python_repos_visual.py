import requests
import sys

from plotly import offline

# Make an API call and store the response.
programming_lang = input("Enter the programming language: ")
page = input("Each page has 30 repos, choose a page:")
url = f'https://api.github.com/search/repositories?q=language:{programming_lang}&sort=stars&page={page}'
headers = {'Accept': 'application/vnd.github.v3+json'}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")
if r.status_code == 422:
    print("There was an error with your request")
    sys.exit()



# Process results.
response_dict = r.json()
# Explore information about the repositories.
repo_dicts = response_dict['items']
repo_links, stars, labels = [], [], []
for repo_dict in repo_dicts:
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url']
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)
    stars.append(repo_dict['stargazers_count'])

    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    label = f"{owner}<br />{description}"
    labels.append(label)

# Make visualization.
data = [{
    'type': 'bar',
    'x': repo_links,
    'y': stars,
    'hovertext': labels,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width':1.5, 'color':'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
}]

my_layout = {
    'title': {'text': f'Most-Starred Python Projects on Github, page={page}', 'font': {'size': 20}},
    'xaxis': {
        'title': {'text': 'Repository', 'font': {'size': 24}},
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': {'text': 'Stars', 'font': {'size': 24}},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='python_repos.html')