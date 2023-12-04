from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)


class PlantsIndex(Resource):
    def get(self):
        plants = Plant.query.all()
        response_dict_list = [plant.serialize() for plant in plants]
        response = make_response(jsonify(response_dict_list), 200)
        return response


class PlantShow(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            response_dict = plant.serialize()
            response = make_response(jsonify(response_dict), 200)
        else:
            response = make_response(jsonify({"error": "Plant not found"}), 404)
        return response


class PlantCreate(Resource):
    def post(self):
        data = request.get_json()
        new_plant = Plant(name=data["name"], image=data["image"], price=data["price"])
        db.session.add(new_plant)
        db.session.commit()

        response_dict = new_plant.serialize()
        response = make_response(jsonify(response_dict), 201)
        return response


api.add_resource(PlantsIndex, "/plants")
api.add_resource(PlantShow, "/plants/<int:id>")
api.add_resource(PlantCreate, "/plants")


if __name__ == "__main__":
    app.run(port=3000)
