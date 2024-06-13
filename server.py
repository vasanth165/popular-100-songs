import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")

@app.route("/songs",methods=["POST"])
def show_songs():
    date = request.form['date']
    url = f"https://www.billboard.com/charts/hot-100/{date}/"

    response = requests.get(url=url)
    content = response.text

    soup = BeautifulSoup(content, "html.parser") 
    all_title = soup.find_all(name="ul", class_="lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-direction-column@mobile-max")

    title = [i.find(name="h3").get_text().strip() for i in all_title]

    if len(title) == 100:
        return render_template("songs.html", title=title, date=date)
    else:
        return render_template("error_page.html", date=date)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
