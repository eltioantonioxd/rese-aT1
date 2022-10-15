from flask import Flask, render_template
import requests
import mysql.connector

mydb = mysql.connector.connect(
  host="mysql",
  port=3306,
  user="user",
  password="password"
)
print(mydb)

app = Flask(__name__)

url = 'https://www.freetogame.com/api/games'
data = requests.get(url)
data = data.json()

@app.route("/")
def index():
    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)