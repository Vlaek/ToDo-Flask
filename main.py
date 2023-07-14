from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime(), default=datetime.now)
    end_date = db.Column(db.DateTime(), default=datetime.min)

    def __repr__(self):
        return '<Task %r>' % self.id


with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "GET":
        q = request.args.get('q')

        if q:
            tasks = Task.query.filter(Task.title.contains(q) | Task.text.contains(q)).all()
        else:
            tasks = Task.query.order_by(Task.id.desc()).all()

        for task in tasks:
            task.start_date = task.start_date.strftime('%d.%m.%Y %H:%M')
            task.end_date = task.end_date.strftime('%d.%m.%Y %H:%M')

        return render_template("index.html", tasks=tasks)

    if request.method == "POST":
        if request.form['action'] == 'Добавить':
            title = request.form['title']
            text = request.form['text']
            start_date = request.form['startDate']
            end_date = request.form['endDate']

            start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

            task = Task(title=title, text=text, start_date=start_date, end_date=end_date)

            try:
                db.session.add(task)
                db.session.commit()

                return redirect('/')
            except:
                return "Ошибка"

        elif request.form['action'] == 'Изменить':
            id = request.form['id2']
            task = Task.query.get(id)
            task.title = request.form['title2']
            task.text = request.form['text2']
            task.start_date = request.form['startDate2']
            task.end_date = request.form['endDate2']

            task.start_date = datetime.strptime(task.start_date, '%Y-%m-%dT%H:%M')
            task.end_date = datetime.strptime(task.end_date, '%Y-%m-%dT%H:%M')

            try:
                db.session.commit()

                return redirect('/')
            except:
                return "Ошибка"

@app.route('/task/<int:task_id>', methods=['POST', 'GET'])
def task_detail(task_id):
    if request.method == "GET":
        task = Task.query.get(task_id)

        task.start_date = task.start_date.strftime('%d.%m.%Y %H:%M')
        task.end_date = task.end_date.strftime('%d.%m.%Y %H:%M')

        return render_template("task.html", task=task)

    if request.method == "POST":
        id = request.form['id']
        task = Task.query.get(id)
        task.title = request.form['title']
        task.text = request.form['text']
        task.start_date = request.form['startDate']
        task.end_date = request.form['endDate']

        task.start_date = datetime.strptime(task.start_date, '%Y-%m-%dT%H:%M')
        task.end_date = datetime.strptime(task.end_date, '%Y-%m-%dT%H:%M')

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"

@app.route('/task/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Ошибка"


if __name__ == '__main__':
    app.run(debug=True)