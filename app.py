from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

#se crea la app
app = Flask(__name__)

#ruta de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///databases/tasks.db'

#Instanciamos el cursor de la base de datos en db
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)



@app.route("/")
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@app.route("/add-task", methods=["POST"])
def add_task():
    print("adding task")
    print(request.form)

    task = Task(content=request.form["task-content"], done=False)
    #guardamos la tarea en la base de datos (PRIMERO SE DEBE CREAR LA TABLA MANUALMENTE O ARROJA ERROR)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete/<id>")
def delete_by_id(id):
    Task.query.filter_by(id=int(id)).delete()    
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/change/<id>")
def change_state(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session().commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    #probamos que sucede si se crea todo el tiempo que se corra la app si se pierden los datos o que
    db.create_all()
    app.run(debug=True, port=4000)
    