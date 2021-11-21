def evaluate(given_indices):
    print("Of these recommendations, which would you click if this was a browser?")
    print("Please enter a space-separated list: ")
    clicked_indices = input()
    print("The model had {}% utility".format(len(clicked_indices.split(" "))/len(given_indices) * 100))