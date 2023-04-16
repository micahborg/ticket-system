from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from src.account import Account

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class EventClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    ticket_price = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_date = request.form['date']
        task_description = request.form['description']
        task_ticket_price = request.form['price']

        new_task = EventClass(content=task_content, date_created=task_date, description=task_description, ticket_price=task_ticket_price)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = EventClass.query.order_by(EventClass.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = EventClass.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/purchase/<int:id>', methods=['GET', 'POST'])
def purchase(id):
    task = EventClass.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('purchase.html', task=task)


@app.route('/choice/', methods=['GET', 'POST'])
def choice():
    
    return render_template('choice.html')


@app.route('/seed/', methods=['GET', 'POST'])
def seed():

    if request.method == 'POST':
        seed = request.form['seed']

        seller_account = Account(seed)

        try:
            return redirect(url_for('/create/', seller_account=seller_account))
        except:
            return 'Here There was an issue adding your task'

    else:
        return render_template('seed.html')
    
    

@app.route('/create/', methods=['GET', 'POST'])
def create():

    seller_account = request.args['seller_account']
    public_key = seller_account.address
    private_key = seller_account.private_key
    balance = seller_account.get_balance()

    
    if request.method == 'POST':

        task_content = request.form['content']
        task_date = request.form['date']
        task_description = request.form['description']
        task_ticket_price = request.form['price']

        new_task = EventClass(content=task_content, date_created=task_date, description=task_description, ticket_price=task_ticket_price)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Here There was an issue adding your task'

    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
