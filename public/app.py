from flask import Flask, render_template, request,session
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



  
app = Flask(__name__)

url = 'https://www.freetogame.com/api/games'
data = requests.get(url)
data = data.json()

app.secret_key = 'esto-es-una-clave-muy-secreta'

@app.route("/")
def index():
    return render_template("index.html", data=data)
  
@app.route('/login',  methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    #user = request.form['email']
    #password = request.form['password']
    
    #print(user, password)
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    for i in myresult:
      if (i[1] == request.form['email'] or i[2] == request.form['email']) and i[3] == request.form['password'] :
        session['user']=request.form['email']
        session['password']=request.form['password']
        session['id']=i[0]
        return render_template("index.html", data=data, user=session['user'])
      else:
          return '<h1> SSEXOOO </h1>'

@app.route('/<id>', methods=['GET'])
def infoGame(id):
  if session['user']!=None:
    dataGame = {}
    for i in data:
      if i['id'] == int(id):
        dataGame = i
    mycursor.execute("SELECT * FROM resenas")
    myresult = mycursor.fetchall()
    comment = []
    print(id)
    for i in myresult:
      if i[3]==int(id):
        comment.append(i)
        print('hola')
    print(comment)
    return render_template("infoGame.html", dataGame = dataGame,comment=comment,user=session['user'])

@app.route('/<id>/comment', methods=['GET','POST'])
def resenaGame(id):
  resena = request.form['resena']
  
  sql = "INSERT INTO resenas (id_user,resena,id_juego) VALUES (%s, %s,%s)"
  val = (session['id'], resena, id)
  mycursor.execute(sql, val)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")
  dataGame = {}
  for i in data:
    if i['id'] == int(id):
      dataGame = i
  mycursor.execute("SELECT * FROM resenas")
  myresult = mycursor.fetchall()
  comment = []
  for i in myresult:
    print('hola')
    if i[3]==int(id):
      comment.append(i)
  print(comment)
  return render_template("infoGame.html",dataGame = dataGame,comment=comment,user=session['user'])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)