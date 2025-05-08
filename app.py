from flask import Flask, jsonify, render_template
from sample_visualisation import get_data

app = Flask(__name__)

@app.route("/")
def index():
    chart = get_data()
    return render_template("index.html", chart=chart)

if __name__ == "__main__":
    app.run(debug=True)
