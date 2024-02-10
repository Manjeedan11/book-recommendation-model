# Book Recommendation System 

This repository contains code for a book recommendation system based on collaborative filtering. The system suggests books similar to a given book, leveraging information about authors and publishers.

## Contents

- [Introduction](#introduction)
- [Setup](#setup)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Dependencies](#dependencies)

## Introduction

The book recommendation system is built using Flask, a micro web framework for Python. It utilizes collaborative filtering techniques to recommend books that are similar to a given book. The recommendation process involves finding books by the same author as the input book.

## Setup

To set up the project locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/your_username/book-recommendation-system.git
```

2. Navigate to the project directory:

```
cd book-recommendation-system
```

3. Install the required dependencies. You can use the provided `requirements.txt` file to install the dependencies:

```
pip install -r requirements.txt
```

4. Ensure you have the necessary dataset files (`books.csv`, `users.csv`, `ratings.csv`) in a folder named `Datasets`. Update the file paths in the code if needed.

5. Run the Flask application:

```
python app.py
```

## Usage

Once the Flask application is running, you can interact with the recommendation system using HTTP requests. The system provides an endpoint for recommending books similar to a given book. You can send a POST request to the `/recommend` endpoint with the name of the book as the payload.

## Endpoints

The application exposes the following endpoint:

- `/recommend`: This endpoint accepts a POST request with the name of the book (`bookName`) as JSON data. It returns a JSON response containing recommended books similar to the input book.

Example usage:

```
POST /recommend
{
  "bookName": "Harry Potter and the Sorcerer's Stone"
}
```

Response:

```
{
  "books_by_author": [
    {
      "Book-Title": "Harry Potter and the Chamber of Secrets",
      "Image-URL-S": "http://example.com/image1.jpg"
    },
    {
      "Book-Title": "Harry Potter and the Prisoner of Azkaban",
      "Image-URL-S": "http://example.com/image2.jpg"
    },
    ...
  ]
}
```

## Dependencies

The project relies on the following dependencies:

- Flask: Micro web framework for Python.
- Flask-CORS: Extension for handling Cross-Origin Resource Sharing (CORS) in Flask applications.
- pandas: Library for data manipulation and analysis.
- scikit-learn: Machine learning library for Python.
- seaborn: Statistical data visualization library.
- matplotlib: Plotting library for Python.
- numpy: Library for numerical computing in Python.

These dependencies can be installed using `pip` as mentioned in the setup instructions.

