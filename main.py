import re
import pickle
import operator
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from scipy.sparse import csr_matrix
from pandas.api.types import is_numeric_dtype
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, jsonify
from flask_cors import CORS

import warnings
warnings.filterwarnings("ignore")

# Loading datasets
books = pd.read_csv(r"Datasets/books.csv", delimiter=';', encoding='ISO-8859-1')
users = pd.read_csv(r"Datasets/users.csv", delimiter=';', encoding='ISO-8859-1')
ratings = pd.read_csv(r"Datasets/ratings.csv", delimiter=';', encoding='ISO-8859-1')

# Dropping unnecessary columns from books dataset
books.drop(['Image-URL-M', 'Image-URL-L'], axis=1, inplace=True)

# Data cleaning and handling invalid entries in books dataset
# Handle missing values in 'Book-Author' and 'Publisher'
books['Book-Author'].fillna('Other', inplace=True)
books['Publisher'].fillna('Other', inplace=True)

# Handling invalid entries in 'Year-Of-Publication' column
# Convert 'Year-Of-Publication' to integers and handle invalid years
books['Year-Of-Publication'] = pd.to_numeric(books['Year-Of-Publication'], errors='coerce')
books['Year-Of-Publication'].fillna(2002, inplace=True)
books['Year-Of-Publication'] = books['Year-Of-Publication'].astype(int)

# Data cleaning and handling invalid entries in users dataset
# Handling outliers and missing values in 'Age' column
users['Age'] = users['Age'].apply(lambda x: 80 if x > 80 else (10 if x < 10 else x))
users['Age'].fillna(round(users['Age'].mean()), inplace=True)
users['Age'] = users['Age'].astype(int)

# Handle missing values in 'Location' column
users['Location'].fillna('', inplace=True)

# Extracting city, state, and country from 'Location' column in users dataset
split_location = users['Location'].str.split(', ', expand=True)
# Ensure that split_location has three columns
if len(split_location.columns) == 3:
    users[['City', 'State', 'Country']] = split_location
else:
    # If split_location doesn't have three columns, assign default values
    users['City'] = ''
    users['State'] = ''
    users['Country'] = ''

# Drop the 'Location' column
users.drop('Location', axis=1, inplace=True)

# Drop duplicate rows in users dataset
users.drop_duplicates(keep='last', inplace=True)

# Data cleaning and handling invalid entries in ratings dataset
# Convert ISBN to uppercase and remove extra characters
ratings['ISBN'] = ratings['ISBN'].str.upper()
ratings['ISBN'] = ratings['ISBN'].str.replace("[^A-Za-z0-9]", "")

# Drop duplicate rows in ratings dataset
ratings.drop_duplicates(keep='last', inplace=True)

# Merging datasets
dataset = pd.merge(books, ratings, on='ISBN', how='inner')
dataset = pd.merge(dataset, users, on='User-ID', how='inner')

# Define explicit ratings dataset (ratings != 0)
dataset1 = dataset[dataset['Book-Rating'] != 0].reset_index(drop=True)

# Define implicit ratings dataset (ratings == 0)
dataset2 = dataset[dataset['Book-Rating'] == 0].reset_index(drop=True)

# Define functions for recommending books based on collaborative filtering

def printBooks(df, n):
    """Prints top n books from the given DataFrame."""
    for title in df['Book-Title'].unique()[:n]:
        print(title)

def get_books(dataframe, book_name):
    """Recommends books similar to the given book_name."""
    author = dataframe['Book-Author'].iloc[0]
    #publisher = dataframe['Publisher'].iloc[0]

    similar_author_books = dataset1[dataset1['Book-Author'] == author].sort_values(by='Book-Rating', ascending=False)
    print("Books by the same author:")
    printBooks(similar_author_books, 5)

    """"similar_publisher_books = dataset1[dataset1['Publisher'] == publisher].sort_values(by='Book-Rating', ascending=False)
    print("\nBooks by the same publisher:")
    printBooks(similar_publisher_books, 5)"""""

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend_books():
    # Get the book name from the POST request data
    book_name = request.json.get('bookName')

    if book_name is None:
        return jsonify({'error': 'Book name is missing'}),

    # Check if the book name is valid
    if book_name not in dataset1['Book-Title'].unique():
        return jsonify({'error': 'Invalid Book Name'}),

    # Find the book data
    book_data = dataset1[dataset1['Book-Title'] == book_name]

    # Get similar books by the same author
    author = book_data['Book-Author'].iloc[0]
    similar_author_books = dataset1[dataset1['Book-Author'] == author].sort_values(by='Book-Rating', ascending=False)

    # Get similar books by the same publisher
    """"publisher = book_data['Publisher'].iloc[0]
    similar_publisher_books = dataset1[dataset1['Publisher'] == publisher].sort_values(by='Book-Rating', ascending=False)"""""

    # Extract relevant information for each book
    if 'Image-URL-S' in similar_author_books.columns:
        books_by_author = similar_author_books[['Book-Title', 'Image-URL-S']].head(5).to_dict(orient='records')
    else:
        books_by_author = similar_author_books[['Book-Title']].head(5).to_dict(orient='records')

    """"if 'Image-URL-S' in similar_publisher_books.columns:
        books_by_publisher = similar_publisher_books[['Book-Title', 'Image-URL-S']].head(5).to_dict(orient='records')
    else:
        books_by_publisher = similar_publisher_books[['Book-Title']].head(5).to_dict(orient='records')"""""

    # Modify the response to include image URLs
    response = {
        'books_by_author': books_by_author,
        #'books_by_publisher': books_by_publisher
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Change the port number if needed
