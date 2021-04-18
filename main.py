import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass228@localhost/Task'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=True)
    first_date = db.Column(db.DateTime(), default=datetime.now)
    second_date = db.Column(db.DateTime(), default=datetime.min)

    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all()

@app.route('/')
def index():
    q = request.args.get('q')

    if q:
        tasks = Task.query.filter(Task.title.contains(q) | Task.text.contains(q)).all()
    else:
        tasks = Task.query.all()

    for i in tasks:
        i.first_date = i.first_date.strftime('%d.%m.%Y %H:%M')
        i.second_date = i.second_date.strftime('%d.%m.%Y %H:%M')

    return render_template("index.html", tasks=tasks)


@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get(task_id)

    task.first_date = task.first_date.strftime('%d.%m.%Y %H:%M')
    task.second_date = task.second_date.strftime('%d.%m.%Y %H:%M')

    file_array = []

    for root, dirs, files in os.walk("uploads/" + str(task.id)):
        for filename in files:
            file_array.append(filename)

    return render_template("task.html", task=task, file_array=file_array)


@app.route('/task/edit/<int:task_id>/file/delete/<string:file_name>')
def edit_file_delete(task_id, file_name):
    directory_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "uploads/" + str(task_id))

    os.remove(directory_folder + "/" + file_name)

    return redirect(url_for('edit_task', task_id=task_id))


@app.route('/task/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    directory_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "uploads/" + str(task.id))

    if os.path.exists(directory_folder):
        for root, dirs, files in os.walk("uploads/" + str(task.id)):
            for filename in files:
                os.remove(directory_folder + "/" + filename)
        os.rmdir(directory_folder)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Ошибка"


@app.route('/task/edit/<int:task_id>', methods=['POST', 'GET'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if request.method == "POST":

        if request.form['action'] == 'Изменить':
            task.title = request.form['title']
            task.text = request.form['text']
            task.first_date = request.form['firstDate']
            task.second_date = request.form['secondDate']

            task.first_date = datetime.strptime(task.first_date, '%Y-%m-%dT%H:%M')
            task.second_date = datetime.strptime(task.second_date, '%Y-%m-%dT%H:%M')

            file = request.files['file']

            if file:
                directory = "uploads/" + str(task_id)
                if not os.path.exists(directory):
                    os.mkdir(directory)
                file.save(os.path.join(directory, file.filename))

            try:
                db.session.commit()
                return redirect('/')
            except:
                return "Ошибка"

        elif request.form['action'] == 'Загрузить файл':
            file = request.files['file']

            if file:
                directory = "uploads/" + str(task_id)
                if not os.path.exists(directory):
                    os.mkdir(directory)
                file.save(os.path.join(directory, file.filename))

            return redirect('/task/edit/' + str(task.id))
    else:
        task.first_date = task.first_date.strftime('%Y-%m-%dT%H:%M')
        task.second_date = task.second_date.strftime('%Y-%m-%dT%H:%M')

        file_array = []

        for root, dirs, files in os.walk("uploads/" + str(task.id)):
            for filename in files:
                file_array.append(filename)

        min_date = datetime.now().strftime('%Y-%m-%dT%H:%M')

        return render_template("edit.html", task=task, file_array=file_array, min_date=min_date)


@app.route('/add', methods=['POST', 'GET'])
def add_task():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        first_date = request.form['firstDate']
        second_date = request.form['secondDate']

        task = Task(title=title, text=text, first_date=datetime.strptime(first_date, '%Y-%m-%dT%H:%M'),
                    second_date=datetime.strptime(second_date, '%Y-%m-%dT%H:%M'))

        try:
            db.session.add(task)
            db.session.commit()

            return redirect('/')
        except:
            return "Ошибка"

    else:
        min_date = datetime.now().strftime('%Y-%m-%dT%H:%M')

        return render_template("add.html", min_date=min_date)


if __name__ == '__main__':
    app.run()
