from os import abort

import flask
from flask import render_template, request, redirect, url_for, jsonify
from models import Seed


def register_routes(app, db):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        seeds = Seed.query.all()
        return render_template('index.html', seeds=seeds)

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'GET':
            return render_template('add.html')
        if request.method == 'POST':
            try:
                area = float(request.form['area'])
                if area < 0:
                    raise ValueError("Area cannot be negative")
                perimeter = float(request.form['perimeter'])
                if perimeter < 0:
                    raise ValueError("Perimeter cannot be negative")
                compactness = float(request.form['compactness'])
                if compactness < 0:
                    raise ValueError("Compactness cannot be negative")
                kernel_length = float(request.form['kernel_length'])
                if kernel_length < 0:
                    raise ValueError("Kernel length cannot be negative")
                kernel_width = float(request.form['kernel_width'])
                if kernel_width < 0:
                    raise ValueError("Kernel width cannot be negative")
                asymmetry_coefficient = float(request.form['asymmetry_coefficient'])
                kernel_groove_length = float(request.form['kernel_groove_length'])
                if kernel_groove_length < 0:
                    raise ValueError("Kernel groove length cannot be negative")
                seed_class = int(request.form['seed_class'])
                if seed_class < 0 or seed_class > 3:
                    raise ValueError("Seed class is incorrect")

            except (ValueError, KeyError):
                flask.abort(400)

            max_id = db.session.query(db.func.max(Seed.seed_id)).scalar()

            if max_id is None:
                max_id = 1
            else:
                max_id = max_id + 1

            new_seed = Seed(seed_id=max_id, area=area, perimeter=perimeter, compactness=compactness,
                            kernel_length=kernel_length,
                            kernel_width=kernel_width, asymmetry_coefficient=asymmetry_coefficient,
                            kernel_groove_length=kernel_groove_length, seed_class=seed_class)

            db.session.add(new_seed)
            db.session.commit()
            return redirect(url_for('index')), 200


        else:
            return render_template('add.html')

    @app.route('/delete/<int:id>', methods=['POST'])
    def delete(id):

        seed = Seed.query.get(id)

        if seed is None:
            flask.abort(404)

        else:
            db.session.delete(seed)
            db.session.commit()
            return redirect(url_for('index')), 200

    @app.route('/predict')
    def predict():
        return render_template('predict.html')

    @app.route('/api/data', methods=['GET', 'POST'])
    def api_data():
        if request.method == 'GET':
            seeds = Seed.query.all()
            return jsonify([seed.to_dict() for seed in seeds])
        elif request.method == 'POST':

            data = request.get_json()

            required_fields = ['area', 'perimeter', 'compactness', 'kernel_length',
                               'kernel_width', 'asymmetry_coefficient', 'kernel_groove_length', 'seed_class']
            try:
                if not all(field in data for field in required_fields):
                    raise ValueError('Required field(s) missing')

                area = float(data['area'])
                if area < 0:
                    raise ValueError("Area cannot be negative")
                perimeter = float(data['perimeter'])
                if perimeter < 0:
                    raise ValueError("Perimeter cannot be negative")
                compactness = float(data['compactness'])
                if compactness < 0:
                    raise ValueError("Compactness cannot be negative")
                kernel_length = float(data['kernel_length'])
                if kernel_length < 0:
                    raise ValueError("Kernel length cannot be negative")
                kernel_width = float(data['kernel_width'])
                if kernel_width < 0:
                    raise ValueError("Kernel width cannot be negative")
                asymmetry_coefficient = float(data['asymmetry_coefficient'])
                kernel_groove_length = float(data['kernel_groove_length'])
                if kernel_groove_length < 0:
                    raise ValueError("Kernel groove length cannot be negative")
                seed_class = int(data['seed_class'])
                if seed_class < 0 or seed_class > 3:
                    raise ValueError("Seed class is incorrect")

            except (ValueError, KeyError):
                return jsonify({'error': 'Invalid data'}), 400

            max_id = db.session.query(db.func.max(Seed.seed_id)).scalar()

            if max_id is None:
                max_id = 1
            else:
                max_id = max_id + 1

            new_seed = Seed(seed_id=max_id, area=area, perimeter=perimeter, compactness=compactness,
                            kernel_length=kernel_length,
                            kernel_width=kernel_width, asymmetry_coefficient=asymmetry_coefficient,
                            kernel_groove_length=kernel_groove_length, seed_class=seed_class)

            db.session.add(new_seed)
            db.session.commit()

            return jsonify({'seed_id': new_seed.seed_id}), 200
        else:
            flask.abort(400)

    @app.route('/delete/<int:record_id>', methods=['DELETE'])
    def api_delete(record_id):

        seed = Seed.query.get(record_id)

        if seed is None:
            return jsonify({'error': 'Record not found'}), 404

        else:
            db.session.delete(seed)
            db.session.commit()
            return jsonify({'seed_id': seed.seed_id}), 200