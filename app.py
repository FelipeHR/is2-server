from flask import Flask, request
from flask_cors import CORS
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
CORS(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'onefelixe@gmail.com'
app.config['MAIL_PASSWORD'] = 'dungmjgiiuyuwwot'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
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
    string += "     "+data['description']
    for i in data['preguntas']:
        string += '\n '+str(i['title'])
        for j in i['alter']:
            string +='     '+str(j['title'])
    print(str(app.config['MAIL_USERNAME']))
    sendMail(string, ['mmolina2018@udec.cl'])
    return data

def sendMail(mensaje, destinatarios):
    msg = Message('hola', sender = app.config['MAIL_USERNAME'], recipients = destinatarios)
    msg.body = mensaje
    mail.send(msg)

mail.init_app(app)
app.run(debug = True)
