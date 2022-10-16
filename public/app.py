from flask import Flask, render_template, request
import requests
import mysql.connector


mydb = mysql.connector.connect(
  host="mysql",
  port=3306,
  user="user",
  password="password",
  database='tarea1'
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM users")
myresult = mycursor.fetchall()

for x in myresult:
  print(x[1])
  
app = Flask(__name__)

url = 'https://www.freetogame.com/api/games'
data = requests.get(url)
data = data.json()



@app.route("/")
def index():
    return render_template("index.html", data=data)
  
@app.route('/login',  methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    user = request.form['email']
    password = request.form['password']
    print(user, password)
    for i in myresult:
      if (i[1] == user or i[2] == user) and i[3] == password :
        return render_template("index.html", data=data, user=user)
      else:
          return '<h1> SSEXOOO </h1>'

@app.route('/<id>', methods=['GET'])
def infoGame(id):
  dataGame = {}
  for i in data:
    if i['id'] == int(id):
      dataGame = i
  return render_template("infoGame.html", dataGame = dataGame)


def resenaGame(id_user, resena, id_juego):
  resena = request.form['resena']
  mycursor = mydb.cursor()
  sql = "INSERT INTO customers (id_user,resena,id_juego) VALUES (%d, %s,%d)"
  val = (id_user, resena, id_juego)
  mycursor.execute(sql, val)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)