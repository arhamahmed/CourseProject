# todo:
# - evaluation:
# -     explicit: ask some ppl to try it out
# -     implicit: compare top ranked docs with ones ppl actually click on in the results (track clicks)
from model import recommend
from data.data_processing import prepare_data, fetch_repos, import_user
import asyncio

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
    loop.run_until_complete(import_user('arhamahmed'))
elif selection == 2:
    print("Enter a space-separated list of 'owner/repo_name' entries which are projects you like (e.g.: homebrew/brew dapr/dapr)")
    loop.run_until_complete(fetch_repos(input().split(" ")))
else:
    print("Open up `https://www.kaggle.com/chasewillden/topstarredopensourceprojects` in a browser and enter the indices (0-based) of projects you like with spaces in between (e.g. 5 10 93)")
    input_indices = list(map(int, input().split(" ")))
    recommend(input_indices)