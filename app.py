from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import Task

app = Flask(__name__)

@app.route('/')
def index():
    tasks = Task.get_all()
    categories = Task.get_all_categories()
    return render_template('index.html', tasks=tasks, categories=categories)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip() or 'General'
    if title:
        task = Task(title=title, category=category)
        task.save()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.get_by_id(task_id)
    if task:
        task.completed = not task.completed
        task.save()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    task = Task.get_by_id(task_id)
    if task:
        new_title = request.form.get('title', '').strip()
        new_category = request.form.get('category', '').strip()
        if new_title:
            task.title = new_title
        if new_category:
            task.category = new_category
        task.save()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.get_by_id(task_id)
    if task:
        task.delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    Task.init_db()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)