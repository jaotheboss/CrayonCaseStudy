from flask import Flask, request

app = Flask(__name__)

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

    # perhaps extract data from Feature Store
    # execute rules-based algorithm to recommend movies according to Features (e.g demographics)

    return {
        "status": 200,
        "response": {
            "Ranking": [1, 2, 3, 4, 5],
            "Movies": ["Avengers: Endgame", "Avengers: Infinity War", "Captain America: The Winter Soldier", "Iron Man", "Thor: Ragnarok"],
        }
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)