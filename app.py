import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

#Cargar las variables de entorno 
load_dotenv()


# Crear instancia
app = Flask(__name__)   

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)    
  


#modelo de la base de datos

class Evento(db.Model):
    __tablename__ = 'eventos'
    no_evento = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    detalle_evento = db.Column(db.Integer)
     
    def to_dict(self):
        return{
            'no_evento': self.no_evento,
            'nombre': self.nombre,
            'ap_paterno':self.ap_paterno, 
            'ap_materno': self.ap_materno,
            'detalle_evento': self.detalle_evento,
         }

# Ruta raiz/ 
@app.route('/')
def index():
    #trae todos los alumnos
    eventos = Evento.query.all()
    return render_template('index.html', eventos = eventos)

# Ruta /eventos
@app.route('/eventos')
def getClientes():
    return 'Aqui van los clientes'

with app.app_context():
    db.create_all()

#Ruta /crear un nuevo cliente
@app.route('/eventos/new', methods=['GET', 'POST'])
def create_cliente():
    if request.method == 'POST':
        #Agregar Cliente
        no_evento = request.form ['no_evento']
        nombre = request.form ['nombre']
        ap_paterno = request.form ['ap_paterno']
        ap_materno = request.form ['ap_materno']
        detalle_evento = request.form ['detalle_evento']
        
        nvo_evento = Evento(no_evento=no_evento, nombre=nombre,ap_paterno=ap_paterno, ap_materno=ap_materno, detalle_evento=detalle_evento)
        db.session.add(nvo_evento)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    #Aqui sigue si es GET
    return render_template('create_cliente.html')    
    
    #Eliminar cliente
@app.route('/eventos/delete/<string:no_evento>')
def delete_cliente(no_evento):
    evento = Evento.query.get(no_evento)
    if evento:
        db.session.delete(evento)  
        db.session.commit()
    return redirect(url_for('index'))



#Actualizar cliente
@app.route('/eventos/update/<string:no_evento>', methods=['GET', 'POST'])
def update_cliente(no_evento):
    eventos = Evento.query.get(no_evento)
    
    if request.method == 'POST':
        eventos.nombre = request.form ['nombre']
        eventos.ap_paterno = request.form ['ap_paterno']
        eventos.ap_materno = request.form ['ap_materno']
        eventos.detalle_evento = request.form ['detalle_evento'] 
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_cliente.html', evento = eventos)

if __name__ == '__main__':
    app.run(debug=True)