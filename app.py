from audioop import cross
from random import random
from traceback import print_tb
from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from flask_mail import Message
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from numpy import empty
from config import DevelopmentConfig
from datetime import datetime
import uuid ### libreria para generar id
import hashlib
import re
import flask

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)
app.config["JSON_SORT_KEYS"] = True
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
mail = Mail(app)
mysql = MySQL(app)

@app.route('/hello')
def main():
    return session


@app.route('/holaMundo')
def holaMundo():
    print('hola mundo!')
    return 'hola mundo!'


@app.route('/getForms/<empresa>', methods=['GET'])
def getForms(empresa):
    cur = mysql.connection.cursor()
    idEmpresa = getId(empresa)
    cur.execute('SELECT Id_encuesta FROM Empresa_Encuesta WHERE Id_Empresa = %s', (idEmpresa,))
    data = cur.fetchall()
    encuestas = {}
    index = 1
    for i in data:
        cur.execute('SELECT * FROM Encuesta WHERE Id_encuesta = %s', (i[0],))
        consulta = cur.fetchall()
        fecha = consulta[0][3].split('-')
        encuesta = {'title': consulta[0][1], 'description': consulta[0][2], 'id': consulta[0][0], 'date': {'year': fecha[0], 'month': fecha[1], 'day': fecha[2]}}
        encuestas["Encuesta "+str(index)] = encuesta
        index += 1
    cur.close()
    data = jsonify(encuestas)
    return data


@app.route('/getInfo/<empresa>', methods= ["GET"])
def getInfo(empresa):
    img = getImg(empresa)
    idEmpresa = getId(empresa)
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM Empresa_Usuario WHERE Id_Empresa = %s', (idEmpresa,))
    nUsers = cur.fetchone()[0]
    message = {'img': img,
     'nUsers': nUsers}
    return jsonify(message)

def getImg(empresa):
    cur = mysql.connection.cursor()
    cur.execute("SELECT img FROM UsuarioEmpresa WHERE Username = %s", (empresa,))
    return cur.fetchone()[0]

def getId(empresa):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Id_Empresa FROM UsuarioEmpresa WHERE Username = %s", (empresa,))
    return cur.fetchone()[0]

