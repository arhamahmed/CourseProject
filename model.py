#Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from data.data_processing import short_desc
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
        final_scores = final_scores + scores[1:11]

    # sort the final list of top recommended repos and take the top 10
    final_scores = sorted(final_scores, key = lambda score: score[1], reverse = True)
    final_scores = final_scores[1:11]
    indices = [entry[0] for entry in final_scores]

    print()
    for input in inputs:
        print("Input: " + str(data["Repository Name"][input]) + "(" + short_desc(data["Description"][input], 75))
    print("--------------------")
    count = 0
    for i in indices:
        print("Recommendation # " + str(count) + ": " + str(data["Repository Name"][i]) + ": " + short_desc(data['Description'][i], 75))
        count = count + 1
    return indices