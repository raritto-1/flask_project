from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo_database.db'
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        new_todo = Todo(title=title, desc=desc)
        db.session.add(new_todo)
        db.session.commit()
              
        return redirect('/')
    
    todo_all = Todo.query.all()
    return render_template('base.html', todos=todo_all)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    todo_to_delete = Todo.query.get_or_404(id)  
    db.session.delete(todo_to_delete) 
    db.session.commit()
    return redirect('/')  
if __name__ == "__main__":
    app.run(debug=True)
