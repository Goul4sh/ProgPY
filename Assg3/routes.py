import flask
import numpy as np
from flask import render_template, request, redirect, url_for, jsonify
from models import Seed
from knn import train_knn_model


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

    @app.route('/predict', methods=['GET', 'POST'])
    def predict():

        if request.method == 'GET':
            return render_template('predict.html')
        if request.method == 'POST':

            try:

                features = [
                    float(request.form['area']),
                    float(request.form['perimeter']),
                    float(request.form['compactness']),
                    float(request.form['kernel_length']),
                    float(request.form['kernel_width']),
                    float(request.form['asymmetry_coefficient']),
                    float(request.form['kernel_groove_length']),
                ]

                if features[0] < 0:
                    raise ValueError("Area cannot be negative")
                if features[1] < 0:
                    raise ValueError("Perimeter cannot be negative")
                if features[2] < 0:
                    raise ValueError("Compactness cannot be negative")
                if features[3] < 0:
                    raise ValueError("Kernel length cannot be negative")
                if features[4] < 0:
                    raise ValueError("Kernel width cannot be negative")
                if features[6] < 0:
                    raise ValueError("Kernel groove length cannot be negative")

            except (ValueError, KeyError):
                flask.abort(400)

            knn_model, scaler = train_knn_model()

            if knn_model is None:
                return render_template('500.html',
                                       response="There are not enough records in the database for the prediction to proceed."), 500

            features = np.array(features).reshape(1, -1)

            features = scaler.transform(features)

            prediction = knn_model.predict(features)[0]
            return render_template('result.html', category=prediction)

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

            except KeyError:
                return jsonify({"error": "Missing required parameters"}), 400

            except ValueError:
                return jsonify({"error": "Invalid data"}), 400

            max_id = db.session.query(db.func.max(Seed.seed_id)).scalar()

            if max_id is None:
                max_id = 1
            else:
                max_id = max_id + 1

            new_seed = Seed(seed_id=max_id,
                            area=round(area, 4),
                            perimeter=round(perimeter, 4),
                            compactness=round(compactness, 4),
                            kernel_length=round(kernel_length, 4),
                            kernel_width=round(kernel_width, 4),
                            asymmetry_coefficient=round(asymmetry_coefficient, 4),
                            kernel_groove_length=round(kernel_groove_length, 4),
                            seed_class=seed_class)

            db.session.add(new_seed)
            db.session.commit()

            return jsonify({'seed_id': new_seed.seed_id}), 200

    @app.route('/api/data/<int:record_id>', methods=['DELETE'])
    def api_delete(record_id):

        seed = Seed.query.get(record_id)

        if seed is None:
            return jsonify({'error': 'Record not found'}), 404

        else:
            db.session.delete(seed)
            db.session.commit()
            return jsonify({'seed_id': seed.seed_id}), 200

    @app.route('/api/predictions', methods=['GET'])
    def api_predict():

        try:
            features = [
              round(float(request.args['area']),4),
                round(float(request.args['perimeter']),4),
                round(float(request.args['compactness']),4),
                round(float(request.args['kernel_length']),4),
                round(float(request.args['kernel_width']),4),
                round(float(request.args['asymmetry_coefficient']),4),
                round(float(request.args['kernel_groove_length']),4),
            ]

            if features[0] < 0:
                raise ValueError("Area cannot be negative")
            if features[1] < 0:
                raise ValueError("Perimeter cannot be negative")
            if features[2] < 0:
                raise ValueError("Compactness cannot be negative")
            if features[3] < 0:
                raise ValueError("Kernel length cannot be negative")
            if features[4] < 0:
                raise ValueError("Kernel width cannot be negative")
            if features[6] < 0:
                raise ValueError("Kernel groove length cannot be negative")

            knn_model, scaler = train_knn_model()

            if knn_model is None:
                return jsonify(
                    {'error': 'There are not enough records in the database for the prediction to proceed.'}), 500

            features = np.array(features).reshape(1, -1)

            features = scaler.transform(features)

            prediction = knn_model.predict(features)[0]

            return jsonify({"category": int(prediction)})

        except KeyError:
            return jsonify({"error": "Missing required parameters"}), 400

        except ValueError:
            return jsonify({"error": "Invalid data"}), 400