def getEmpresa(correo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT Username FROM UsuarioEmpresa WHERE Correo = %s', (correo,))
    return cur.fetchone()

@app.route('/getForm/<formID>', methods = ["GET"])
def getForm(formID):
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT Nombre_encuesta FROM Encuesta WHERE Id_encuesta = %s', (formID,))  
    titulo = cursor.fetchone()
    
    cursor.execute('SELECT Descripcion FROM Encuesta WHERE Id_encuesta = %s', (formID,))
    descripcion = cursor.fetchone()

    preguntas = [{}]
    alternativas = [{}]
    preguntas.pop()
    alternativas.pop()
    cursor.execute('SELECT Id_pregunta FROM Encuesta_Pregunta WHERE Id_encuesta = %s', (formID,))
    preguntasID = cursor.fetchall()
    
    for i in preguntasID:
        cursor.execute('SELECT Enunciado FROM Pregunta WHERE Id_pregunta = %s', (i,))
        tit = cursor.fetchone()
        cursor.execute('SELECT Id_alternativa FROM Pregunta_Alternativa WHERE Id_pregunta = %s', (i,))
        alternativasID = cursor.fetchall()
        #print("\n\nSe seleccionaron los id: ")
        #print(alternativasID)
        for j in alternativasID:
            cursor.execute('SELECT Enunciado FROM Alternativa WHERE Id_alternativa = %s', (j,))
            alternativas.append({'title' : cursor.fetchone(), 'id' : j})
            #print("\nSe guardaron las alternativas de ID: ")
            #print(j)
        preguntas.append({'title' : tit, 'id' : i, 'alter' : alternativas.copy()})
        alternativas.clear()
    #print(preguntas)

    message = {
        'title' : titulo,
        'description' : descripcion,
        'preguntas' : preguntas
    }
    #print(message)
    return jsonify(message)


@app.route('/getFormAnswers/<empresa>/<formID>', methods = ["GET"])
def getFormAnswers(empresa,formID):
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT Id_Empresa FROM UsuarioEmpresa WHERE Username = %s", (empresa,))
    idEmpresa = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Empresa_Encuesta WHERE Id_encuesta = %s AND Id_empresa = %s", (formID, idEmpresa,))
    
    if cursor.fetchone() is None: 
        return ("No corresponde al usuario")
    
   

    cursor.execute('SELECT Nombre_encuesta FROM Encuesta WHERE Id_encuesta = %s', (formID,))  
    titulo = cursor.fetchone()
    
    cursor.execute('SELECT Descripcion FROM Encuesta WHERE Id_encuesta = %s', (formID,))
    descripcion = cursor.fetchone()

    preguntas = [{}]
    alternativas = [{}]
    preguntas.pop()
    alternativas.pop()
    cursor.execute('SELECT Id_pregunta FROM Encuesta_Pregunta WHERE Id_encuesta = %s', (formID,))
    preguntasID = cursor.fetchall()
    
    print()
    for i in preguntasID:
        cursor.execute('SELECT Enunciado FROM Pregunta WHERE Id_pregunta = %s', (i,))
        tit = cursor.fetchone()
        cursor.execute('SELECT Id_alternativa FROM Pregunta_Alternativa WHERE Id_pregunta = %s', (i,))
        alternativasID = cursor.fetchall()
   
        for j in alternativasID:
            cursor.execute('SELECT Enunciado FROM Alternativa WHERE Id_alternativa = %s', (j,))
            t = cursor.fetchone()
            cursor.execute("SELECT * FROM Alternativa_Respuesta WHERE Id_alternativa = %s", (j,))
            nAns = cursor.fetchall()
           
            alternativas.append({'title' : t, 'id' : j, 'answers' : len(nAns)})
            #print("\nSe guardaron las alternativas de ID: ")
            #print(j)
        preguntas.append({'title' : tit, 'id' : i, 'alter' : alternativas.copy()})
        alternativas.clear()
    #print(preguntas)

    message = {
        'title' : titulo,
        'description' : descripcion,
        'preguntas' : preguntas
    }
    #print(message)
    return jsonify(message)



@app.route("/newRespuesta", methods=["POST"])
def newRespuesta():
    data = request.get_json()
    print ("ok")
    print (data)
    x = 0
    for i in data:
        print ("alternativa "+ str(x) + ": " + str(i))
        x+=1
    response = jsonify("hola mundo!")

    
    cursor = mysql.connection.cursor()
    nAnswers= cursor.execute('SELECT * FROM `Respuesta`')
    formId=uuid.uuid1().hex

    cursor.execute('INSERT INTO `Respuesta` VALUES(%s)', (str(nAnswers)))
    for i in data:
        cursor.execute('INSERT INTO `Alternativa_Respuesta` VALUES (%s, %s)', (str(i[0]), str(nAnswers)) )

    mysql.connection.commit()
    cursor.close()
    return(response)

@app.route("/newForm/<empresa>", methods=["POST"])
def newForm(empresa):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    idEmpresa = getId(empresa)
    print(empresa+" "+str(idEmpresa))	
    formId=uuid.uuid1().hex

    link="http://localhost:3000/form/"+formId

    cursor.execute('INSERT INTO `Empresa_Encuesta` VALUES(%s,%s)',(idEmpresa,formId))
    cursor.execute('INSERT INTO `Encuesta` VALUES(%s,%s,%s,%s)',(formId,str(data['title']),
        str(data['description']),str(datetime.today().strftime('%Y-%m-%d'))))
    
    for i in range(len(data['preguntas'])):
        
        cursor.execute('INSERT INTO `Pregunta` (Enunciado,Numero_pregunta) VALUES(%s,%s)',(str(data['preguntas'][i]['title']),i))
        mysql.connection.commit()
        cursor.execute('SELECT LAST_INSERT_ID()')
        idPregunta = cursor.fetchone()[0]
        cursor.execute('INSERT INTO `Encuesta_Pregunta` VALUES(%s,%s)',(formId,idPregunta))
        mysql.connection.commit()
        for j in range(len(data['preguntas'][i]['alter'])):
            cursor.execute('INSERT INTO `Alternativa` (Enunciado,Letra) VALUES(%s,%s)',(str(data['preguntas'][i]['alter'][j]['title']),j))
            mysql.connection.commit()
            cursor.execute('SELECT LAST_INSERT_ID()')
            idAlter = cursor.fetchone()[0]
            cursor.execute('INSERT INTO `Pregunta_Alternativa` VALUES(%s,%s)',(idPregunta,idAlter))
            mysql.connection.commit()

    cursor.close()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT Correo FROM `Empresa_Usuario` WHERE Id_empresa=%s',(idEmpresa,))
    correos = cursor.fetchall()
    listaCorreos = []
    for i in correos:
        cursor.execute('SELECT Participa FROM `Usuario` WHERE Correo=%s',(i[0],))
        participa = cursor.fetchall()[0][0]
        if participa == 1:
            listaCorreos.append(i[0])
    
    cursor.close()
    link="http://localhost:3000/#/form/"+formId
    mensaje = "Participa en la siguiente encuesta!\n" + link
    ## Nuevo ciclo para los correos
    for i in listaCorreos:
       sendMail("Encuesta: "+str(data['title']), mensaje + "\n\nPara darte de baja del servicio de correos haz click aqui -> " + "http://localhost:5000/unsuscribe/" + hashlib.md5(i.encode('utf-8')).hexdigest(), [i])

    ##sendMail("Encuesta: "+str(data['title']),"Participa en la siguiente encuesta!\n"+link,listaCorreos)
    
    #sendMail('Respuestas encuesta',string,['dapiyih456@idurse.com'])
    ### GENERANDO LINK PARA ENCUESTA 
    print(formId)


    ### retorna el id del formulario para ocuparlo en react
    response = jsonify(formId)
    response.headers.add("Access-Control-Allow-Origin", "*") 
    return response

@app.route("/newEmpresa", methods = ["POST"])
def newEmpresa():
    data = request.get_json()
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM UsuarioEmpresa WHERE Id_Empresa='{}'".format(data['Correo']))
    empresa = cursor.fetchall()
    if len(empresa) != 0:
        return jsonify({'message':"Empresa ya registrada"})
    cursor.execute("INSERT INTO UsuarioEmpresa VALUES('{}','{}','{}')".format(data['Username'],data['Clave'],data['Correo']))
    mysql.connection.commit()
    cursor.close()

    response = jsonify({'message':"Usuario agregado con exito"})
    return response

@app.route("/newUser", methods = ["POST"])
def newUser():
    data = request.get_json()
    cursor = mysql.connection.cursor()

    if not validateMail(format(data['Correo'])):
        return jsonify({'message': "Ingrese un correo valido"})
    

    cursor.execute("SELECT * FROM Usuario WHERE Correo='{}'".format(data['Correo']))
    usuarios = cursor.fetchall()
    if len(usuarios) != 0:
        return jsonify({'message':"Correo ya registrado"})

    cursor.execute("INSERT INTO Usuario VALUES('{}','{}','{}')".format(data['Correo'],1,hashlib.md5(data['Correo'].encode('utf-8')).hexdigest()))
    cursor.execute("SELECT Id_empresa FROM UsuarioEmpresa")
    for i in cursor.fetchall():
        cursor.execute("INSERT INTO Empresa_Usuario VALUES('{}','{}')".format(i[0],data['Correo']))
    
    mysql.connection.commit()
    cursor.close()

    response = jsonify( {'message':"Usuario agregado con exito"})
    return response


def sendMail(asunto,mensaje, destinatarios):
    msg = Message(asunto, sender = app.config['MAIL_USERNAME'], recipients = destinatarios)
    msg.body = mensaje
    mail.send(msg)

def validateMail(correo):
    regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if not re.fullmatch(regex, correo):
        return False
    return True

@app.route("/unsuscribe/<md5>")
def unsuscribe(md5):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Usuario SET Participa = 0 WHERE md5_correo = '{}'".format(md5))
    mysql.connection.commit()
    cursor.close()
    return "correo dado de baja"

@app.route("/login",methods = ["POST"])
def login():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    username = data['correo']
    password = data['contraseña']
    respuesta = {}
    empresa = getEmpresa(username)
    respuesta['username'] = empresa
    cursor.execute('SELECT Contraseña FROM `UsuarioEmpresa` WHERE Correo = %s',(username,))
    consulta = cursor.fetchall()
    if (consulta == ()):
        respuesta['message'] = "Correo no registrado"
        return jsonify(respuesta)
    else:
        contraseña2 = hashlib.md5((consulta[0][0]).encode('utf-8')).hexdigest()
        if contraseña2 == password:
            respuesta['message'] = "Login exitoso"
            print(session)
            return jsonify(respuesta)
        else: 
            respuesta['message'] = "Contraseña incorrecta"
            return jsonify(respuesta)

mail.init_app(app)
app.run(host='localhost',debug = True)
