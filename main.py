# from surprise import SVD
# from surprise import Dataset
# from surprise.model_selection import cross_validate

# # Load the movielens-100k dataset (download it if needed).
# data = Dataset.load_builtin('ml-100k', False)

# # Use the famous SVD algorithm.
# algo = SVD()

# # Run 5-fold cross-validation and print results.
# cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# uid = str(196)  # raw user id (as in the ratings file). They are **strings**!
# iid = str(302)  # raw item id (as in the ratings file). They are **strings**!

# # get a prediction for specific users and items.
# pred = algo.predict(uid, iid, r_ui=4, verbose=True)

# from surprise import dump

# dump.dump("algo_file", algo=algo)
# _, loaded_algo = dump.load("algo_file")

from flask import Flask, request
from surprise import dump
import pandas as pd

app = Flask(__name__)
_, model = dump.load("data/model_file")
data = pd.read_csv("data/movie_dataset.csv")
eligible_users = [str(i) for i in data.name.unique()]

def get_top_10(user: str) -> list:
    print(user)
    rankings = data.iloc[data.loc[data.name != int(user)].movie_id.drop_duplicates().apply(lambda id: model.predict(user, str(id))[3]).sort_values(ascending=False)[:10].index]
    print(rankings)
    return rankings.movie_name.to_list()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/healthcheck")
def health_check():
    return {
        "status": 200,
        "response": "healthy"
    }

@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return {
            "status": 418,
            "response": "Content-Type not supported!"
        }
    
    json = request.json
    if "user" not in json:
        return {
            "status": 400,
            "response": "payload requires key value: 'user'"
        }

    if json["user"] not in eligible_users:
        return {
            "status": 200,
            "response": {
                "Ranking": [1, 2, 3, 4, 5],
                "Movies": ["Avengers: Endgame", "Avengers: Infinity War", "Captain America: The Winter Soldier", "Iron Man", "Thor: Ragnarok"],
            }
        }
    else:
        return {
            "status": 200,
            "response": {
                "Ranking": [i for i in range(1, 11)],
                "Movies": get_top_10(json["user"])
            }
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)