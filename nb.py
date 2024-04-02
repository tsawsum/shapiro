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
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score,
)

nltk.download('stopwords')

df = pd.read_csv('Agreed.csv', delimiter=',')
dataset = [list(row) for row in df.values]
             
dataset = pd.DataFrame(dataset)
dataset.columns = ["Title", "Label"]

titles = dataset.iloc[:, 0]
cats = dataset.iloc[:, 1]

cv = CountVectorizer(min_df=10, max_df=0.4) # words must show up in at least 5 and no more than 40% of documents
features = cv.fit_transform(titles).toarray()
print(features.shape)
vocab = cv.get_feature_names_out()
print(vocab)

mnb = MultinomialNB()
feat_train, feat_test, label_train, label_test = train_test_split(features, cats, test_size=0.2)
mnb.fit(feat_train, label_train)
preds = mnb.predict(feat_test)
 
confusion_matrix = confusion_matrix(label_test, preds)

log_odds = mnb.feature_log_prob_[1] - mnb.feature_log_prob_[0]
wd_list = sorted([i for i in zip(log_odds, vocab)])

print(wd_list[:50])

stoplist = set(stopwords.words('english'))
n_topics = 10
n_docs = len(dataset)

mdl = tomotopy.LDAModel(k=n_topics)
for title in titles:
  mdl.add_doc([w for w in title if w not in stoplist and w.isalpha()])

iters_per_check = 50
for i in range(0, 1000, iters_per_check):
    mdl.train(iters_per_check)
    print('Iteration: {}\tLog-likelihood: {}'.format(i+iters_per_check, mdl.ll_per_word))

print("Top 25 words by topic")
for k in range(n_topics):
    print('#{}: {}'.format(k, ' '.join([w for (w, prop) in mdl.get_topic_words(k, top_n=10)])))

mdl.summary()

doc_topic_props = np.zeros(shape=(n_docs, n_topics))
for i, doc in enumerate(mdl.docs):
    doc_topic_props[i, :] = doc.get_topic_dist()

n_clusters = 5
kmm = KMeans(n_clusters=n_clusters)
cluster_labels = kmm.fit_predict(doc_topic_props)

sent_labels = np.array(cats)
for k in range(n_clusters):
    # Which documents have the right cluster label
    cluster_doc_idxs = np.argwhere(cluster_labels == k).ravel()
    cat_count = Counter(sent_labels[cluster_doc_idxs])
    cluster_size = len(cluster_doc_idxs)
    print("Cluster {}: {} total, {:.1f}% positive".format(k, cluster_size, cat_count['pos'] * 100 / cluster_size))

n_sample_docs = 4
for k in range(n_clusters):
    print("Documents in cluster k:")
    cluster_doc_idxs = np.argwhere(cluster_labels == k).ravel()
    random_doc_idxs = np.random.choice(cluster_doc_idxs, size=n_sample_docs, replace=False)
    for didx in random_doc_idxs:
      print("Document {} ({}): {}...".format(didx, cats[didx], titles[didx][:400]))

tsne_docs = TSNE().fit_transform(doc_topic_props)

sns.scatterplot(x=tsne_docs[:,0], y=tsne_docs[:,1], hue=[str(l) for l in cluster_labels], alpha=0.4, s=10, linewidth=0, hue_order=(str(i) for i in range(n_clusters)))
sns.kdeplot(x=tsne_docs[:,0], y=tsne_docs[:,1], hue=[str(l) for l in cluster_labels], hue_order=(str(i) for i in range(n_clusters)))
plt.show()