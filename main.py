# todo:
# - data:
# -     read data: read csv file
# -     enrich data: add readme column by scraping url link
# -     format data: create new column `full_desc`  = description + tags + readme
# -     clean data: remove observations that have empty full `full_desc`
# - modelling:
# -     create model
# -     train model / create predictions
# -     return top ranked docs
# - evaluation:
# -     explicit: ask some ppl to try it out
# -     implicit: compare top ranked docs with ones ppl actually click on in the results (track clicks)
# - ui/cli:
# -     input can be list of topics
# -     optionally allow importing of github profile if enough time
# -     output is model results