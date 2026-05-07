from flask import Flask, request, redirect, render_template
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'todo-db'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASS', 'password'),
        database=os.environ.get('DB_NAME', 'tododb')
    )

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255)
        )
    ''')

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    conn.close()

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO tasks (title) VALUES (%s)',
        (task,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'DELETE FROM tasks WHERE id=%s',
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
