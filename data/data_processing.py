import pandas
import requests
from os.path import exists

def enrich_data():
    data = pandas.read_csv('./data/TopStaredRepositories.csv')
    REPO_NAME = "<REPO_NAME>"
    REPO_OWNER = "<REPO_OWNER>"
    readmes = []
    
    for i in range(0, data.__len__()):
        repo_name = data["Repository Name"][i]
        repo_owner = data["Username"][i]
        print("Processing repo # " + str(i) + " of " + str(data.__len__()))
        query = """
            query {
                repo: repository(name: "<REPO_NAME>", owner: "<REPO_OWNER>") {
                    ...RepoFragment
                }
            }

            fragment RepoFragment on Repository {
                parseReadmeAttempt1: object(expression: "master:README.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt2: object(expression: "master:README.MD") {
                    ...ReadmeText
                }
                parseReadmeAttempt3: object(expression: "master:readme.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt4: object(expression: "master:Readme.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt5: object(expression: "master:README") {
                    ...ReadmeText
                }
                parseReadmeAttempt6: object(expression: "main:README.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt7: object(expression: "main:README.MD") {
                    ...ReadmeText
                }
                parseReadmeAttempt8: object(expression: "main:readme.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt9: object(expression: "main:Readme.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt10: object(expression: "main:README") {
                    ...ReadmeText
                }
                parseReadmeAttempt11: object(expression: "develop:README.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt12: object(expression: "develop:README.MD") {
                    ...ReadmeText
                }
                parseReadmeAttempt13: object(expression: "develop:readme.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt14: object(expression: "develop:Readme.md") {
                    ...ReadmeText
                }
                parseReadmeAttempt15: object(expression: "develop:README") {
                    ...ReadmeText
                }
            }

            fragment ReadmeText on GitObject {
                ... on Blob {
                    text
                }
            }
        """.replace(REPO_NAME, repo_name).replace(REPO_OWNER, repo_owner)

        pat = ""
        with open("./github_pat.txt") as f:
            pat = f.read()

        headers = {'Authorization': 'token %s' % pat}
        json_req = { 'query' : query }
        response = requests.post(url = 'https://api.github.com/graphql',json = json_req, headers = headers)
        json_res = response.json()
        readme_data = ""

        readme_candidates = json_res.get("data").get("repo")
        if readme_candidates != None:
            for key, value in readme_candidates.items():
                if value != None:
                    readme_data = str(value.get("text"))
                    break
        readmes.append(readme_data)

    data["Readme"] = readmes
    # data["Complete Project Information"] = data[["Description", "Tags", "Readme"]].agg(' '.join, axis = 1)
    data["Complete Project Information"] = data["Description"] + " " + \
                                           data ["Tags"] + " " + \
                                           data["Language"] + " " + \
                                           data["Readme"]
    data.to_csv("./data/processed_data.csv", encoding='utf-8')

def clean_data():
    data = pandas.read_csv('./data/processed_data.csv')
    for i in range(0, data.__len__()):
        # drop observations that have
        if data["Description"][i] == None and data["Tags"][i] == None and data["Readme"][i] == None:
            data.drop([i, i])
            print("Dropping observation: " + i)

if not exists('./data/processed_data.csv'):
    enrich_data()
clean_data()

print("Completed processing.")