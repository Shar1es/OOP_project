
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Clase main para subir a db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    species = db.Column(db.String(50), nullable = False)
    height = db.Column(db.Float, nullable = True)
    diameter = db.Column(db.Float, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r' % self.id


#Crea la app. Necesario para correr la versión en pruebas
def create_app(config=None):
    
    app = Flask(__name__)
    
    # Configuración por defecto
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arboles.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Si se da una configuración distinta se sobreescribe (Permite el testeo)
    if config:
        app.config.update(config)
    

    db.init_app(app)
    with app.app_context():
        db.create_all()


    #Función de la página principal
    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == "POST":
            species = request.form.get('Especie')
            diameter = request.form.get('Diametro')
            height = request.form.get('Altura')
            new_task = Todo(species=species,
                            diameter=diameter,
                            height=height
                            )
            try: 
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except: 
                return "Por favor meta los valores apropiados en cada pestaña"

        else:
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('index.html', tasks = tasks)    

    ## Función que se corre al borrar un elemento de la tabla
    @app.route('/delete/<int:id>')
    def delete(id):
        task_to_delete = Todo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'Problema borrando'


    ## Función que se corre al pulsar update en un elemento de la tabla
    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update(id):

        task = Todo.query.get_or_404(id)


        if request.method == 'POST':
            species = request.form.get('Especie')
            diameter = request.form.get('Diametro')
            height = request.form.get('Altura')
            task.species = species
            task.diameter = diameter
            task.height = height                  
            try:
                db.session.commit()
                return redirect('/')
            except: 
                return 'Ups, problema actualizando'
        else:
            return render_template('update.html', task = task)
    return app


# Main code. Solo se corre cuando se corre directamente app.py 
# Crea la base de datos si no existe 
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=False)