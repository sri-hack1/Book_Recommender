# Importing neccessary modules
from flask import Flask, render_template, request
import pickle
import numpy as np

# Loading pkl files
popular_df = pickle.load(open("Book_recommender/templates/popular.pkl", "rb"))
pt = pickle.load(open("Book_recommender/templates/pt.pkl", "rb"))
books = pickle.load(open("Book_recommender/templates/books.pkl", "rb"))
similarity_scores = pickle.load(open("Book_recommender/templates/similarity_scores.pkl", "rb"))

# Creating instance
app = Flask(__name__)

# Routing Process
@app.route("/")
def index():
    return render_template("index.html",
                           book_name = list(popular_df["Book-Title"].values),
                           author = list(popular_df["Book-Author"].values),
                           images = list(popular_df["Image-URL-M"].values),
                           votes = list(popular_df["num_rating"].values),
                           ratings = list(popular_df["avg_rating"].values)
                           )

@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")

@app.route("/recommend_books", methods=["post"])
def recommend_books():
    user_input = request.form.get("user_input")
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        items = []
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        items.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        items.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        data.append(items)

    print(data)
    return render_template("recommend.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)