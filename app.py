from flask import Flask, request
from flask_cors import CORS
from flask_mail import Mail
from flask_mail import Message
from config import DevelopmentConfig
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
mail = Mail(app)
@app.route('/')
def main():
    print('Este es el mensaje al cargar el home')
    return "Hello Flask!"


@app.route('/holaMundo')
def holaMundo():
    print('hola mundo!')
    return 'hola mundo!'


@app.route("/newForm", methods=["POST"])
def newForm():
    data = request.get_json()
    string = data['title']
    string += "\n"+data['description']
    for i in data['preguntas']:
        string += '\n '+str(i['title'])
        for j in i['alter']:
            string +='\n     <br>'+str(j['title'])
    sendMail('Respuestas encuesta',string,['dapiyih456@idurse.com'])
    print(string)
    return data

def sendMail(asunto,mensaje, destinatarios):
    msg = Message(asunto, sender = app.config['MAIL_USERNAME'], recipients = destinatarios)
    msg.body = mensaje
    mail.send(msg)

mail.init_app(app)
app.run(debug = True)
