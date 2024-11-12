import pandas as pd

def load_ratings(file_path):
    return pd.read_csv(file_path)

def load_movies(file_path):
    return pd.read_csv(file_path)

def load_links(file_path):
    return pd.read_csv(file_path)

def merge_data(ratings_df, links_df):
    return pd.merge(ratings_df, links_df, on='movieId')
