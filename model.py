from settings import role_keywords

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('courses.csv')

df['title_clean'] = df['title'].str.lower().fillna('')
df['url'] = 'www.udemy.com' + df['url']

# Tfidf Model
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['title_clean'])

def get_recommendations(role, top_n=5):
    role = role.lower()

    if role not in role_keywords:
        return []

    keywords = role_keywords[role]
    query_vec = tfidf.transform([keywords])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarity.argsort()[-top_n:][::-1]

    top_courses = df.iloc[top_indices][['title', 'rating', 'num_reviews', 'url']]

    return top_courses.to_dict(orient='records')
