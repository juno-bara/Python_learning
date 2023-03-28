import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("tmdb.csv")
all_titles = [df['title'][i] for i in range(len(df['title']))]
class RECOMMEND():
    def __init__(self , vectorizer=TfidfVectorizer):
        self.vectorizer =vectorizer
        self.all_titles = all_titles

    def get_recommendation(self , title):
        count = self.vectorizer(stop_words='english')
        count_matrix = count.fit_transform(df['soup'])
        cos_sim = cosine_similarity(count_matrix ,count_matrix)

        indices = pd.Series(df.index, index=df['title'])
        idx = indices[title]

        sim_scores = list(enumerate(cos_sim[idx]))
        data = sorted(sim_scores , key=lambda x:x[1] , reverse=True)
        sim_indices = data[1:11]
        sim_sorted = [x[0] for x in sim_indices]
        title =df['title'].iloc[sim_sorted]
        release_date = list(df['release_date'].iloc[sim_sorted])
        homepage_url = df['homepage'].iloc[sim_sorted]
        movie_df = pd.DataFrame(columns=['title', 'release_date', 'homepage_url'])
        movie_df['title'] = title
        movie_df['release_date'] = release_date
        movie_df['homepage_url'] = homepage_url
        # print(movie_df['homepage_url'])

        return movie_df
        
# RECOMMEND().get_recommendation("Av atar")
# print(df['soup'][0])