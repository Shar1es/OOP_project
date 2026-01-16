from app import app, db

## Script que inicializa la base de datos.
## Debe correrse para crear el archivo test.db.

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Base de datos creada correctamente")