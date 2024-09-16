from flask import Flask, render_template, request
from utils.utils import transcript, summarize, web
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/summary", methods=["GET", "POST"])
def summary():
    url = request.form.get('url')
    if "you" in url:
        content = transcript(url)
    else:
        content = web(url)
    summary = summarize(content)
    print(summary)
    return render_template("summary.html", summary=summary)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
