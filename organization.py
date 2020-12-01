import flask
from flask import Flask, jsonify, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

database = psycopg2.connect(database='org', user='postgres', password=' ', host='127.0.0.1', port=5432)
database_cursor = database.cursor()


@app.route('/home_page')
def homepage():
    return render_template('Home_page.html')


@app.route('/home_page', methods=['POST'])
def authentication():
    data = request.form
    print(data)
    if data.get('login') and data.get('password'):
        database_cursor.execute(f"select* from Исполнитель where Пароль = '{data.get('password')}' "
                                f"and Логин = '{data.get('login')}'")
        for row in database_cursor:
            print(row)
            if row[0] is None:
                return render_template('Home_page.html')  # Ошибка аутентификации
            if row[1] == 0:
                database_cursor.execute(f"select* from Задание")
                for task in database_cursor:
                    print(task)  # Надо передать
                return render_template("Manager.html", name=str(row[3]).strip(), surname=str(row[2]).strip(),
                                       login=data.get('login'))
            # return redirect(url_for("manager", login=data.get('login')))  # Перенаправляет на метод
            if row[1] == 1:
                return redirect(url_for("worker", login=data.get('login')))
    return render_template('Home_page.html')


@app.route('/Manager', methods=['GET'])
def manager():
    data = request.args
    print(data)
    return render_template('Manager.html')


@app.route('/Worker')
def worker():
    return render_template('Worker.html')


@app.route('/CreateTask')
def create_task():
    return render_template('Task.html')


@app.route('/EditTask')
def edit_task():
    return render_template('EditTask.html')


@app.route('/Registration')
def registration():
    return render_template('Registration.html')


@app.route('/Registration', methods=['POST'])
def registration_post():
    data = request.form
    print(data)
    database_cursor.execute("select max(ID_Исполнителя) from Исполнитель")
    new_worker_id = 0
    for row in database_cursor:
        print(row[0])
        new_worker_id = 0 if row[0] is None else int(row[0]) + 1
    new_position_id = None
    if (data.get('position_manager') == 'on') and (data.get('position_worker') == 'on'):
        return flask.redirect("registration")
    if data.get('position_manager') == 'on':
        new_position_id = 0
    if data.get('position_worker') == 'on':
        new_position_id = 1
    database_cursor.execute(
        f"insert into Исполнитель values({new_worker_id}, {new_position_id}, '{data.get('surname')}',"
        f"'{data.get('name')}', '{data.get('lastname')}', '{data.get('login')}', '{data.get('password')}')")
    database.commit()
    return flask.redirect("home_page")  # redirect перенаправляет на другой метод


if __name__ == "__main__":
    app.run(debug=True)
