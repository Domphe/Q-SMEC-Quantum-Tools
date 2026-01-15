from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def tag_topics(entries, n_topics=5, n_top_words=5):
    abstracts = [entry["abstract"] for entry in entries]
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = vectorizer.fit_transform(abstracts)

    nmf = NMF(n_components=n_topics, random_state=1)
    W = nmf.fit_transform(tfidf)
    H = nmf.components_

    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(H):
        topics.append([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])

    for i, entry in enumerate(entries):
        entry["topics"] = [topics[j] for j in W[i].argsort()[-2:][::-1]]

    return entries
