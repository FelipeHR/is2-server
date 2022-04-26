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


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
mail = Mail(app)
mysql = MySQL(app)
@app.route('/')
def main():
    cursor = mysql.connection.cursor()
    dato = "UdeC"
    cursor.execute('SELECT Correo FROM `Empresa_Usuario` WHERE Id_empresa=%s',(dato,))
    correos = cursor.fetchall()
    listaCorreos = []
    for i in correos:
        cursor.execute('SELECT Participa FROM `Usuario` WHERE Correo=%s',(i[0],))
        participa = cursor.fetchall()[0][0]
        if participa == 1:
            listaCorreos.append(i[0])
    sendMail('prueba',"holi, es una prueba",listaCorreos)
    print(listaCorreos)
    return "Hello Flask!"


@app.route('/holaMundo')
def holaMundo():
    print('hola mundo!')
    return 'hola mundo!'


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
    link="http://localhost:3000/form/"+formId
    sendMail("Encuesta: "+str(data['title']),"Participa en la siguiente encuesta!\n"+link,listaCorreos)
    
    #sendMail('Respuestas encuesta',string,['dapiyih456@idurse.com'])
    ### GENERANDO LINK PARA ENCUESTA 
    print(formId)


    ### retorna el id del formulario para ocuparlo en react
    return jsonify(formId)

def sendMail(asunto,mensaje, destinatarios):
    msg = Message(asunto, sender = app.config['MAIL_USERNAME'], recipients = destinatarios)
    msg.body = mensaje
    mail.send(msg)

mail.init_app(app)
app.run(debug = True)
