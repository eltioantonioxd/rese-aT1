from flask import Flask, render_template, request,session,redirect, url_for
import requests
import mysql.connector
from waitress import serve



mydb = mysql.connector.connect(
  host="mysql",
  port=3306,
  user="user",
  password="password",
  database='tarea1'
)

mycursor = mydb.cursor()

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM users")
myresult = mycursor.fetchall()

for x in myresult:
  print(x[1])

app = Flask(__name__)

url = 'https://www.freetogame.com/api/games'
data = requests.get(url)
data = data.json()

app.secret_key = 'esto-es-una-clave-muy-secreta'

@app.route("/")
def index():
    return render_template("index.html", data=data, user = session['user'])
  
@app.route('/login',  methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    for i in myresult:
      if (i[1] == request.form['email'] or i[2] == request.form['email']) and i[3] == request.form['password'] :
        session['user']=request.form['email']
        session['password']=request.form['password']
        session['id']=i[0]
        return render_template("index.html", data=data, user=session['user'])

#Ingresar al sistema
@app.route('/logout',  methods=['GET', 'POST'])
def logout():
  session['user']=None
  session['password']=None
  session['id']=None
  return redirect(url_for('index'))

#Detalle del juego
@app.route('/<id>', methods=['GET'])
def infoGame(id):
  dataGame = specificGame(id)
  comment = tableResena(id)
  if session['user']!=None:
    return render_template("infoGame.html", dataGame = dataGame,comment=comment, session=session)
  else:
    return render_template("infoGame.html", dataGame = dataGame,comment=comment, session=session)

#Insertar comentario
@app.route('/<id>/comment', methods=['GET','POST'])
def resenaGame(id):
  resena = request.form['resena']
  sql = "INSERT INTO resenas (id_user,resena,id_juego) VALUES (%s, %s,%s)"
  val = (session['id'], resena, id)
  mycursor.execute(sql, val)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")
  return redirect(url_for('infoGame',id=id, session=session))

#Remover comentario
@app.route('/<id>/<remove>', methods=['GET','DELETE'])
def eliminar(id,remove):
  eliminar=uResena(remove)
  print(eliminar)
  if int(session['id'])==int(eliminar[1]):
    sql = "DELETE FROM resenas WHERE id = %s"
    val = (eliminar[0],)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
    return redirect(url_for('infoGame',id=id, session=session))
  error = '<p>Usted no es propietario de esta resena</p>'
  return redirect(url_for('infoGame',id=id, session=session))

#Registrar usuario
@app.route('/register', methods=['GET', 'POST'])
def registerUser():
  if request.method == 'POST':
    user = request.form['user']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']
    
    mycursor = mydb.cursor()
    sqlUser = 'SELECT * FROM users WHERE email = %s'      
    value = (email,)
    mycursor.execute(sqlUser, value)
    myresult = mycursor.fetchall()
    print(myresult)
    
    if myresult == [] and password == password2:
      mycursor = mydb.cursor()
      sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
      val = (user, email, password)
      mycursor.execute(sql, val)
      mydb.commit()
      
      mycursor = mydb.cursor()
      sqlUser = 'SELECT * FROM users WHERE email = %s'      
      value = (email,)
      mycursor.execute(sqlUser, value)
      myresult = mycursor.fetchall()
      session['user'] = email
      session['id'] = myresult[0][0]

      return render_template("index.html", data=data, session = session)
    else:
      return redirect(url_for('index'))

#Actualizar Reseña
@app.route('/<id>/update/<id_resena>', methods=['GET', 'POST', 'PUT'])
def updateresena(id,id_resena):
  resena = request.form['resena']
  update=uResena(id_resena)
  if update[1]!=None:
    if int(session['id'])==int(update[1]):
      sql = "UPDATE resenas SET resena=%s WHERE id=%s"
      val = (resena, id_resena)
      mycursor.execute(sql, val)
      mydb.commit()
      return redirect(url_for('infoGame',id=id, session=session))
  else:
    return redirect(url_for('infoGame',id=id, session=session))

#Métodos
def uResena(id):
  mycursor.execute("SELECT * FROM resenas")
  myresult = mycursor.fetchall()
  for i in myresult:
    if int(i[0])==int(id):
      return i

def tableUser(id_user):
  mycursor.execute("SELECT * FROM users")
  myresult = mycursor.fetchall()
  userEmail = []
  for i in myresult:
    if i[0] == int(id_user):
      userEmail = i[1]
      return userEmail
          
def tableResena(id):
  mycursor.execute("SELECT * FROM resenas")
  myresult = mycursor.fetchall()
  comment = []
  for i in myresult:
    if str(i[3]) ==(id):
      info = {'id_reseña': i[0], 'id_user': int(i[1]), 'resena': i[2], 'id_juego': i[3], 'userComment': tableUser(i[1])}
      comment.append(info)
  return comment

def specificGame(id):
  dataGame = {}
  for i in data:
    if str(i['id']) == (id):
      dataGame = i
  return dataGame
  


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    serve(app, host='0.0.0.0', port=5000)