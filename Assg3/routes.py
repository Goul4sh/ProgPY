from flask import render_template, request
from models import Seed

def register_routes(app, db):

    @app.route('/')
    def index():
        seeds = Seed.query.all()
        return render_template('index.html', seeds=seeds)

    @app.route('/add')
    def add():
        return render_template('add.html')

    @app.route('/delete/<int:id>')
    def delete(id):
        return render_template('delete.html', id=id)

    @app.route('/predict')
    def predict():
        return render_template('predict.html')