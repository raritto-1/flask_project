from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # For CSRF token generation

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.ID}, - {self.title}'

with app.app_context():
    db.create_all()

# Route for the home page (listing all todos)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')

        if title:  # Ensure title is provided
            new_todo = Todo(title=title, desc=desc)
            db.session.add(new_todo)
            db.session.commit()
            flash('Todo added successfully!', 'success')

        return redirect(url_for('index'))

    todo_all = Todo.query.all()
    return render_template('base.html', todos=todo_all)

# Route to delete a todo item
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    todo_to_delete = Todo.query.get_or_404(id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Todo.query.get_or_404(id)

    if request.method == 'POST':
        item.title = request.form.get('title')
        item.desc = request.form.get('desc')

        try:
            db.session.commit()
            flash('Item updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating item: {e}', 'danger')

    return render_template('update_item.html', item=item)

if __name__ == "__main__":
    app.run(debug=True)
