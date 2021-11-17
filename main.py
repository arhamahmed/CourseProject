# todo:
# - evaluation:
# -     explicit: ask some ppl to try it out
# -     implicit: compare top ranked docs with ones ppl actually click on in the results (track clicks)
# - ui/cli:
# -     allow importing of github profile if enough time
# -     cleaner ui for selecting repos e.g. just browsing list of dataset repos
from model import recommend
from data.data_processing import prepare_data

prepare_data()
print("Input the index of a repository you like and want recommendations for (a number):")
input_indices = list(map(int, input().split(" ")))
recommend(input_indices)