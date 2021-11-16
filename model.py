#Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas

print("Input the index of a repository you like and want recommendations for (a number):")
# TODO: index of liked repo(s), make it a list, ensure it's in dataset else fetch the data for it
input = int(input())

# computing similaries
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
data = pandas.read_csv('./data/processed_data.csv')
feature_column = "Complete Project Information"
data[feature_column] = data[feature_column].fillna('')
matrix = tfidf_vectorizer.fit_transform(data[feature_column])
cosine_similarity = linear_kernel(matrix, matrix)

# scoring
scores = list(enumerate(cosine_similarity[input]))
scores = sorted(scores, key = lambda score: score[1], reverse = True)
scores = scores[1:6]
print("Scores: " + str(scores))
indices = [entry[0] for entry in scores]
print("indices: " + str(indices))

print("Input: " + str(data["Repository Name"][input]) + " with the description: " + str(data["Description"][input]))
print()
for i in indices:
    print("Recommendation # " + str(i) + ": " + str(data["Repository Name"][i]) + ". desc: " + str(data["Description"][i]))