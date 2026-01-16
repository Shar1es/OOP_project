from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)

## Señala a la base de datos en test.db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

## Le da nombre a la base de datos
db = SQLAlchemy(app)

## Clase que sirve para definir las columnas de las base de datos.
## Se utilizará para crear los objetos que se meten en base de datos.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    species = db.Column(db.String(50), nullable = False)
    height = db.Column(db.Float, nullable = True)
    diameter = db.Column(db.Float, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r' % self.id


## Función que añade las columnas a base de datos en la pantalla base
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
            return "Commit en el index() error"

    else:
        #print(Todo)
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



if __name__ == '__main__':

    app.run(debug = True)