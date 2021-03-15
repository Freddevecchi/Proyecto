from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.lista'

db = SQLAlchemy( app)
ma = Marshmallow(app)

# SQLAlchemy
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.String(250))
    status = db.Column(db.String(70))
    tutor = db.Column(db.String(70))
  

    def __init__(self, title, description, status, tutor): 
        self.title = title
        self.description = description
        self.status = status
        self.tutor = tutor


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.String(250))
    

    def __init__(self, name, description): 
        self.name = name
        self.description= description
        

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(70))
    name = db.Column(db.String(70))
    email = db.Column(db.String(30))
    

    def __init__(self, name, first_name, email): 
        self.name = name
        self.first_name = first_name
        self.email= email

db.create_all()

# Marshmallow
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'status', 'tutor')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class StatusSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

status_schema = StatusSchema()
status_schema = StatusSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'first_name', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Route Flask
@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    status = request.json['status']
    tutor = request.json['tutor']

    new_task = Task(title, description, status, tutor)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

@app.route('/status', methods=['POST'])
def create_status():
    name = request.json['name']
    description = request.json['description']
    
    new_status = Status(name, description)

    db.session.add(new_status)
    db.session.commit()

    return status_schema.jsonify(new_status)

@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    first_name = request.json['firstname']
    email = request.json['email']
    
    new_user = User(name, first_name, email)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)



@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/status', methods=['GET'])
def get_status():
    all_status = Status.query.all()
    result = status_schema.dump(all_status)
    return jsonify(result)

@app.route('/status/<id>', methods=['GET'])
def get_statuss(id):
    status = Status.query.get(id)
    return status_schema.jsonify(status)

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)
    
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    task.title = request.json['titulo']
    task.description = request.json['descripcion']

    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/status/<id>', methods=['PUT'])
def update_status(id):
    status = Status.query.get(id)

    status.title = request.json['title']
    status.description = request.json['description']

    db.session.commit()

    return status_schema.jsonify(status)   

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    user.name = request.json['name']
    user.firsname = request.json['firstname']
    user.email = request.json['email']

    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'ok'})


if __name__ == "__main__":
    app.run(debug=True, port='3001')
