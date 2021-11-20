#Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas

def recommend(inputs):
    # computing similaries
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    data = pandas.read_csv('./data/processed_data.csv')
    feature_column = "Complete Project Information"
    data[feature_column] = data[feature_column].fillna('')
    matrix = tfidf_vectorizer.fit_transform(data[feature_column])
    cosine_similarity = linear_kernel(matrix, matrix)

    # scoring
    final_scores = []
    for input in inputs:
        # score individual inputs and add the top to a list of candidates
        scores = list(enumerate(cosine_similarity[input]))
        scores = sorted(scores, key = lambda score: score[1], reverse = True)
        final_scores = final_scores + scores[1:6]

    # sort the final list of top recommended repos and take the top 5
    final_scores = sorted(final_scores, key = lambda score: score[1], reverse = True)
    final_scores = final_scores[1:6]
    print("Scores: " + str(final_scores))
    indices = [entry[0] for entry in final_scores]

    for input in inputs:
        print("Input " + str(input) + ": " + str(data["Repository Name"][input]) + " with the description: " + str(data["Description"][input]) + "\n---")

    for i in indices:
        print("Recommendation # " + str(i) + ": " + str(data["Repository Name"][i]) + ". desc: " + str(data["Description"][i]))
    return indices