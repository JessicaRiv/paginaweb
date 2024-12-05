# principal
from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Task
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

#Para listar tareas pendientes
@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks():
    tasks = Task.query.filter_by(completed=False).all()
    return jsonify([task.to_dict() for task in tasks])

#Para crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data.get('description'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

#Para marcar una tarea como completada
@app.route('/tasks/complete/<int:id>', methods=['PUT'])
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    task.completion_date = datetime.utcnow()
    db.session.commit()
    return jsonify(task.to_dict())

# Vista principal para mostrar tareas pendientes
@app.route('/')
def index():
    tasks = Task.query.filter_by(completed=False).all()
    return render_template('index.html', tasks=tasks)

# Vista para agregar una nueva tarea (usando formulario HTML)
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Marcar una tarea como completada desde el formulario HTML
@app.route('/complete_task/<int:id>', methods=['POST'])
def complete_task_form(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    task.completion_date = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
