from os import error, read
import pandas
import requests
from os.path import exists
from data.queries import *

def short_desc(value, limit):
    val = str(value)
    return (str(val[0:min(len(val), limit)]) + "...")

def get_repo_index(data, owner, repo_name):
    return data.loc[(data['Repository Name'] == repo_name) & (data['Username'] == owner)].index.values.item()

async def import_user(username):
    print('Importing your starred repos... Note that we\'re limited to the first 100 by GitHub\'s APIs')
    res = await run_general_query(get_starred_repos.replace(LOGIN_PLACEHOLDER, username))
    raw = res.get('data').get('user').get('starredRepositories').get('nodes')
    repos = ''
    for repo in raw:
        repos = repos + repo.get('nameWithOwner') + ' '
    repos = repos[0:-1]
    print('Discovered the following repos: ' + repos)
    return await fetch_repos(repos.split(' '))

# repoInfo is a list of strings in the format owner/repoName
async def fetch_repos(repoInfo):
    repoDatum = []
    for repo in repoInfo:
        print("Fetching " + str(repo) + "...")
        parts = str(repo).split("/")
        res = await run_data_query(full_github_repo_data, parts[0], parts[1])
        repoDatum.append(res)
    return append_data(repoDatum)

def append_data(repoDatum):
    if not exists('./data/processed_data.csv'):
        return error("Could not find processed data file")
    data = pandas.read_csv('./data/processed_data.csv', index_col = 0)
    indices = []
    for repoData in repoDatum:
        readme = get_readme_from_raw(repoData)
        owner = repoData.get("data").get("repo").get("owner").get("login")
        name = repoData.get("data").get("repo").get("name")
        lang = repoData.get("data").get("repo").get("languages").get("nodes")
        if len(lang) > 0:
            lang = lang[0].get("name")
        else:
            lang = "none"
        url = repoData.get("data").get("repo").get("url")
        desc = repoData.get("data").get("repo").get("description")
        stars = repoData.get("data").get("repo").get("stargazerCount")
        updated = repoData.get("data").get("repo").get("updatedAt")
        rawTags = repoData.get("data").get("repo").get("repositoryTopics").get("nodes")
        tags = ""
        for tag in rawTags:
            tags = tags + tag.get("topic").get("name") + ","
        tags = tags[0:-1]
        full_desc = str(desc) + " " + str(lang) + " " + str(tags) + " " + str(readme)
        df = pandas.DataFrame( \
            data = [[owner, name, desc, updated, lang, stars, tags, url, readme, full_desc]], \
            columns = [ \
                'Username', 'Repository Name', 'Description', 'Last Update Date', \
                'Language', 'Number of Stars', 'Tags', 'Url', 'Readme', 'Complete Project Information' \
            ])
        if is_value_missing_from_column(data, 'Repository Name', name):
            data = data.append(df, sort = True, ignore_index = True)
        else:
            print("Skipping addition of " + str(owner) + "/" + str(name) + " as it already exists")
        indices.append(get_repo_index(data, owner, name))
    data.to_csv("./data/processed_data.csv", encoding='utf-8')
    return indices
    
def is_value_missing_from_column(dataset, column, value):
    return len(dataset[dataset[column].str.contains(value)]) == 0

async def enrich_data():
    data = pandas.read_csv('./data/TopStaredRepositories.csv')
    readmes = []
    
    for i in range(0, data.__len__()):
        repo_name = data["Repository Name"][i]
        repo_owner = data["Username"][i]
        print("Processing repo # " + str(i) + " of " + str(data.__len__()))
        readmes.append(await fetch_readme(repo_owner, repo_name))

    data["Readme"] = readmes
    cols = ['Description', 'Language', 'Tags', 'Readme']
    data['Complete Project Information'] = data[cols].apply(lambda row: ' '.join(row.dropna().values.astype(str)), axis=1)
    data.to_csv("./data/processed_data.csv", encoding='utf-8')

async def run_data_query(query, owner, repo):
    q = str(query).replace(REPO_NAME_PLACEHOLDER, repo).replace(REPO_OWNER_PLACEHOLDER, owner)
    return await run_general_query(q)

async def run_general_query(query):
    pat = ""
    with open("./github_pat.txt") as f:
        pat = f.read()

    headers = {'Authorization': 'token %s' % pat}
    json_req = { 'query' : query }
    response = requests.post(url = 'https://api.github.com/graphql',json = json_req, headers = headers)
    return response.json()

def get_readme_from_raw(raw):
    readme_data = ""
    readme_candidates = raw.get("data").get("repo")

    if readme_candidates != None:
        for key, value in readme_candidates.items():
            if README_IDENTIFER not in str(key):
                continue
            if value != None:
                readme_data = str(value.get("text"))
                break
    return readme_data

async def fetch_readme(owner, repo_name):
    json_res = await run_data_query(github_readme_only, owner, repo_name)
    return get_readme_from_raw(json_res)

def clean_data():
    data = pandas.read_csv('./data/processed_data.csv', index_col = 0)
    for i in range(0, data.__len__()):
        # drop observations that have a core field missing
        if data["Description"][i] == None and data["Tags"][i] == None and data["Readme"][i] == None:
            data.drop([i, i])
            print("Dropping observation: " + i)

async def prepare_data():
    if not exists('./data/processed_data.csv'):
        await enrich_data()
    clean_data()
    print("Completed data processing.")