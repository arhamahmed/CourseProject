import asyncio
from model import recommend
from data.data_processing import prepare_data, fetch_repos, import_user
from evaluation import evaluate

loop = asyncio.get_event_loop()
print("One moment while the data is loaded...")
loop.run_until_complete(prepare_data())
print("How would you like your recommendations")
print("1 = import my GitHub profile")
print("2 = manually enter GitHub repos I like")
print("3 = manually enter IDs of available GitHub repos from a list of the top 980 (provided a link to the ones available")
selection = int(input())

if selection == 1:
    print("Enter your GitHub username, and all the repo's you've starred will be imported")
    indices = loop.run_until_complete(import_user(input()))
elif selection == 2:
    print("Enter a space-separated list of 'owner/repo_name' entries which are projects you like (e.g.: homebrew/brew dapr/dapr)")
    indices = loop.run_until_complete(fetch_repos(input().split(" ")))
else:
    print("Visit `https://www.kaggle.com/chasewillden/topstarredopensourceprojects` and enter the indices (0-based) of projects you like with spaces in between (e.g. 5 10 93)")
    indices = list(map(int, input().split(" ")))

recommendations = recommend(indices)
evaluate(recommendations)