import pytest
from app import Todo, db, create_app
import os
import tempfile


###==============Codigo que testea la distintas funciones de la Herramienta==============###


@pytest.fixture(scope='function')
def app():
    """Create and configure a new app instance for each test."""
    # Crea la base de datos en memoria
    test_app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'connect_args': {'check_same_thread': False}
        }
    })
    
    yield test_app
    
    # Limpia la db creada en memoria
    with test_app.app_context():
        db.session.remove()
        db.drop_all()


#Crea un cliente test
@pytest.fixture
def client(app):
    
    return app.test_client()

#Corre el cliente test
@pytest.fixture
def runner(app):
    
    return app.test_cli_runner()


#Test del index get
def test_index_get(client):
    print("-----index get test-----")
    response = client.get('/')
    print("Code status: ")
    assert response.status_code == 200
    print("Response status: ")
    assert b"<html" in response.data  # Retorno de HTML

#Test del index post
def test_index_post(client, app):
    print("-----index post test-----")
    response = client.post('/', data = {'Especie': 'test', "Altura": 69, "Diametro": 69})
    print("Code status: ")
    assert response.status_code == 302
    print("Response status: ")
    assert b"<html" in response.data
    with app.app_context():
        registro = Todo.query.filter_by(species ='test').first()
        assert registro is not None
        assert registro.height == 69
        assert registro.diameter == 69
        db.session.close()

#Test delete 
def test_delete(client, app):

    print("-----delete test-----")
    response = client.post('/', data = {'Especie': 'test', "Altura": 69, "Diametro": 69})
    print("Code status: ")
    assert response.status_code == 302

    with app.app_context():
        # 2. Comprobar que existe
        registro = Todo.query.filter_by(species='test').first()
        assert registro is not None
        assert registro.height == 69
        assert registro.diameter == 69
        registro_id = registro.id

    print("Response status: ")
    assert b"<html" in response.data

    response = client.get(f'/delete/{registro_id}')
    assert response.status_code == 302

    with app.app_context():
        registro_borrado = Todo.query.filter_by(id=registro_id).first()
        assert registro_borrado is None
        db.session.close()


# Test de la función update
def test_update(client, app):
    print("-----update test-----")

    # 1. Crear el registro inicial
    client.post(
        '/',
        data={'Especie': 'test', 'Altura': 69, 'Diametro': 69}
    )

    with app.app_context():
        task = Todo.query.filter_by(species='test').first()
        assert task is not None
        task_id = task.id
        assert task.height == 69
        assert task.diameter == 69

    # 2. Actualizar el registro
    response = client.post(
        f'/update/{task_id}',
        data={'Especie': 'updated', 'Altura': 100, 'Diametro': 200}
    )

    # 3. Comprobar redirección
    assert response.status_code == 302

    # 4. Comprobar que los datos se actualizaron
    with app.app_context():
        updated_task = Todo.query.get(task_id)
        assert updated_task is not None
        assert updated_task.species == 'updated'
        assert updated_task.height == 100
        assert updated_task.diameter == 200

        db.session.close()

