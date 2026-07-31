from flask import Flask

from catalog import render_catalog

app = Flask(__name__)


@app.route("/")
def catalog():
    return render_catalog()


if __name__ == "__main__":
    app.run(debug=True)