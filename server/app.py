from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.serialize() for plant in plants])

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            return jsonify(plant.serialize())
        else:
            return jsonify({"message": "Plant not found"}), 404

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.serialize()), 201

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
