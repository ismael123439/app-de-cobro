from flask import Flask, request, jsonify, render_template

from flask_sqlalchemy import SQLAlchemy
import pymysql
import mercadopago

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u8hhqvrap0mtdbtl:kmdYEIy3t9FRuIXWOZ8M@bympkas0qk7r7auydfha-mysql.services.clever-cloud.com:3306/bympkas0qk7r7auydfha'
sdk = mercadopago.SDK("TEST-1343000075296803-090509-78660005179ebd257a490107fb4513bd-1276110477")  

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

@app.route('/pagar')
def pagar():
    return render_template('pagar.html')



@app.route('/crear_pago', methods=['POST'])
def crear_pago():
    body = {
        "transaction_amount": 100,  
        "token": request.json.get("token"),  
        "description": "Compra de prueba",
        "installments": 1,  
        "payment_method_id": request.json.get("Mastercard"),  
        "payer": {
            "email": request.json.get("email")  
        }
    }
    
    payment_response = sdk.payment().create(body)
    payment = payment_response["response"]


    return jsonify(payment), payment_response["status"]

@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        # Intenta hacer una consulta simple
        db.session.execute('SELECT 1')
        return "La base de datos se conectó correctamente", 200
    except Exception as e:
        return f"No se pudo conectar a la base de datos: {e}", 500
    
    
@app.route('/ver_usuarios', methods=['GET'])
def ver_usuarios_console():
    try:
        usuarios = Usuario.query.all()
        for usuario in usuarios:
            print(f"ID: {usuario.id}, Nombre: {usuario.nombre}")
        return "Datos mostrados en la consola", 200
    except Exception as e:
        return f"No se pudo recuperar los datos: {e}", 500



if __name__ == '__main__':
    app.run(debug=True)
