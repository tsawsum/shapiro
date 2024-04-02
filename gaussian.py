# cleaning texts
import pandas as pd
import re
import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from collections import Counter
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import seaborn as sns
import tomotopy
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    recall_score,
    precision_score,
    ConfusionMatrixDisplay,
    f1_score,
)

nltk.download('stopwords')

df = pd.read_csv('Agreed.csv', delimiter=',')
dataset = [list(row) for row in df.values]
             
dataset = pd.DataFrame(dataset)
# dataset.columns = ["Title", "Olivia", "George", "Final", "Capital", "List", "Imperative", "Mystery", "Emotional", "Xs"]
dataset.columns = ["Title", "Label"]

titles = dataset.iloc[:, 0]
cats = dataset.iloc[:, 1]

cv = CountVectorizer(min_df=10, max_df=0.4) # words must show up in at least 5 and no more than 40% of documents
features = cv.fit_transform(titles).toarray()
print(features.shape)
vocab = cv.get_feature_names_out()
print(vocab)
 
# nltk.download('stopwords')
 
# corpus = []
 
# for i in range(0, 100):
#     text = re.sub('[^a-zA-Z]', '', dataset['Title'][i])
#     text = text.lower()
#     text = text.split()
#     ps = PorterStemmer()
#     text = ''.join(text)
#     corpus.append(text)
 
# # creating bag of words model
# cv = CountVectorizer(max_features = 1500)
 
# X = cv.fit_transform(corpus).toarray()
# y = dataset.iloc[:, 1].values

X_train, X_test, y_train, y_test = train_test_split(
           features, cats, test_size = 0.25, random_state = 0)

classifier = GaussianNB();
classifier.fit(X_train, y_train)
 
# predicting test set results
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(y_pred)
print(y_test)

print("Accuracy: " , accuracy)
print("Precision: ",  precision)
print("F1: ", f1)
print("Recall: ",  recall)
 
# making the confusion matrix
cm = confusion_matrix(y_test, y_pred)
