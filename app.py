from audioop import cross
from random import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail
from flask_mail import Message
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from config import DevelopmentConfig
from datetime import datetime
import uuid ### libreria para generar id
import hashlib


app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)
mail = Mail(app)
mysql = MySQL(app)
@app.route('/')
def main():
    return "Hello Flask!"


@app.route('/holaMundo')
def holaMundo():
    print('hola mundo!')
    return 'hola mundo!'


@app.route('/getForms/<empresa>', methods=['GET'])
def getForms(empresa):
    cur = mysql.connection.cursor()
    cur.execute('SELECT Id_encuesta FROM Empresa_Encuesta WHERE Id_empresa = %s', (empresa,))
    data = cur.fetchall()
    encuestas = {}
    index = 1
    for i in data:
        cur.execute('SELECT * FROM Encuesta WHERE Id_encuesta = %s', (i[0],))
        consulta = cur.fetchall()
        fecha = consulta[0][3].split('-')
        encuesta = {'title': consulta[0][1], 'description': consulta[0][2], 'id': 'https://is2-client.herokuapp.com/#/form/'+consulta[0][0], 'date': {'year': fecha[0], 'month': fecha[1], 'day': fecha[2]}}
        encuestas["Encuesta "+str(index)] = encuesta
        index += 1
    print(len(data))
    print(len(encuestas))
    cur.close()
    return jsonify(encuestas)





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

@app.route("/newForm", methods=["POST"])
def newForm():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    Empresa = "UdeC"
    formId=uuid.uuid1().hex
    link="http://localhost:3000/form/"+formId
    cursor.execute('INSERT INTO `Empresa_Encuesta` VALUES(%s,%s)',(Empresa,formId))
    cursor.execute('INSERT INTO `Encuesta` VALUES(%s,%s,%s,%s)',(formId,str(data['title']),
        str(data['description']),str(datetime.today().strftime('%Y-%m-%d'))))
    npreguntas = cursor.execute('SELECT * FROM `Pregunta`')
    nalter = cursor.execute('SELECT * FROM `Alternativa`')
    for i in range(len(data['preguntas'])):
        cursor.execute('INSERT INTO `Encuesta_Pregunta` VALUES(%s,%s)',(formId,npreguntas))
        cursor.execute('INSERT INTO `Pregunta` VALUES(%s,%s,%s)',(npreguntas,str(data['preguntas'][i]['title']),
           i))
        for j in range(len(data['preguntas'][i]['alter'])):
            cursor.execute('INSERT INTO `Pregunta_Alternativa` VALUES(%s,%s)',(npreguntas,nalter))
            cursor.execute('INSERT INTO `Alternativa` VALUES(%s,%s,%s)',(nalter,str(data['preguntas'][i]['alter'][j]['title']),
                j))
            nalter += 1
        npreguntas += 1 
    mysql.connection.commit()
    cursor.close()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT Correo FROM `Empresa_Usuario` WHERE Id_empresa=%s',(Empresa,))
    correos = cursor.fetchall()
    listaCorreos = []
    for i in correos:
        cursor.execute('SELECT Participa FROM `Usuario` WHERE Correo=%s',(i[0],))
        participa = cursor.fetchall()[0][0]
        if participa == 1:
            listaCorreos.append(i[0])
    
    cursor.close()
    link="http://localhost:3000/#/form/"+formId
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

    cursor.execute("SELECT Id_empresa FROM 'UsuarioEmpresa'")
    empresa = []
    empresa = cursor.fetchall()
    if empresa.size() != 0:
        return jsonify("error")
    cursor.execute("INSERT INTO 'UsuarioEmpresa' VALUES(%s,%s)", str(data['ID']), str(data['Clave']))
    ## Deben asociarse todos los correos disponibles a esta empresa
    mysql.connection.commit()
    cursor.close()

    response = jsonify("Usuario agregado con exito")
    return response

@app.route("/newUser", methods = ["POST"])
def newUser():
    data = request.get_json()
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT Correo FROM 'Usuario'")
    usuarios = []
    usuarios = cursor.fetchall()
    if usuarios.size() != 0:
        return jsonify("error")
    cursor.execute("INSERT INTO 'Usuario' VALUES(%s,%s)", str(data['Correo']), "1")
    cursor.execute("SELECT Id_empresa FROM 'UsuarioEmpresa'")
    for i in cursor.fetchall():
        cursor.execute("INSERT INTO 'Empresa_Usuario' VALUES(%s,%s)", str(i), str(data['Correo']))
    
    mysql.connection.commit()
    cursor.close()

    response = jsonify("Usuario agregado con exito")
    return response


def sendMail(asunto,mensaje, destinatarios):
### Ciclo para enviar 1 a 1 los correos con el link personalizado para darse de baja. Para volver de hash a correo es HASH.hexdigest()
    for i in destinatarios:
        msg = Message(asunto, sender = app.config['MAIL_USERNAME'], recipients = i)
        msg.body = mensaje + "\n\nPara darte de baja del servicio de correos haz click aqui -> " + "HTTP://ACASESUPONEQUEVAELLINK/" + hashlib.md5(i)
        mail.send(msg) 
### Lo siguiente lo comente porque enviaba el correo masivo
#    msg = Message(asunto, sender = app.config['MAIL_USERNAME'], recipients = destinatarios)
#    msg.body = mensaje
#    mail.send(msg)

mail.init_app(app)
app.run(debug = True)
